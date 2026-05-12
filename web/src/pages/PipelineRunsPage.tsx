import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { loadPipelineRuns } from '../lib/pipelineRunsLoader';
import type { PipelineSession as PipelineSessionT } from '../types';
import { PipelineSession } from '../components/PipelineSession';

type DateRange = 'today' | '7d' | '30d' | 'all';
type Status = 'all' | 'success' | 'failed';

export function PipelineRunsPage() {
  const [params, setParams] = useSearchParams();
  const [sessions, setSessions] = useState<PipelineSessionT[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const tickersFilter = params.get('ticker')?.split(',').filter(Boolean) ?? [];
  const dateRange = (params.get('date') as DateRange) || 'all';
  const status = (params.get('status') as Status) || 'all';
  const expandBatchId = params.get('batch_id');

  useEffect(() => {
    loadPipelineRuns()
      .then((manifest) => {
        setSessions(manifest.sessions);
        setLoading(false);
      })
      .catch((e: Error) => {
        setError(`Lỗi load: ${e.message}`);
        setLoading(false);
      });
  }, []);

  const filteredSessions = useMemo(() => {
    let result = sessions;
    if (tickersFilter.length > 0) {
      result = result.filter((s) =>
        s.batches.some((b) => tickersFilter.includes(b.ticker)),
      );
    }
    if (dateRange !== 'all') {
      const cutoff = computeCutoff(dateRange);
      result = result.filter((s) => new Date(s.started_at) >= cutoff);
    }
    if (status !== 'all') {
      result = result.filter((s) =>
        status === 'success' ? s.chosen_total > 0 : s.chosen_total === 0,
      );
    }
    return result;
  }, [sessions, tickersFilter.join(','), dateRange, status]);

  const sessionToExpand = useMemo(() => {
    if (!expandBatchId) return null;
    return filteredSessions.find((s) =>
      s.batches.some((b) => b.funnel_batch_id === expandBatchId),
    );
  }, [filteredSessions, expandBatchId]);

  const updateFilter = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    if (!value || value === 'all') next.delete(key);
    else next.set(key, value);
    setParams(next, { replace: true });
  };

  if (loading) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-8">
        <p className="text-fg-3">Đang tải lịch sử pipeline...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-8">
        <div className="rounded-md border border-rec/40 bg-rec/10 p-4 text-rec">
          {error}
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-8">
      <h1 className="text-2xl font-semibold tracking-tight text-fg-0">
        Lịch sử pipeline run
      </h1>
      <p className="mt-2 text-sm text-fg-3">
        {filteredSessions.length}/{sessions.length} session
      </p>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <FilterSelect
          label="Khoảng thời gian"
          value={dateRange}
          options={[
            { value: 'today', label: 'Hôm nay' },
            { value: '7d', label: '7 ngày' },
            { value: '30d', label: '30 ngày' },
            { value: 'all', label: 'Tất cả' },
          ]}
          onChange={(v) => updateFilter('date', v)}
        />
        <FilterSelect
          label="Trạng thái"
          value={status}
          options={[
            { value: 'all', label: 'Tất cả' },
            { value: 'success', label: 'Thành công (≥1 chosen)' },
            { value: 'failed', label: 'Thất bại (0 chosen)' },
          ]}
          onChange={(v) => updateFilter('status', v)}
        />
      </div>

      <div className="mt-6 space-y-3">
        {filteredSessions.length === 0 ? (
          <p className="py-8 text-fg-3">Không có session nào cho bộ lọc đã chọn.</p>
        ) : (
          filteredSessions.map((session) => (
            <PipelineSession
              key={session.session_id}
              session={session}
              defaultExpanded={session === sessionToExpand}
              expandBatchId={session === sessionToExpand ? expandBatchId : undefined}
            />
          ))
        )}
      </div>
    </main>
  );
}

function FilterSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: { value: string; label: string }[];
  onChange: (value: string) => void;
}) {
  return (
    <label className="flex items-center gap-2 text-sm">
      <span className="text-fg-3">{label}:</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border border-fg-4/40 bg-bg-2 px-2 py-1 text-fg-0"
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function computeCutoff(range: DateRange): Date {
  const now = new Date();
  if (range === 'today') {
    const today = new Date(now);
    today.setHours(0, 0, 0, 0);
    return today;
  }
  if (range === '7d') {
    return new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  }
  if (range === '30d') {
    return new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
  }
  return new Date(0);
}

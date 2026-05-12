import { useState } from 'react';
import type { PipelineSession as PipelineSessionT } from '../types';
import { PipelineBatch } from './PipelineBatch';

function formatTriggerLabel(session: PipelineSessionT): string {
  if (session.trigger_type === 'tin') return `/tin ${session.trigger_args}`;
  if (session.trigger_type === 'tin-hot')
    return `/tin-hot ${session.trigger_args.replace('N=', '')}`;
  return `/${session.trigger_type} ${session.trigger_args}`;
}

function formatStartedAt(iso: string): string {
  const d = new Date(iso);
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

export function PipelineSession({
  session,
  defaultExpanded = false,
  expandBatchId,
}: {
  session: PipelineSessionT;
  defaultExpanded?: boolean;
  expandBatchId?: string | null;
}) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  return (
    <div className="rounded-lg border border-fg-4/40 bg-bg-2/40 p-4">
      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className="flex w-full items-center gap-3 text-left font-medium text-fg-0 hover:text-brand"
      >
        <span aria-hidden className="font-mono text-fg-3">
          {expanded ? '▼' : '▶'}
        </span>
        <span className="font-mono text-sm">{formatTriggerLabel(session)}</span>
        <span className="text-sm text-fg-3">· {formatStartedAt(session.started_at)}</span>
        <span className="text-sm text-fg-3">· {session.batches.length} ticker</span>
        <span className="ml-auto font-mono text-xs text-fg-3 tabular-nums">
          📊 {session.fetched_total} fetched, {session.chosen_total} chosen, {session.rejected_total} rejected
        </span>
      </button>

      {expanded && (
        <div className="mt-3 space-y-2">
          {session.batches.map((batch) => (
            <PipelineBatch
              key={batch.funnel_batch_id}
              batch={batch}
              defaultExpanded={batch.funnel_batch_id === expandBatchId}
            />
          ))}
        </div>
      )}
    </div>
  );
}

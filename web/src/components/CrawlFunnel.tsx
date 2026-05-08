import type { CrawlFunnelData, FunnelItem } from '../types';
import { formatPublishedDate } from '../lib/format';

function FunnelGroup({
  emoji,
  label,
  items,
  type,
}: {
  emoji: string;
  label: string;
  items: FunnelItem[];
  type: 'picked' | 'rejected';
}) {
  if (items.length === 0) return null;
  const labelColor = type === 'picked' ? 'text-green-700' : 'text-red-700';
  return (
    <div className="mb-3">
      <p className={`font-semibold mb-1 ${labelColor}`}>
        {emoji} <strong>{label}</strong> ({items.length})
      </p>
      <ul className="text-sm pl-4 space-y-1 mb-0">
        {items.map((item, i) => (
          <li key={i}>
            <a href={item.url} target="_blank" rel="noopener noreferrer">
              <strong>{item.source}</strong>
            </a>{' '}
            <span className="text-gray-500">({formatPublishedDate(item.published)})</span>{' '}
            — {item.reason}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function CrawlFunnel({
  data,
  funnelBatchId,
}: {
  data: CrawlFunnelData;
  funnelBatchId: string;
}) {
  const total =
    data.picked.length +
    data.rejected_editor_v1.length +
    data.rejected_story_editor.length +
    data.rejected_master.length;

  return (
    <details>
      <summary className="text-sm">
        📊 Crawl funnel — đã search nhiều nguồn, {total} candidate, {data.picked.length} picked
      </summary>
      <div className="mt-3 text-sm">
        <p className="text-gray-500 text-xs mb-3">
          <strong>Funnel batch</strong>: <code>{funnelBatchId}</code> · Sort: by Published_time desc
        </p>
        <FunnelGroup emoji="✅" label="Picked" items={data.picked} type="picked" />
        <FunnelGroup
          emoji="❌"
          label="Rejected by Editor V1"
          items={data.rejected_editor_v1}
          type="rejected"
        />
        <FunnelGroup
          emoji="❌"
          label="Rejected by Story Editor"
          items={data.rejected_story_editor}
          type="rejected"
        />
        <FunnelGroup
          emoji="❌"
          label="Rejected by Master"
          items={data.rejected_master}
          type="rejected"
        />
      </div>
    </details>
  );
}

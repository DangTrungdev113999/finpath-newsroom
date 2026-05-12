import { useState } from 'react';
import type {
  PipelineBatch as PipelineBatchT,
  PipelineRejectedItem,
  PipelinePickedItem,
} from '../types';

export function PipelineBatch({
  batch,
  defaultExpanded = false,
}: {
  batch: PipelineBatchT;
  defaultExpanded?: boolean;
}) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  return (
    <div className="border-l-2 border-fg-4/40 pl-3 py-2">
      <button
        type="button"
        onClick={() => setExpanded((v) => !v)}
        className="flex w-full items-center gap-2 text-left text-sm font-medium text-fg-1 hover:text-fg-0"
      >
        <span aria-hidden className="font-mono text-fg-3">
          {expanded ? '▼' : '▶'}
        </span>
        <span className="font-mono">{batch.ticker}</span>
        {batch.sector_name && (
          <span className="text-fg-3"> · {batch.sector_name}</span>
        )}
        {batch.hot_nhom && (
          <span className="text-fg-3">
            {' '}· {batch.hot_nhom} #{batch.hot_rank}
          </span>
        )}
        <span className="ml-auto font-mono text-xs text-fg-3 tabular-nums">
          {batch.fetched_count}/{batch.chosen_count}/{batch.rejected_count}
        </span>
      </button>

      {expanded && (
        <div className="mt-2 pl-4 space-y-3 text-sm">
          {batch.funnel_detail.picked.length > 0 && (
            <PickedList items={batch.funnel_detail.picked} />
          )}
          {batch.funnel_detail.rejected.length > 0 && (
            <RejectedList items={batch.funnel_detail.rejected} />
          )}
        </div>
      )}
    </div>
  );
}

function PickedList({ items }: { items: PipelinePickedItem[] }) {
  return (
    <div>
      <h4 className="text-xs font-semibold uppercase tracking-wide text-green-600">
        ✅ Đã chọn ({items.length})
      </h4>
      <ul className="mt-1 space-y-1">
        {items.map((item, idx) => (
          <li key={idx} className="text-fg-2">
            <a
              href={item.url}
              target="_blank"
              rel="noreferrer noopener"
              className="font-medium text-brand hover:underline"
            >
              {item.source}
            </a>
            <span className="text-fg-3"> ({item.published})</span>
            <span className="text-fg-3"> — {item.reason}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function RejectedList({ items }: { items: PipelineRejectedItem[] }) {
  return (
    <div>
      <h4 className="text-xs font-semibold uppercase tracking-wide text-rec">
        ❌ Không chọn ({items.length})
      </h4>
      <ul className="mt-1 space-y-1">
        {items.map((item, idx) => (
          <li key={idx} className="text-fg-2">
            <a
              href={item.url}
              target="_blank"
              rel="noreferrer noopener"
              className="font-medium text-brand hover:underline"
            >
              {item.source}
            </a>
            <span className="text-fg-3"> ({item.published})</span>
            <span className="ml-2 font-mono text-xs text-rec">{item.reject_label}</span>
            <span className="text-fg-3"> — {item.reason}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

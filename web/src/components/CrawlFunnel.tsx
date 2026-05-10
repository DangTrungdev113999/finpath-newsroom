import type { CrawlFunnelData, FunnelItem } from '../types';
import { formatPublishedDate } from '../lib/format';

function FunnelEntry({ item }: { item: FunnelItem }) {
  return (
    <li>
      <a href={item.url} target="_blank" rel="noopener noreferrer">
        <strong>{item.source}</strong>
      </a>{' '}
      <span className="text-fg-3">({formatPublishedDate(item.published)})</span>
      {item.reject_label && (
        <>
          {' '}— <em className="text-rec">{item.reject_label}</em>
        </>
      )}
      <div className="text-sm text-fg-2 ml-4 mt-1">
        {item.reject_label ? 'Vì sao bỏ' : 'Lý do chọn'}: {item.reason}
      </div>
    </li>
  );
}

export function CrawlFunnel({
  data,
  funnelBatchId,
}: {
  data: CrawlFunnelData;
  funnelBatchId: string;
}) {
  return (
    <details>
      <summary className="section-pill">
        Crawl funnel — đã quét nhiều nguồn, gom {data.total_candidates} bài, chọn {data.picked.length}, loại {data.rejected.length}
      </summary>
      <div className="mt-3 text-sm space-y-4">
        <p className="text-fg-3 text-xs">
          <strong>Funnel batch</strong>: <code>{funnelBatchId}</code>
        </p>
        {data.picked.length > 0 && (
          <div>
            <p className="font-semibold text-done mb-1">✅ ĐÃ CHỌN ({data.picked.length})</p>
            <ul className="space-y-2 pl-4">
              {data.picked.map((item, i) => (
                <FunnelEntry key={i} item={item} />
              ))}
            </ul>
          </div>
        )}
        {data.rejected.length > 0 && (
          <div>
            <p className="font-semibold text-rec mb-1">❌ KHÔNG CHỌN ({data.rejected.length})</p>
            <ul className="space-y-2 pl-4">
              {data.rejected.map((item, i) => (
                <FunnelEntry key={i} item={item} />
              ))}
            </ul>
          </div>
        )}
      </div>
    </details>
  );
}

import type { CrawlFunnelData, SourceMeta, WhyChosenItem } from '../types';
import { Markdown } from './Markdown';
import { CrawlFunnel } from './CrawlFunnel';
import { formatPublishedDate } from '../lib/format';

export function RightColumn({
  source,
  whyChosen,
  crawlFunnel,
  funnelBatchId,
  rawBody,
}: {
  source: SourceMeta;
  whyChosen: WhyChosenItem[];
  crawlFunnel: CrawlFunnelData;
  funnelBatchId: string;
  rawBody: string;
}) {
  return (
    <section>
      <h2>📰 Raw text gốc + meta</h2>
      <p className="text-base font-semibold text-gray-800 mb-1 mt-0">{source.raw_title}</p>
      <p className="text-sm text-gray-500 italic mb-4">
        Nguồn:{' '}
        <a href={source.url} target="_blank" rel="noopener noreferrer">
          {source.name} — bấm để đọc bài gốc
        </a>{' '}
        · Published {formatPublishedDate(source.published)}
      </p>

      <div className="mb-5">
        <p className="font-semibold mb-2">Cách viết & lý do chọn:</p>
        <ul>
          {whyChosen.map((item, i) => (
            <li key={i}>
              <strong>{item.label}</strong>: {item.content}
            </li>
          ))}
        </ul>
      </div>

      <CrawlFunnel data={crawlFunnel} funnelBatchId={funnelBatchId} />

      <details className="mt-4">
        <summary className="text-sm">📖 Click đọc full bài viết gốc</summary>
        <div className="mt-3 text-sm">
          <Markdown>{rawBody}</Markdown>
        </div>
      </details>
    </section>
  );
}

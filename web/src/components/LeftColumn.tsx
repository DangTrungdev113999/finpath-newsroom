import type { LeftMeta } from '../types';
import { Markdown } from './Markdown';
import { InsightCallout } from './InsightCallout';

export function LeftColumn({
  title,
  meta,
  insight,
  body,
}: {
  title: string;
  meta: LeftMeta;
  insight: string;
  body: string;
}) {
  return (
    <section>
      <h2>✍️ Bài AI viết lại</h2>
      <p className="text-base font-semibold text-gray-800 mb-1 mt-0">
        <a href="#" className="underline">
          {title}
        </a>
      </p>
      <p className="text-sm text-gray-500 italic mb-4">
        — {meta.author} · {meta.word_count} từ · key view: {meta.key_view} · Skeptic:{' '}
        <code>{meta.skeptic_verdict}</code> · {meta.pipeline_version}
      </p>

      <InsightCallout insight={insight} />
      <Markdown>{body}</Markdown>
    </section>
  );
}

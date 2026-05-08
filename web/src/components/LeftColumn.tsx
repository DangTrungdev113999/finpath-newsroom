import type { LeftMeta } from '../types';
import { Markdown } from './Markdown';
import { InsightCallout } from './InsightCallout';
import { PipelineLog } from './PipelineLog';

export function LeftColumn({
  title,
  meta,
  insight,
  body,
  pipelineLog,
}: {
  title: string;
  meta: LeftMeta;
  insight: string;
  body: string;
  pipelineLog: Record<string, unknown>;
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
        <br />
        {meta.format_check}
      </p>

      <InsightCallout insight={insight} />
      <Markdown>{body}</Markdown>
      <PipelineLog log={pipelineLog} />
    </section>
  );
}

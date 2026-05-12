import type { LeftMeta } from "../types";
import { Markdown } from "./Markdown";
import { TTSButton } from "./TTSButton";

// Split body tại heading "## Góc nhìn ngược" → meta line chèn vào giữa
// (giữa Master body kết thúc và Skeptic critique bắt đầu).
const SKEPTIC_HEADING_RE = /\n*#{2,3}\s+G[óo]c\s+nh[iì]n\s+ng[ưu][ợo]?c\s*\n/;

export function LeftColumn({ meta, body }: { meta: LeftMeta; body: string }) {
  const headingMatch = body.match(SKEPTIC_HEADING_RE);
  const splitIdx = headingMatch?.index;
  const masterBody =
    splitIdx != null ? body.slice(0, splitIdx).trim() : body.trim();
  const skepticBody =
    splitIdx != null && headingMatch
      ? body.slice(splitIdx + headingMatch[0].length).trim()
      : "";

  return (
    <section>
      <div className="!mt-0 !mb-6 flex items-center justify-between gap-3 px-4 py-2.5 rounded-r-xl bg-bg-2 border-l-[3px] border-fg-4">
        <h2 className="!m-0 text-base font-semibold text-fg-0">
          Bài Agent phân tích
        </h2>
        <TTSButton text={body} />
      </div>
      <Markdown>{masterBody}</Markdown>

      <p className="text-sm text-fg-3 italic my-4">
        — {meta.author} · {meta.word_count} từ · key view: {meta.key_view} ·
        Skeptic: <code>{meta.skeptic_verdict}</code> · {meta.pipeline_version}
      </p>

      {skepticBody && (
        <details className="mt-6">
          <summary className="section-pill">Góc nhìn ngược</summary>
          <div className="mt-3">
            <Markdown>{skepticBody}</Markdown>
          </div>
        </details>
      )}
    </section>
  );
}

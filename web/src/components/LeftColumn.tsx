import type { LeftMeta } from "../types";
import { Markdown } from "./Markdown";

// Split body tại heading "## Góc nhìn ngược" → meta line chèn vào giữa
// (giữa Master body kết thúc và Skeptic critique bắt đầu).
const SKEPTIC_HEADING_RE = /\n*#{2,3}\s+G[óo]c\s+nh[iì]n\s+ng[ưu][ợo]?c\s*\n/;

export function LeftColumn({ meta, body }: { meta: LeftMeta; body: string }) {
  const headingMatch = body.match(SKEPTIC_HEADING_RE);
  const splitIdx = headingMatch?.index;
  const masterBody =
    splitIdx != null ? body.slice(0, splitIdx).trim() : body.trim();
  const skepticSection = splitIdx != null ? body.slice(splitIdx).trim() : "";

  return (
    <section>
      <h2 className="!mt-0 !mb-6 px-4 py-2.5 rounded-r-xl bg-bg-2 border-l-[3px] border-fg-4 text-base font-semibold text-fg-0">
        Bài Agent phân tích
      </h2>
      <Markdown>{masterBody}</Markdown>

      <p className="text-sm text-fg-3 italic my-4">
        — {meta.author} · {meta.word_count} từ · key view: {meta.key_view} ·
        Skeptic: <code>{meta.skeptic_verdict}</code> · {meta.pipeline_version}
      </p>

      {skepticSection && <Markdown>{skepticSection}</Markdown>}
    </section>
  );
}

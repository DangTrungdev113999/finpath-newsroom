/**
 * Strip Markdown syntax → plain reading text.
 *
 * Conservative implementation: no AST parsing, just regex sweeps that cover
 * the syntax our Newsroom articles use (headings, bold/italic, code, links,
 * bullets, blockquotes). Paragraph breaks become "." so the TTS engine pauses
 * naturally between sections.
 */
export function stripMarkdown(md: string): string {
  return md
    .replace(/```[\s\S]*?```/g, '')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/__([^_]+)__/g, '$1')
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '$1')
    .replace(/(?<!_)_([^_]+)_(?!_)/g, '$1')
    .replace(/~~([^~]+)~~/g, '$1')
    .replace(/^>\s+/gm, '')
    .replace(/^[-*+]\s+/gm, '')
    .replace(/^\d+\.\s+/gm, '')
    .replace(/\n{2,}/g, '. ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Split text into ~200-char chunks at sentence boundaries.
 *
 * Chrome's SpeechSynthesis silently stops after ~15s utterances; chunking
 * keeps each utterance short so onend fires reliably and pause/resume works.
 */
export function chunkForTTS(text: string, maxLen = 200): string[] {
  const sentences = text.split(/(?<=[.!?…])\s+/);
  const chunks: string[] = [];

  for (const s of sentences) {
    if (s.length <= maxLen) {
      chunks.push(s);
      continue;
    }
    // Long sentence — split at commas, then hard-split if still too long
    const parts = s.split(/(?<=,)\s+/);
    let buf = '';
    for (const p of parts) {
      if ((buf + ' ' + p).trim().length > maxLen && buf) {
        chunks.push(buf.trim());
        buf = p;
      } else {
        buf = (buf + ' ' + p).trim();
      }
    }
    if (buf) chunks.push(buf);
  }

  return chunks.filter((c) => c.length > 0);
}

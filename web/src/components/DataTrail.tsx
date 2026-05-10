import type { DataTrailEntry } from '../types';

function renderSource(source: string) {
  if (source.startsWith('http://') || source.startsWith('https://')) {
    return (
      <a href={source} target="_blank" rel="noopener noreferrer" className="font-semibold underline">
        {source}
      </a>
    );
  }
  if (source.startsWith('WebSearch:')) {
    return <span className="font-semibold italic">{source}</span>;
  }
  if (
    source.startsWith('Finpath_API/') ||
    source.startsWith('KB/') ||
    source.startsWith('Manual_YAML/')
  ) {
    return (
      <code className="font-mono text-xs bg-bg-2 rounded px-1.5 py-0.5 text-fg-1">{source}</code>
    );
  }
  // Fallback: plain text (e.g. "Lập luận tự" or legacy free-text label)
  return <span className="font-semibold">{source}</span>;
}

export function DataTrail({
  title,
  emoji,
  trail,
}: {
  title: string;
  emoji: string;
  trail: DataTrailEntry[] | undefined;
}) {
  // Phase G — luôn render section (kể cả empty) để legacy articles vẫn hiển thị
  // structure đầy đủ. Empty trail → expand thấy "Lỗi log ở pipeline".
  const isEmpty = !trail || trail.length === 0;
  if (isEmpty) {
    return (
      <details>
        <summary className="section-pill">
          {title} (0 nguồn)
        </summary>
        <p className="mt-3 text-sm text-rec italic pl-3 border-l-2 border-rec/30">
          ⚠️ Lỗi log ở pipeline — agent không emit data_trail (legacy article hoặc bug).
        </p>
      </details>
    );
  }
  return (
    <details>
      <summary className="section-pill">
        {title} ({trail.length} nguồn)
      </summary>
      <ul className="mt-3 text-sm space-y-3">
        {trail.map((entry, i) => {
          // Backward compat: legacy entries have only `used_for`, map to supports_argument
          const supportsArg = entry.supports_argument || entry.used_for || '';
          const purpose = entry.purpose || '';
          return (
            <li key={i} className="border-l-2 border-fg-4/40 pl-3">
              <div>→ {renderSource(entry.source)}</div>
              {entry.fetched && (
                <div className="text-fg-2 mt-1">
                  <em>Tra được</em>: {entry.fetched}
                </div>
              )}
              {purpose && (
                <div className="text-fg-2 mt-1">
                  <em>Vì sao tra</em>: {purpose}
                </div>
              )}
              {supportsArg && (
                <div className="text-fg-2 mt-1">
                  <em>Bổ sung cho</em>: {supportsArg}
                </div>
              )}
            </li>
          );
        })}
      </ul>
    </details>
  );
}

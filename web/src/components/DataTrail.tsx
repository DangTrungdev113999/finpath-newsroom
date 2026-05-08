import type { DataTrailEntry } from '../types';

export function DataTrail({
  title,
  emoji,
  trail,
}: {
  title: string;
  emoji: string;
  trail: DataTrailEntry[];
}) {
  if (!trail || trail.length === 0) return null;
  return (
    <section>
      <h3>{emoji} {title}</h3>
      <ul className="text-sm space-y-2">
        {trail.map((entry, i) => {
          const isUrl = entry.source.startsWith('http://') || entry.source.startsWith('https://');
          return (
            <li key={i}>
              <div>
                → {isUrl ? (
                  <a href={entry.source} target="_blank" rel="noopener noreferrer" className="font-semibold">
                    {entry.source}
                  </a>
                ) : (
                  <span className="font-semibold">{entry.source}</span>
                )}
              </div>
              <div className="text-gray-600 ml-4">
                <em>Tra được</em>: {entry.fetched}
              </div>
              <div className="text-gray-600 ml-4">
                <em>Dùng cho</em>: {entry.used_for}
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

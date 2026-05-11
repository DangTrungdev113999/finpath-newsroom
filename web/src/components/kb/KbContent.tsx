import type { KbDoc } from '../../lib/kbTypes';
import { titleForSlug } from '../../lib/kbTree';
import { KbMarkdown } from './KbMarkdown';

export function KbContent({ doc }: { doc: KbDoc }) {
  const title = titleForSlug(doc.slug, doc.body, doc.meta.title);
  const lastUpdated = doc.meta.last_updated;
  const appliesTo = doc.meta.applies_to;

  return (
    <article className="mx-auto w-full max-w-[760px] px-6 py-8">
      <header className="mb-8 border-b border-fg-4/40 pb-5">
        <h1 className="font-sans text-3xl font-semibold tracking-tight text-fg-0">
          {title}
        </h1>
        <MetaStrip lastUpdated={lastUpdated} appliesTo={appliesTo} />
      </header>
      <KbMarkdown>{doc.body}</KbMarkdown>
    </article>
  );
}

function MetaStrip({
  lastUpdated,
  appliesTo,
}: {
  lastUpdated: string | undefined;
  appliesTo: string[] | undefined;
}) {
  const hasUpdate = Boolean(lastUpdated);
  const hasApplies = Array.isArray(appliesTo) && appliesTo.length > 0;
  if (!hasUpdate && !hasApplies) return null;

  return (
    <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 font-sans text-[12px] text-fg-2">
      {hasUpdate && (
        <span>
          cập nhật <span className="font-medium text-fg-1">{lastUpdated}</span>
        </span>
      )}
      {hasUpdate && hasApplies && (
        <span aria-hidden className="text-fg-4">·</span>
      )}
      {hasApplies && <AppliesToChips items={appliesTo!} />}
    </div>
  );
}

function AppliesToChips({ items }: { items: string[] }) {
  if (items.length === 1 && items[0] === 'all') {
    return <span>áp dụng: tất cả mã ngành</span>;
  }
  return (
    <span className="flex flex-wrap items-center gap-1.5">
      <span>áp dụng:</span>
      {items.map((t) => (
        <span
          key={t}
          className="inline-flex h-5 items-center rounded-full border border-emerald-400/40 bg-emerald-400/10 px-2 font-mono text-[10.5px] font-medium tabular-nums text-emerald-300"
        >
          {t}
        </span>
      ))}
    </span>
  );
}

export function KbContentNotFound({ slug }: { slug: string }) {
  return (
    <div className="mx-auto w-full max-w-[760px] px-6 py-12">
      <p className="text-fg-2">
        KB <code className="rounded bg-bg-2 px-1.5 py-0.5">{slug}</code> không
        tồn tại trong sector này. Chọn 1 KB từ sidebar bên trái.
      </p>
    </div>
  );
}

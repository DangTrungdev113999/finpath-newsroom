export function ArticleCardSkeleton() {
  return (
    <div
      aria-hidden
      className="flex flex-col rounded-xl border border-fg-4/40 bg-bg-1 p-5"
    >
      <div className="mb-5 flex items-center justify-between">
        <div className="h-[26px] w-12 rounded-md bg-bg-3 animate-pulse" />
        <div className="h-3 w-16 rounded-full bg-bg-3 animate-pulse" />
      </div>
      <div className="flex-1 space-y-2.5">
        <div className="h-4 w-full rounded bg-bg-3 animate-pulse" />
        <div className="h-4 w-[85%] rounded bg-bg-3 animate-pulse" />
        <div className="h-4 w-[55%] rounded bg-bg-3 animate-pulse" />
      </div>
      <div className="mt-5 flex items-center justify-between border-t border-fg-4/30 pt-3">
        <div className="h-3 w-12 rounded-full bg-bg-3 animate-pulse" />
        <div className="h-3 w-3 rounded-full bg-bg-3 animate-pulse" />
      </div>
    </div>
  );
}

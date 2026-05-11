export function CompareFeedSkeleton({ showRight = true }: { showRight?: boolean }) {
  return (
    <div aria-hidden className="max-w-7xl mx-auto px-4 py-6">
      {/* Title block */}
      <div className={showRight ? '' : 'max-w-3xl mx-auto'}>
        <div className="h-7 w-[80%] rounded bg-bg-3 animate-pulse" />
        <div className="mt-2 h-7 w-[55%] rounded bg-bg-3 animate-pulse" />
        <div className="mt-3 h-3 w-[60%] rounded-full bg-bg-3 animate-pulse" />
      </div>

      <hr className={`my-5 border-fg-4/40 ${showRight ? '' : 'max-w-3xl mx-auto'}`} />

      {showRight ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6">
          <ColumnSkeleton />
          <ColumnSkeleton compact />
        </div>
      ) : (
        <div className="max-w-3xl mx-auto">
          <ColumnSkeleton />
        </div>
      )}
    </div>
  );
}

function ColumnSkeleton({ compact = false }: { compact?: boolean }) {
  const lines = compact ? 6 : 10;
  return (
    <div className="space-y-3">
      {/* meta strip */}
      <div className="flex flex-wrap items-center gap-2">
        <div className="h-5 w-20 rounded bg-bg-3 animate-pulse" />
        <div className="h-5 w-16 rounded bg-bg-3 animate-pulse" />
        <div className="h-5 w-24 rounded bg-bg-3 animate-pulse" />
      </div>
      {/* body lines */}
      <div className="space-y-2.5 pt-2">
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            className="h-3.5 rounded bg-bg-3 animate-pulse"
            style={{ width: `${88 - (i % 4) * 9}%` }}
          />
        ))}
      </div>
      {/* bullet block */}
      <div className="space-y-2 pt-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="flex items-start gap-2">
            <div className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-bg-3 animate-pulse" />
            <div className="flex-1 space-y-1.5">
              <div className="h-3.5 w-[92%] rounded bg-bg-3 animate-pulse" />
              <div className="h-3.5 w-[70%] rounded bg-bg-3 animate-pulse" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function InsightCallout({ insight }: { insight: string }) {
  return (
    <div className="my-5 flex gap-3 rounded-md border border-callout-border bg-callout-bg px-4 py-3">
      <span className="text-callout-icon text-lg leading-relaxed shrink-0">💡</span>
      <p className="leading-relaxed m-0">
        <strong className="font-semibold">Insight</strong>: {insight}
      </p>
    </div>
  );
}

export function InsightCallout({ insight }: { insight: string }) {
  return (
    <div className="rounded-md border border-callout-border bg-callout-bg px-4 py-3">
      <p className="leading-relaxed m-0">{insight}</p>
    </div>
  );
}

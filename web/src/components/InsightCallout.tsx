export function InsightCallout({ insight }: { insight: string }) {
  return (
    <div className="rounded-md border border-brand/30 bg-brand/[0.08] px-4 py-3 text-fg-1">
      <p className="leading-relaxed m-0">{insight}</p>
    </div>
  );
}

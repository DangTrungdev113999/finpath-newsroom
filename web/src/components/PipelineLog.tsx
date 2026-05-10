export function PipelineLog({ log }: { log: Record<string, unknown> }) {
  if (!log || Object.keys(log).length === 0) return null;
  return (
    <details className="mt-6 border-t border-fg-4/40 pt-3">
      <summary className="text-sm">📋 Pipeline log</summary>
      <pre className="mt-3 bg-bg-2 text-fg-1 rounded p-3 overflow-x-auto text-xs leading-relaxed">
        {JSON.stringify(log, null, 2)}
      </pre>
    </details>
  );
}

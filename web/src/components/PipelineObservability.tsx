import type { PipelineLog, StepLog } from '../types';

interface Props {
  pipelineLog?: PipelineLog;
}

const STEP_LABELS: Array<{ key: keyof PipelineLog; label: string }> = [
  { key: 'step_1_crawler', label: '1. Crawler' },
  { key: 'step_2_editor', label: '2. Editor V1' },
  { key: 'step_3_story_editor', label: '3. Story Editor' },
  { key: 'step_4_master', label: '4. Master' },
  { key: 'step_5_skeptic', label: '5. Skeptic' },
  { key: 'step_6_render', label: '6. Render' },
];

export function PipelineObservability({ pipelineLog }: Props) {
  if (!pipelineLog) return null;

  const steps = STEP_LABELS
    .map(({ key, label }) => ({ key, label, log: pipelineLog[key] as StepLog | undefined }))
    .filter((s): s is { key: keyof PipelineLog; label: string; log: StepLog } => Boolean(s.log));

  if (steps.length === 0) return null;

  const totalMs = steps.reduce((sum, s) => sum + (s.log.duration_ms ?? 0), 0);
  const tokensPresent = steps.some(s => s.log.tokens != null);
  const totalTokens = steps.reduce((sum, s) => sum + (s.log.tokens ?? 0), 0);
  const tokensLabel = tokensPresent ? `${totalTokens.toLocaleString()} tokens` : '— tokens';

  return (
    <details className="text-sm">
      <summary className="cursor-pointer font-semibold">
        ⚙️ Pipeline run — {tokensLabel} · {(totalMs / 1000).toFixed(1)}s
      </summary>
      <table className="mt-3 w-full text-xs border-collapse">
        <thead>
          <tr className="border-b border-gray-300">
            <th className="text-left py-1.5 pr-2 font-semibold">Step</th>
            <th className="text-left py-1.5 pr-2 font-semibold">Model</th>
            <th className="text-right py-1.5 pr-2 font-semibold">Duration</th>
            <th className="text-right py-1.5 font-semibold">Tokens</th>
          </tr>
        </thead>
        <tbody>
          {steps.map(({ key, label, log }) => (
            <tr key={key} className="border-b border-gray-200">
              <td className="py-1.5 pr-2">{label}</td>
              <td className="py-1.5 pr-2">
                <code className="font-mono text-[10px] bg-gray-100 rounded px-1 py-0.5">
                  {log.model ?? '—'}
                </code>
              </td>
              <td className="py-1.5 pr-2 text-right text-gray-600">
                {log.duration_ms != null ? `${log.duration_ms.toLocaleString()}ms` : '—'}
              </td>
              <td className="py-1.5 text-right text-gray-600">
                {log.tokens != null ? log.tokens.toLocaleString() : '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  );
}

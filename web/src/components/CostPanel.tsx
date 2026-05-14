import type { CostBreakdown } from '../types';

interface Props {
  costs: CostBreakdown | undefined;
}

function formatUsd(value: number | undefined): string {
  if (typeof value !== 'number' || Number.isNaN(value)) return '—';
  // 4 decimals captures fractional cents for cheap calls; >$1 still renders fine.
  return `$${value.toFixed(4)}`;
}

function formatTokens(value: number | undefined): string {
  if (typeof value !== 'number' || Number.isNaN(value)) return '—';
  return value.toLocaleString('en-US');
}

/** V5.1.8 — Chi phí AI per article. Collapsed by default; expand shows
 *  per-model breakdown (Claude / Gemini / Grok / Image) with input/output
 *  tokens + USD cost. Renders nothing when `costs` is undefined or empty. */
export function CostPanel({ costs }: Props) {
  if (!costs) return null;
  const hasAny = Object.values(costs).some((v) => typeof v === 'number');
  if (!hasAny) return null;

  const total = costs.total_cost_usd ?? 0;

  const rows: Array<{ label: string; tokIn?: number; tokOut?: number; usd?: number }> = [
    {
      label: 'Claude Master',
      tokIn: costs.claude_tokens_in,
      tokOut: costs.claude_tokens_out,
      usd: costs.claude_cost_usd,
    },
    {
      label: 'Gemini Writer',
      tokIn: costs.gemini_tokens_in,
      tokOut: costs.gemini_tokens_out,
      usd: costs.gemini_cost_usd,
    },
    {
      label: 'Grok Writer',
      tokIn: costs.grok_tokens_in,
      tokOut: costs.grok_tokens_out,
      usd: costs.grok_cost_usd,
    },
  ];
  if (typeof costs.image_cost_usd === 'number') {
    rows.push({ label: 'Imagen thumb', usd: costs.image_cost_usd });
  }

  return (
    <section>
      <details>
        <summary className="cursor-pointer list-none">
          <span className="section-pill">Chi phí AI</span>
          <span className="ml-2 font-mono text-sm text-fg-2">{formatUsd(total)}</span>
        </summary>
        <table className="mt-3 w-full text-sm">
          <thead>
            <tr className="text-fg-3 text-left">
              <th className="font-normal pb-1">Model</th>
              <th className="font-normal pb-1 text-right">Token in</th>
              <th className="font-normal pb-1 text-right">Token out</th>
              <th className="font-normal pb-1 text-right">USD</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.label} className="border-t border-fg-4/30">
                <td className="py-1">{r.label}</td>
                <td className="py-1 text-right font-mono">{formatTokens(r.tokIn)}</td>
                <td className="py-1 text-right font-mono">{formatTokens(r.tokOut)}</td>
                <td className="py-1 text-right font-mono">{formatUsd(r.usd)}</td>
              </tr>
            ))}
            <tr className="border-t border-fg-4/60 font-semibold">
              <td className="pt-2">Tổng</td>
              <td colSpan={2} />
              <td className="pt-2 text-right font-mono">{formatUsd(total)}</td>
            </tr>
          </tbody>
        </table>
      </details>
    </section>
  );
}

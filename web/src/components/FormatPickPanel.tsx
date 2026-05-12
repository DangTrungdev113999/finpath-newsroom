import type { FormatDirectorData } from '../types';
import { getFormatCategory } from '../lib/formatCategories';

const TONE_LABELS: Record<string, string> = {
  neutral: 'Trung lập',
  acknowledge_market_red: 'Phiên đỏ',
  acknowledge_market_green: 'Phiên xanh',
};

const FORMAT_BADGE_COLORS: Record<string, string> = {
  flash_qa: 'bg-blue-100 text-blue-700',
  standard_qa: 'bg-green-100 text-green-700',
  standard_listicle: 'bg-purple-100 text-purple-700',
  standard_narrative: 'bg-orange-100 text-orange-700',
};

/**
 * V5.0 — Render Format Director output (step_3_5).
 * Returns null for V3.6/V4.0 legacy articles (graceful degrade).
 */
export function FormatPickPanel({
  data,
}: {
  data: FormatDirectorData | null | undefined;
}) {
  if (!data) return null;

  const category = getFormatCategory(data.format_id);
  const label = category?.label ?? data.format_id;
  const badgeClass =
    FORMAT_BADGE_COLORS[data.format_id] ?? 'bg-bg-2 text-fg-1';
  const toneLabel = TONE_LABELS[data.tone_bias] ?? data.tone_bias;
  const varietyWarn = data.variety_check?.current_pick_diversity_warning;
  const recentFormats = data.variety_check?.recent_3_articles_same_ticker_formats;

  return (
    <details className="text-sm">
      <summary className="section-pill">Format chọn</summary>
      <div className="mt-3 pl-3 border-l-2 border-fg-4/40 space-y-2">
        <div>
          <span
            className={`inline-block rounded px-2 py-1 text-xs font-semibold ${badgeClass}`}
          >
            {label}
          </span>
          <span className="ml-2 text-fg-2">
            Mục tiêu {data.length_target} từ · Tone: {toneLabel}
          </span>
        </div>
        <div className="text-fg-2">
          <em>Lý do</em>: {data.format_reason}
        </div>
        {varietyWarn && recentFormats && recentFormats.length > 0 && (
          <div className="text-xs italic text-amber-600">
            Cảnh báo đa dạng: 3 bài gần đây cùng mã đã dùng các format{' '}
            <code className="font-mono text-[10px] bg-bg-2 text-fg-1 rounded px-1 py-0.5">
              {recentFormats.join(', ')}
            </code>
            .
          </div>
        )}
      </div>
    </details>
  );
}

import { useMemo, useId, type CSSProperties } from 'react';

/**
 * Deterministic 32-bit hash (djb2). Same ticker → same visual fingerprint
 * across renders / sessions, so SHB always reads as SHB, VHM as VHM. Distinct
 * tickers land on different spotlight corners + tilt + accent marks even
 * when ticker characters partially overlap (e.g. SHB vs SBT).
 */
function hashStr(s: string): number {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

const SPOTLIGHTS: ReadonlyArray<readonly [string, string]> = [
  ['16%', '22%'],
  ['84%', '24%'],
  ['22%', '80%'],
  ['78%', '78%'],
  ['52%', '14%'],
  ['12%', '55%'],
  ['88%', '52%'],
];

// Serif-leaning glyphs — chosen so they sit beside the editorial pill chips
// without reading as "magical fantasy". Each ticker pulls one at random.
const DECOR = ['✦', '✧', '◈', '◊', '✶', '✷', '✺'];

/**
 * Hero slot for ArticleCard when no Imagen thumb exists. The point is NOT to
 * fake a photo — instead we lean into the absence and turn the slot into a
 * miniature editorial poster: deep ink ground + warm amber light pool +
 * over-sized italic display ticker bleeding off the bottom-right corner.
 *
 * Per-ticker fingerprint (deterministic, no JS animation):
 *   - spotlight position    → 7 corners around the frame
 *   - hue rotation          → ±12° around the brand amber
 *   - italic tilt           → −3° to +3°
 *   - decorative glyph      → 1 of 7 serif marks (top-right corner)
 *
 * The result is that 4 cards stacked together each read as a distinct poster
 * even though every card uses the same component.
 */
export function TickerHero({
  ticker,
  sector,
}: {
  ticker: string;
  sector?: string;
}) {
  const filterId = useId();
  const fingerprint = useMemo(() => {
    const h = hashStr(ticker || 'XXX');
    return {
      spotlight: SPOTLIGHTS[h % SPOTLIGHTS.length],
      tilt: ((h >> 3) % 7) - 3,
      hueShift: ((h >> 5) % 24) - 12,
      mark: DECOR[(h >> 7) % DECOR.length],
    };
  }, [ticker]);

  const cssVars = {
    '--sx': fingerprint.spotlight[0],
    '--sy': fingerprint.spotlight[1],
    '--tilt': `${fingerprint.tilt}deg`,
    '--hue': `${fingerprint.hueShift}deg`,
  } as CSSProperties;

  return (
    <div
      className="relative aspect-video w-full overflow-hidden border-b border-fg-4/30 bg-[#0e0c09] text-bg-0"
      style={cssVars}
    >
      {/* Warm fireplace glow — anchored to a per-ticker corner. On hover the
          gradient scales slightly so the void feels alive without ever
          becoming a literal animation. */}
      <div
        aria-hidden
        className="absolute inset-0 transition-transform duration-[1200ms] ease-out group-hover:scale-[1.08]"
        style={{
          background:
            'radial-gradient(circle at var(--sx) var(--sy), hsl(var(--brand) / 0.62) 0%, hsl(var(--brand) / 0.22) 26%, hsl(var(--brand) / 0.06) 50%, transparent 74%)',
          filter: 'hue-rotate(var(--hue)) saturate(1.05)',
        }}
      />

      {/* Cinematic vignette — pulls the glow back into the frame so the edges
          stay deep ink and the ticker reads against contrast. */}
      <div
        aria-hidden
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(120% 100% at 50% 50%, transparent 38%, rgba(0,0,0,0.55) 100%)',
        }}
      />

      {/* Fractal noise grain — the single most "ảo diệu" detail; without it
          the gradient looks plastic. Mix-blend-overlay so it tints rather
          than dirties. */}
      <svg
        aria-hidden
        className="pointer-events-none absolute inset-0 h-full w-full opacity-[0.18] mix-blend-overlay"
      >
        <filter id={filterId}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.9"
            numOctaves="2"
            stitchTiles="stitch"
          />
          <feColorMatrix
            values="0 0 0 0 1  0 0 0 0 0.88  0 0 0 0 0.72  0 0 0 0.9 0"
          />
        </filter>
        <rect width="100%" height="100%" filter={`url(#${filterId})`} />
      </svg>

      {/* Top-left label cluster — tiny mono "MÃ CHỨNG KHOÁN" caption +
          italic serif sector. Anchors the poster as an editorial artifact
          rather than a placeholder. */}
      <div className="absolute left-4 top-3 z-10 max-w-[70%]">
        <span className="block font-mono text-[8.5px] font-semibold uppercase tracking-[0.28em] text-bg-0/55">
          mã chứng khoán
        </span>
        {sector && (
          <span className="mt-0.5 block truncate font-serif text-[10.5px] italic text-bg-0/45">
            {sector}
          </span>
        )}
      </div>

      {/* Top-right decorative glyph — per-ticker fingerprint. Brand-hot
          amber so it picks up the spotlight color. */}
      <span
        aria-hidden
        className="absolute right-4 top-3 z-10 select-none font-serif text-[13px] leading-none text-brand-hot/85"
      >
        {fingerprint.mark}
      </span>

      {/* Hairline under the labels — quietly divides "metadata strip" from
          the poster body. */}
      <span
        aria-hidden
        className="absolute left-4 right-4 top-[44px] h-px bg-bg-0/12"
      />

      {/* THE TICKER. Oversized italic display serif, intentionally bleeding
          off the bottom-right edge so each card looks like a cropped poster
          rather than a centered placeholder. leading is tight (0.84) so the
          glyph descenders land below the visible frame. */}
      <span
        className="pointer-events-none absolute -right-1 select-none font-display font-bold italic leading-[0.84] tracking-tighter text-bg-0 [font-size:clamp(3.5rem,9.5vw,5.75rem)]"
        style={{
          bottom: '-0.08em',
          transform: 'rotate(var(--tilt))',
          textShadow: '0 1px 0 rgba(0,0,0,0.35)',
        }}
      >
        {ticker}
      </span>

      {/* Hover sweep — slow vertical sheen passes left → right on hover.
          1200ms feels considered, not gimmicky. */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-bg-0/[0.06] to-transparent transition-transform duration-[1200ms] ease-out group-hover:translate-x-full"
      />
    </div>
  );
}

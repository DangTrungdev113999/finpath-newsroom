import { useMemo, useId, type ReactNode } from 'react';
import { formatCrawledAt } from '../lib/format';

/* djb2 — deterministic hash so SHB always lands in the same theme + variant
 * across sessions. Hash is also reused to seed sub-variants (rotation, dot
 * positions) so each theme has its own per-ticker fingerprint without
 * leaking out of the palette / composition. */
function hashStr(s: string): number {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

/* ---------------------------------------------------------------- *
 *  Shared atoms                                                     *
 * ---------------------------------------------------------------- */

function Grain({
  id,
  opacity = 0.16,
  baseFrequency = 0.9,
  tint = '1 1 1',
}: {
  id: string;
  opacity?: number;
  baseFrequency?: number;
  tint?: string;
}) {
  return (
    <svg
      aria-hidden
      className="pointer-events-none absolute inset-0 h-full w-full mix-blend-overlay"
      style={{ opacity }}
    >
      <filter id={id}>
        <feTurbulence
          type="fractalNoise"
          baseFrequency={baseFrequency}
          numOctaves="2"
          stitchTiles="stitch"
        />
        <feColorMatrix
          values={`0 0 0 0 ${tint.split(' ')[0]}  0 0 0 0 ${tint.split(' ')[1]}  0 0 0 0 ${tint.split(' ')[2]}  0 0 0 0.85 0`}
        />
      </filter>
      <rect width="100%" height="100%" filter={`url(#${id})`} />
    </svg>
  );
}

const TICKER_FONT =
  'pointer-events-none absolute inset-0 flex items-center justify-center font-display font-bold leading-none tracking-tight select-none [font-size:clamp(2.5rem,7vw,4.25rem)]';

interface ThemeProps {
  ticker: string;
  sector?: string;
  grainId: string;
  h: number;
  /** ISO string from manifest, used for the bottom <time> caption baked
   *  into each theme. Passed already-split for convenience. */
  crawledAt: string;
  stamp: { date: string; time: string };
}

/* ---------------------------------------------------------------- *
 *  1. Brasserie — deep bordeaux + gold double-rule + cream cursive  *
 * ---------------------------------------------------------------- */

function Brasserie({
  ticker,
  sector,
  grainId,
  crawledAt,
  stamp,
}: ThemeProps) {
  return (
    <>
      <div
        className="absolute inset-0"
        style={{
          background:
            'linear-gradient(178deg, #3a121a 0%, #2a0b12 55%, #18060a 100%)',
        }}
      />
      <Grain id={grainId} opacity={0.13} tint="0.95 0.85 0.7" />
      <div className="absolute inset-x-5 top-3 flex items-center justify-between">
        <span className="font-mono text-[8px] uppercase tracking-[0.3em] text-[#c9a861]/75">
          ★ Privée
        </span>
        {sector && (
          <span className="max-w-[55%] truncate font-serif text-[10px] italic text-[#c9a861]/60">
            {sector}
          </span>
        )}
      </div>
      <span className="absolute inset-x-5 top-[42px] h-px bg-[#c9a861]/45" />
      <span className="absolute inset-x-5 top-[45px] h-px bg-[#c9a861]/22" />
      <span className="absolute inset-x-5 bottom-[36px] h-px bg-[#c9a861]/22" />
      <span className="absolute inset-x-5 bottom-[33px] h-px bg-[#c9a861]/45" />
      <span className={`${TICKER_FONT} italic`} style={{ color: '#f4e7cf' }}>
        {ticker}
      </span>
      {/* Brass plaque — vintage wine-year sticker. Solid bordeaux fill,
          gold hairline ring, faint top highlight to read as embossed metal. */}
      <time
        dateTime={crawledAt}
        className="absolute bottom-3 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-md px-2.5 py-1 font-mono text-[10.5px] font-semibold uppercase tabular-nums tracking-[0.16em]"
        style={{
          backgroundColor: 'rgba(15, 4, 8, 0.7)',
          color: '#f4e7cf',
          boxShadow:
            'inset 0 0 0 1px rgba(201, 168, 97, 0.55), inset 0 1px 0 0 rgba(255, 240, 200, 0.12)',
        }}
      >
        {stamp.date} · {stamp.time}
      </time>
    </>
  );
}

/* ---------------------------------------------------------------- *
 *  2. Almanac — bone cream + horizontal rules + oxblood bold serif  *
 * ---------------------------------------------------------------- */

function Almanac({ ticker, sector, grainId, crawledAt, stamp }: ThemeProps) {
  return (
    <>
      <div
        className="absolute inset-0"
        style={{ background: 'linear-gradient(180deg, #ede2cd 0%, #e4d6bb 100%)' }}
      />
      <div
        aria-hidden
        className="absolute inset-0"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg, transparent 0px, transparent 14px, rgba(107, 26, 26, 0.085) 14px, rgba(107, 26, 26, 0.085) 15px)',
        }}
      />
      <Grain id={grainId} opacity={0.18} tint="0.4 0.25 0.18" />
      <div className="absolute inset-x-5 top-3 flex items-center justify-between">
        <span className="font-mono text-[8px] uppercase tracking-[0.32em] text-[#6b1a1a]/70">
          Vol · I
        </span>
        <span className="font-serif text-[10px] italic text-[#6b1a1a]/55">
          {sector ?? 'Finpath'}
        </span>
      </div>
      <span
        aria-hidden
        className="absolute left-1/2 top-[45px] -translate-x-1/2 font-serif text-[11px] tracking-[0.4em] text-[#6b1a1a]/45"
      >
        ▲ ◆ ▲
      </span>
      <span
        className={`${TICKER_FONT} italic`}
        style={{ color: '#6b1a1a' }}
      >
        {ticker}
      </span>
      {/* Ink rubber-stamp on bone paper — oxblood double-rule border, no
          fill so the ruled paper texture shows through. */}
      <time
        dateTime={crawledAt}
        className="absolute bottom-3 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-sm px-2.5 py-1 font-mono text-[10.5px] font-semibold uppercase tabular-nums tracking-[0.16em]"
        style={{
          backgroundColor: 'rgba(245, 235, 214, 0.92)',
          color: '#6b1a1a',
          boxShadow:
            'inset 0 0 0 1px rgba(107, 26, 26, 0.55), inset 0 0 0 3px rgba(245, 235, 214, 0.92), inset 0 0 0 4px rgba(107, 26, 26, 0.3)',
        }}
      >
        {stamp.date} · {stamp.time}
      </time>
    </>
  );
}

/* ---------------------------------------------------------------- *
 *  3. Observatory — deep navy + concentric circles + cyan accent    *
 * ---------------------------------------------------------------- */

function Observatory({ ticker, sector, grainId, h, crawledAt, stamp }: ThemeProps) {
  // Pseudo-random "stars" deterministic per-ticker hash
  const stars = useMemo(() => {
    const out: Array<{ x: number; y: number; r: number }> = [];
    let s = h | 1;
    for (let i = 0; i < 9; i++) {
      s = (s * 1103515245 + 12345) & 0x7fffffff;
      out.push({ x: (s % 100), y: ((s >> 8) % 100), r: 0.25 + ((s >> 16) % 5) / 10 });
    }
    return out;
  }, [h]);

  return (
    <>
      <div
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(120% 100% at 50% 50%, #1f3a55 0%, #0d1b2a 55%, #050b14 100%)',
        }}
      />
      <Grain id={grainId} opacity={0.12} tint="0.5 0.8 1" />
      <svg
        aria-hidden
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid meet"
        className="absolute inset-0 h-full w-full"
      >
        {[38, 30, 22, 14].map((r, i) => (
          <circle
            key={r}
            cx="50"
            cy="50"
            r={r}
            fill="none"
            stroke="#79c2d0"
            strokeOpacity={0.42 - i * 0.08}
            strokeWidth="0.25"
            strokeDasharray={i === 0 ? '0.6 0.8' : undefined}
          />
        ))}
        {stars.map((s, i) => (
          <circle key={i} cx={s.x} cy={s.y} r={s.r} fill="#ece4d6" opacity="0.55" />
        ))}
      </svg>
      <div className="absolute inset-x-5 top-3 z-10 flex items-center justify-between">
        <span className="font-mono text-[8px] uppercase tracking-[0.3em] text-[#79c2d0]/70">
          α · Stella
        </span>
        {sector && (
          <span className="max-w-[55%] truncate font-serif text-[10px] italic text-[#79c2d0]/55">
            {sector}
          </span>
        )}
      </div>
      <span
        className={`${TICKER_FONT} italic z-10`}
        style={{
          color: '#ece4d6',
          textShadow: '0 0 18px rgba(121, 194, 208, 0.45)',
        }}
      >
        {ticker}
      </span>
      {/* Signal token — frosted deep-navy chip, cyan rim with soft glow
          like an instrument readout in low light. */}
      <time
        dateTime={crawledAt}
        className="absolute bottom-3 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-md px-2.5 py-1 font-mono text-[10.5px] font-semibold uppercase tabular-nums tracking-[0.16em]"
        style={{
          backgroundColor: 'rgba(8, 18, 32, 0.7)',
          color: '#cdeef5',
          boxShadow:
            'inset 0 0 0 1px rgba(121, 194, 208, 0.55), 0 0 14px -2px rgba(121, 194, 208, 0.35)',
          backdropFilter: 'blur(3px)',
        }}
      >
        {stamp.date} · {stamp.time}
      </time>
    </>
  );
}

/* ---------------------------------------------------------------- *
 *  4. Saigon Dusk — terracotta + warm cream + leaf silhouette       *
 * ---------------------------------------------------------------- */

function SaigonDusk({ ticker, sector, grainId, crawledAt, stamp }: ThemeProps) {
  return (
    <>
      <div
        className="absolute inset-0"
        style={{
          background:
            'linear-gradient(135deg, #d68548 0%, #b56535 50%, #6e3a1f 100%)',
        }}
      />
      <Grain id={grainId} opacity={0.18} tint="0.95 0.85 0.65" />
      {/* sun arc — top-right glow */}
      <div
        aria-hidden
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(45% 40% at 85% 18%, rgba(255, 232, 188, 0.55) 0%, rgba(255, 200, 140, 0.2) 30%, transparent 60%)',
        }}
      />
      {/* palm leaf silhouettes bottom corners */}
      <svg
        aria-hidden
        viewBox="0 0 100 60"
        preserveAspectRatio="xMidYMax slice"
        className="absolute inset-x-0 bottom-0 h-2/5 w-full"
      >
        <path
          d="M -2 60 Q 8 35 16 30 Q 12 42 18 60 Z"
          fill="#3d1f10"
          opacity="0.55"
        />
        <path
          d="M 102 60 Q 88 32 78 26 Q 84 40 80 60 Z"
          fill="#3d1f10"
          opacity="0.45"
        />
      </svg>
      <div className="absolute inset-x-5 top-3 z-10 flex items-center justify-between">
        <span className="font-mono text-[8px] uppercase tracking-[0.3em] text-[#f4e2c4]/85">
          Saigon · 19h
        </span>
        {sector && (
          <span className="max-w-[55%] truncate font-serif text-[10px] italic text-[#f4e2c4]/65">
            {sector}
          </span>
        )}
      </div>
      <span
        className={`${TICKER_FONT} italic z-10`}
        style={{
          color: '#f5e4c5',
          textShadow: '0 1px 0 rgba(60, 22, 8, 0.35)',
        }}
      >
        {ticker}
      </span>
      {/* Lacquer plaque — deep terracotta solid + warm-cream hairline rim.
          Reads like a hand-painted signboard. */}
      <time
        dateTime={crawledAt}
        className="absolute bottom-3 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-md px-2.5 py-1 font-mono text-[10.5px] font-semibold uppercase tabular-nums tracking-[0.16em]"
        style={{
          backgroundColor: 'rgba(50, 18, 6, 0.75)',
          color: '#fef3da',
          boxShadow:
            'inset 0 0 0 1px rgba(244, 226, 196, 0.6), inset 0 1px 0 0 rgba(255, 232, 188, 0.18)',
        }}
      >
        {stamp.date} · {stamp.time}
      </time>
    </>
  );
}

/* ---------------------------------------------------------------- *
 *  5. Numismatic — antique gold + dotted coin border + brown serif  *
 * ---------------------------------------------------------------- */

function Numismatic({ ticker, sector, grainId, crawledAt, stamp }: ThemeProps) {
  // Coin edge — 48 evenly spaced dots around an ellipse
  const dots = useMemo(() => {
    const out: Array<{ x: number; y: number }> = [];
    for (let i = 0; i < 56; i++) {
      const θ = (i / 56) * Math.PI * 2;
      out.push({
        x: 50 + Math.cos(θ) * 46,
        y: 50 + Math.sin(θ) * 40,
      });
    }
    return out;
  }, []);

  return (
    <>
      <div
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(140% 110% at 50% 35%, #d9b86c 0%, #b5934a 40%, #6e5224 100%)',
        }}
      />
      <Grain id={grainId} opacity={0.2} tint="0.55 0.4 0.18" />
      <svg
        aria-hidden
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        className="absolute inset-0 h-full w-full"
      >
        {dots.map((d, i) => (
          <circle key={i} cx={d.x} cy={d.y} r="0.45" fill="#3d2817" opacity="0.65" />
        ))}
        <ellipse
          cx="50"
          cy="50"
          rx="42"
          ry="36"
          fill="none"
          stroke="#3d2817"
          strokeOpacity="0.35"
          strokeWidth="0.25"
        />
      </svg>
      <div className="absolute inset-x-5 top-3 z-10 flex items-center justify-between">
        <span className="font-mono text-[8px] uppercase tracking-[0.34em] text-[#3d2817]/75">
          ▲ Finpath
        </span>
        {sector && (
          <span className="max-w-[55%] truncate font-serif text-[10px] italic text-[#3d2817]/65">
            {sector}
          </span>
        )}
      </div>
      <span
        className={`${TICKER_FONT} z-10`}
        style={{
          color: '#2a1808',
          textShadow: '0 1px 0 rgba(255, 235, 180, 0.45)',
        }}
      >
        {ticker}
      </span>
      {/* Numismatic medal — deep brown plaque with double gold rim, the
          way a coin's inscription band sits inside the milled edge. */}
      <time
        dateTime={crawledAt}
        className="absolute bottom-3 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-md px-2.5 py-1 font-mono text-[10.5px] font-semibold uppercase tabular-nums tracking-[0.16em]"
        style={{
          backgroundColor: '#2a1808',
          color: '#f5dfa0',
          boxShadow:
            'inset 0 0 0 1px rgba(217, 184, 108, 0.85), inset 0 0 0 2px rgba(42, 24, 8, 1), inset 0 0 0 3px rgba(217, 184, 108, 0.4)',
        }}
      >
        {stamp.date} · {stamp.time}
      </time>
    </>
  );
}

/* ---------------------------------------------------------------- *
 *  6. Blueprint — cobalt + white grid + chalky white slab serif     *
 * ---------------------------------------------------------------- */

function Blueprint({ ticker, sector, grainId, crawledAt, stamp }: ThemeProps) {
  return (
    <>
      <div
        className="absolute inset-0"
        style={{
          background:
            'linear-gradient(160deg, #1c3d6e 0%, #133057 55%, #0a1d3a 100%)',
        }}
      />
      {/* engineering grid */}
      <div
        aria-hidden
        className="absolute inset-0"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg, transparent 0px, transparent 18px, rgba(220, 235, 255, 0.07) 18px, rgba(220, 235, 255, 0.07) 19px), repeating-linear-gradient(90deg, transparent 0px, transparent 18px, rgba(220, 235, 255, 0.07) 18px, rgba(220, 235, 255, 0.07) 19px)',
        }}
      />
      <Grain id={grainId} opacity={0.1} tint="0.85 0.92 1" />
      {/* corner tick marks */}
      {[
        'left-4 top-4',
        'right-4 top-4',
        'left-4 bottom-4',
        'right-4 bottom-4',
      ].map((pos) => (
        <span
          key={pos}
          aria-hidden
          className={`absolute ${pos} h-2 w-2 border border-[#9fc7ff]/55`}
        />
      ))}
      <div className="absolute inset-x-9 top-3 z-10 flex items-center justify-between">
        <span className="font-mono text-[8px] uppercase tracking-[0.3em] text-[#9fc7ff]/80">
          REV-A · 2026
        </span>
        {sector && (
          <span className="max-w-[55%] truncate font-mono text-[8.5px] uppercase tracking-[0.18em] text-[#9fc7ff]/55">
            {sector}
          </span>
        )}
      </div>
      <span
        className={`${TICKER_FONT} z-10`}
        style={{ color: '#e6f0ff', letterSpacing: '0.02em' }}
      >
        {ticker}
      </span>
      {/* Drawing-notation block — cobalt fill with sharp chalk-white tick
          border. Square corners on purpose; this is engineering, not jewelry. */}
      <time
        dateTime={crawledAt}
        className="absolute bottom-3 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-none px-2.5 py-1 font-mono text-[10.5px] font-semibold uppercase tabular-nums tracking-[0.16em]"
        style={{
          backgroundColor: 'rgba(7, 19, 40, 0.78)',
          color: '#eef3ff',
          boxShadow:
            'inset 0 0 0 1px rgba(159, 199, 255, 0.7), inset 0 0 0 4px rgba(7, 19, 40, 0)',
        }}
      >
        {stamp.date} · {stamp.time}
      </time>
    </>
  );
}

/* ---------------------------------------------------------------- *
 *  7. Atelier — warm sepia + radiating engraved fan + ink serif     *
 * ---------------------------------------------------------------- */

function Atelier({ ticker, sector, grainId, crawledAt, stamp }: ThemeProps) {
  // 21 fan rays from bottom-center outward
  const rays = useMemo(
    () =>
      Array.from({ length: 21 }, (_, i) => {
        const angle = -90 + (i - 10) * 5; // -130° to -40° (top half)
        return angle;
      }),
    [],
  );

  return (
    <>
      <div
        className="absolute inset-0"
        style={{ background: 'linear-gradient(180deg, #f5ebd6 0%, #e8d9b8 100%)' }}
      />
      <svg
        aria-hidden
        viewBox="0 0 100 60"
        preserveAspectRatio="xMidYMax slice"
        className="absolute inset-x-0 bottom-0 h-full w-full"
      >
        <g transform="translate(50 60)">
          {rays.map((a) => (
            <line
              key={a}
              x1="0"
              y1="0"
              x2={Math.cos((a * Math.PI) / 180) * 80}
              y2={Math.sin((a * Math.PI) / 180) * 80}
              stroke="#3a2618"
              strokeOpacity="0.13"
              strokeWidth="0.18"
            />
          ))}
        </g>
      </svg>
      <Grain id={grainId} opacity={0.22} tint="0.35 0.22 0.12" />
      <div className="absolute inset-x-5 top-3 z-10 flex items-center justify-between">
        <span className="font-serif text-[10px] italic text-[#3a2618]/70">
          Atelier · Finpath
        </span>
        {sector && (
          <span className="font-mono text-[8px] uppercase tracking-[0.3em] text-[#3a2618]/55">
            {sector}
          </span>
        )}
      </div>
      <span
        className={`${TICKER_FONT} z-10`}
        style={{
          color: '#1d130a',
          textShadow: '0 1px 0 rgba(255, 235, 200, 0.5)',
        }}
      >
        {ticker}
      </span>
      {/* Letterpress impression — sepia card pressed into paper, ink edge
          deeper than the body. Inset bottom shadow simulates the indent. */}
      <time
        dateTime={crawledAt}
        className="absolute bottom-3 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap rounded-sm px-2.5 py-1 font-mono text-[10.5px] font-semibold uppercase tabular-nums tracking-[0.16em]"
        style={{
          backgroundColor: 'rgba(232, 217, 184, 0.95)',
          color: '#1d130a',
          boxShadow:
            'inset 0 0 0 1px rgba(58, 38, 24, 0.55), 0 1px 0 0 rgba(58, 38, 24, 0.18), inset 0 1px 0 0 rgba(255, 248, 224, 0.5)',
        }}
      >
        {stamp.date} · {stamp.time}
      </time>
    </>
  );
}

/* ---------------------------------------------------------------- *
 *  Theme registry                                                   *
 * ---------------------------------------------------------------- */

type ThemeRender = (props: ThemeProps) => ReactNode;

const THEMES: ThemeRender[] = [
  Brasserie,
  Almanac,
  Observatory,
  SaigonDusk,
  Numismatic,
  Blueprint,
  Atelier,
];

/**
 * Hero slot for ArticleCard when no Imagen thumb exists. Instead of one
 * generic placeholder, we draw the ticker as a miniature editorial poster
 * cycling through 7 distinct themes (palette + composition + typography all
 * differ). A ticker hashes to exactly one theme so SHB always reads as
 * "Foundry-style SHB", VHM always as "Almanac VHM", etc.
 *
 * Themes
 *   1. Brasserie   — bordeaux + gold double rule + cream cursive
 *   2. Almanac     — bone cream + ruled paper + oxblood bold italic
 *   3. Observatory — deep navy + concentric circles + cyan-lit serif
 *   4. Saigon Dusk — terracotta + sun arc + tropical leaf silhouettes
 *   5. Numismatic  — antique gold coin edge + brown roman serif
 *   6. Blueprint   — cobalt + engineering grid + corner ticks + chalky text
 *   7. Atelier     — sepia + radiating engraved fan + heavy ink serif
 *
 * The hero is purely decorative — actual click target + accessibility text
 * are owned by the parent ArticleCard.
 */
export function TickerHero({
  ticker,
  sector,
  crawledAt,
}: {
  ticker: string;
  sector?: string;
  /** ISO timestamp from manifest. Each theme bakes the formatted date+time
   *  into its own bottom caption slot using theme-specific typography. */
  crawledAt: string;
}) {
  const grainId = useId();
  const h = useMemo(() => hashStr(ticker || 'XXX'), [ticker]);
  const Theme = THEMES[h % THEMES.length];
  const safeTicker = ticker || '—';
  const stamp = useMemo(() => {
    const formatted = formatCrawledAt(crawledAt);
    const [date, time] = formatted.split(' ');
    return { date: date || '', time: time || '' };
  }, [crawledAt]);

  return (
    <div className="relative aspect-video w-full overflow-hidden border-b border-fg-4/30">
      <Theme
        ticker={safeTicker}
        sector={sector}
        grainId={grainId}
        h={h}
        crawledAt={crawledAt}
        stamp={stamp}
      />
      {/* Universal hover sheen — same across all themes so cards share an
          interaction signature even though the surface art diverges. */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/[0.07] to-transparent transition-transform duration-[1100ms] ease-out group-hover:translate-x-full"
      />
    </div>
  );
}

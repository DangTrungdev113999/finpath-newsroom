import { cn } from '../shared/lib/cn';

/**
 * 4-bar voice equalizer — live "audio đang phát" indicator.
 * Each bar uses global `eqBar` keyframe (scaleY 0.28 ↔ 1) with staggered
 * animation-delay → wave illusion. Active=false giữ bars ở pose tĩnh.
 *
 * `size` mặc định 16px (h-4 w-4). Truyền 'sm' (12px) cho pill nhỏ.
 * `color` default 'brand' — đổi 'currentColor' để inherit từ parent text color.
 */

interface Props {
  active: boolean;
  size?: 'sm' | 'md';
  color?: 'brand' | 'current';
  className?: string;
}

const HEIGHTS = ['65%', '95%', '75%', '55%'];
const DELAYS = ['0ms', '120ms', '240ms', '360ms'];

export function EqualizerBars({
  active,
  size = 'md',
  color = 'brand',
  className,
}: Props) {
  const wrap = size === 'sm' ? 'h-3 w-3 gap-[1.5px]' : 'h-4 w-4 gap-[2px]';
  const barW = size === 'sm' ? 'w-[1.5px]' : 'w-[2px]';
  const barBg = color === 'brand' ? 'bg-brand' : 'bg-current';

  return (
    <span
      className={cn(
        'inline-flex shrink-0 items-end justify-center',
        wrap,
        className,
      )}
      aria-hidden
    >
      {HEIGHTS.map((h, i) => (
        <span
          key={i}
          className={cn('block rounded-[1px]', barW, barBg)}
          style={{
            height: h,
            transformOrigin: 'bottom',
            animation: active
              ? `eqBar 850ms ${DELAYS[i]} ease-in-out infinite`
              : undefined,
          }}
        />
      ))}
    </span>
  );
}

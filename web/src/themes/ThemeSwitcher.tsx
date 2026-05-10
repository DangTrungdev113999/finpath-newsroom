/* ═══════════════════════════════════════════════════════════════════════════
 * <ThemeSwitcher>
 *
 *   Sidebar-footer-sized dropdown. VSCode-style theme picker:
 *     • On open — auto-scroll to active item
 *     • Arrow keys — live preview (swaps theme as you navigate)
 *     • Enter — commit selection
 *     • Esc / click outside — revert to original theme
 *     • Active item visually prominent (brand tint + accent bar)
 *     • Footer hint row shows keyboard controls
 *
 *   During the first paint before `next-themes` hydrated, `theme` is
 *   `undefined`; `getTheme(undefined)` falls back to the default (Salon).
 * ═══════════════════════════════════════════════════════════════════════════ */

import { useTheme } from "next-themes";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowDown,
  ArrowUp,
  Check,
  ChevronsUpDown,
  CornerDownLeft,
  Palette as PaletteIcon,
  Search,
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "../shared/ui/dropdown-menu";
import { cn } from "../shared/lib/cn";
import { matchesTokens } from "../shared/lib/normalize";
import { THEMES, getTheme } from "./registry";

function SwatchTrio({
  swatches,
  size = "sm",
}: {
  swatches: readonly [string, string, string];
  size?: "sm" | "md";
}) {
  const dot = size === "md" ? "h-3 w-3" : "h-2.5 w-2.5";
  return (
    <span className="flex items-center gap-0.5 shrink-0" aria-hidden>
      {swatches.map((c, i) => (
        <span
          key={i}
          className={cn(
            dot,
            "rounded-pill shadow-[inset_0_0_0_1px_rgb(0_0_0_/_0.08)]",
          )}
          style={{ backgroundColor: c }}
        />
      ))}
    </span>
  );
}

/**
 * Keycap — tactile mechanical-keyboard chip.
 *
 *   bg-bg-0 sits below the popup (bg-bg-1) on every theme, so the chip
 *   always separates from its container regardless of light/dark mood.
 *   The layered shadow simulates a keycap: a hairline top highlight
 *   (1px inset rgba-white) gives the bevel; a 1px bottom edge (rgba-black)
 *   grounds it. The same recipe reads as refined on parchment and as
 *   mechanical on obsidian.
 */
function Keycap({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex h-[18px] min-w-[18px] items-center justify-center",
        "rounded-[4px] px-1",
        "bg-bg-0 text-fg-1",
        "border border-fg-4/70",
        "shadow-[inset_0_1px_0_rgb(255_255_255_/_0.08),0_1px_0_rgb(0_0_0_/_0.12)]",
        className,
      )}
    >
      {children}
    </span>
  );
}

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();
  const active = getTheme(theme);

  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const searchRef = useRef<HTMLInputElement>(null);

  // Snapshot the theme when the menu opens so we can revert on cancel.
  const originalRef = useRef<string | undefined>(undefined);
  const committedRef = useRef(false);

  const filtered = useMemo(() => {
    if (query.trim().length === 0) return THEMES;
    return THEMES.filter((t) =>
      matchesTokens(`${t.label} ${t.description} ${t.id}`, query),
    );
  }, [query]);

  // Scroll the active item into view once the menu opens.
  const listRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open) return;
    setQuery("");
    // Wait a frame so the content is mounted + measured.
    const id = requestAnimationFrame(() => {
      const el = listRef.current?.querySelector<HTMLElement>(
        '[data-active="true"]',
      );
      el?.scrollIntoView({ block: "center" });
      searchRef.current?.focus();
    });
    return () => cancelAnimationFrame(id);
  }, [open]);

  const handleOpenChange = (next: boolean) => {
    if (next) {
      originalRef.current = theme;
      committedRef.current = false;
    } else if (!committedRef.current && originalRef.current) {
      // Revert to snapshot — user bailed out (Esc / click-outside).
      setTheme(originalRef.current);
    }
    setOpen(next);
  };

  return (
    <DropdownMenu open={open} onOpenChange={handleOpenChange}>
      <DropdownMenuTrigger
        className={cn(
          "group flex h-7 w-full items-center gap-2 rounded-pill px-3",
          "border border-fg-4/40 bg-bg-2/60 text-fg-2",
          "hover:border-fg-4/70 hover:bg-bg-2 hover:text-fg-0",
          "transition-[background-color,border-color,color] duration-med ease-out-quart",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35",
          "data-[state=open]:border-fg-4/70 data-[state=open]:bg-bg-2 data-[state=open]:text-fg-0",
        )}
        aria-label="Đổi giao diện"
      >
        <PaletteIcon className="h-3.5 w-3.5 shrink-0" strokeWidth={1.75} />
        <span className="flex-1 truncate text-left font-sans text-xs">
          {active.label}
        </span>
        <SwatchTrio swatches={active.swatches} />
        <ChevronsUpDown className="h-3 w-3 shrink-0 text-fg-3 group-hover:text-fg-1" />
      </DropdownMenuTrigger>
      <DropdownMenuContent
        side="top"
        align="start"
        className="w-72 p-0"
      >
        <DropdownMenuLabel className="px-2.5 pb-1 pt-2 text-fg-2">
          Giao diện
        </DropdownMenuLabel>
        {/* Prominent shortcut strip pinned at top */}
        <div
          role="note"
          aria-label="Phím tắt"
          className={cn(
            "mx-2 mb-1.5 flex items-center justify-between gap-2 rounded-md",
            "border border-brand/25 bg-brand/[0.06] px-2 py-1.5",
            "font-sans text-[10px] text-fg-1",
          )}
        >
          <span className="flex items-center gap-1">
            <span className="flex items-center gap-0.5">
              <Keycap>
                <ArrowUp className="h-2.5 w-2.5" strokeWidth={2.5} />
              </Keycap>
              <Keycap>
                <ArrowDown className="h-2.5 w-2.5" strokeWidth={2.5} />
              </Keycap>
            </span>
            <span>xem trước</span>
          </span>
          <span className="flex items-center gap-1">
            <Keycap>
              <CornerDownLeft className="h-2.5 w-2.5" strokeWidth={2.5} />
            </Keycap>
            <span>chọn</span>
          </span>
          <span className="flex items-center gap-1">
            <Keycap className="px-1.5 font-mono text-[9px] tracking-[0.02em]">
              Esc
            </Keycap>
            <span>huỷ</span>
          </span>
        </div>
        {/* Search */}
        <label
          className={cn(
            "mx-2 mb-1.5 flex h-7 items-center gap-1.5 rounded-md bg-bg-0 px-2",
            "shadow-[inset_0_0_0_1px_hsl(var(--fg-4)/0.55)]",
            "focus-within:shadow-[inset_0_0_0_1.5px_hsl(var(--focus-ring))]",
            "transition-shadow duration-fast ease-out-quart",
          )}
        >
          <Search
            className="h-3 w-3 shrink-0 text-fg-3"
            strokeWidth={1.75}
            aria-hidden
          />
          <input
            ref={searchRef}
            value={query}
            onChange={(e) => setQuery(e.currentTarget.value)}
            onKeyDown={(e) => {
              if (e.key.length === 1 || e.key === "Backspace") {
                e.stopPropagation();
              }
              if (e.key === "ArrowDown") {
                e.preventDefault();
                const first = listRef.current?.querySelector<HTMLElement>(
                  '[role="menuitem"]',
                );
                first?.focus();
              }
            }}
            placeholder="Tìm giao diện…"
            className={cn(
              "flex-1 bg-transparent font-sans text-xs text-fg-0",
              "placeholder:text-fg-3 outline-none",
            )}
            aria-label="Tìm giao diện"
            spellCheck={false}
          />
        </label>
        <div ref={listRef} className="max-h-64 overflow-y-auto px-0.5 pb-1">
          {filtered.length === 0 ? (
            <div className="px-2 py-3 text-center font-mono text-[10px] text-fg-3">
              Không có giao diện khớp
            </div>
          ) : null}
          {filtered.map((t) => {
            const selected = t.id === active.id;
            return (
              <DropdownMenuItem
                key={t.id}
                data-active={selected ? "true" : undefined}
                onFocus={() => {
                  // VSCode-style live preview on keyboard navigation.
                  if (t.id !== theme) setTheme(t.id);
                }}
                onPointerEnter={(e) => {
                  // Mirror hover preview for mouse users (Radix already moves
                  // focus to pointer target; onFocus handles it — but guard
                  // defensively in case of focus-trap weirdness).
                  if (t.id !== theme) setTheme(t.id);
                  e.currentTarget.focus();
                }}
                onSelect={() => {
                  // Commit (Enter or click). setTheme already applied by
                  // focus/pointer preview; just mark committed and close.
                  committedRef.current = true;
                  setTheme(t.id);
                }}
                className={cn(
                  "relative h-auto items-start gap-2.5 py-1.5 pl-3 pr-2",
                  "data-[active=true]:bg-brand/10 data-[active=true]:text-fg-0",
                )}
              >
                {selected && (
                  <span
                    aria-hidden
                    className="pointer-events-none absolute inset-y-1 left-0 w-[2px] rounded-r-full bg-brand"
                  />
                )}
                <span className="mt-0.5">
                  <SwatchTrio swatches={t.swatches} size="md" />
                </span>
                <span className="flex min-w-0 flex-col gap-0.5">
                  <span
                    className={cn(
                      "truncate font-sans text-xs",
                      selected
                        ? "font-semibold text-fg-0"
                        : "font-medium text-fg-1",
                    )}
                  >
                    {t.label}
                  </span>
                  <span className="truncate font-sans text-[10px] text-fg-3">
                    {t.description}
                  </span>
                </span>
                {selected && (
                  <Check
                    className="ml-auto mt-1 h-3.5 w-3.5 shrink-0 text-brand"
                    strokeWidth={2.75}
                  />
                )}
              </DropdownMenuItem>
            );
          })}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

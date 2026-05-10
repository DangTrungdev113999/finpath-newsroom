/* ═══════════════════════════════════════════════════════════════════════════
 * THEME REGISTRY
 *
 *   Single source of truth for every dashboard theme. The switcher, the
 *   ThemeProvider, and the Monaco theme resolver all read this list — adding
 *   a new entry here (plus the matching `<id>.css` and monaco palettes) is
 *   all that's needed to make a new theme selectable end-to-end.
 *
 *   `monaco.light` / `monaco.dark` point at theme IDs registered in
 *   `./monaco.ts`. Each dashboard theme ships both surfaces because some
 *   editors (JsonEditor) run on a light Monaco surface while others
 *   (Prompt*, FileViewer) deliberately run dark even on a light dashboard.
 * ═══════════════════════════════════════════════════════════════════════════ */

export type ThemeId =
  | "salon"
  | "airbnb"
  | "apple"
  | "binance"
  | "claude"
  | "cursor"
  | "figma"
  | "framer"
  | "linear"
  | "meta"
  | "mintlify"
  | "nike"
  | "notion"
  | "nvidia"
  | "playstation"
  | "raycast"
  | "resend"
  | "sanity"
  | "sentry"
  | "shopify"
  | "spotify"
  | "stripe"
  | "superhuman"
  | "supabase"
  | "tesla"
  | "uber"
  | "vercel";

export type ThemeMeta = {
  id: ThemeId;
  /** Display name in the switcher. */
  label: string;
  /** One-line tagline shown below the label in the menu. */
  description: string;
  /** Reserved for future dark themes; currently all entries are "light". */
  mood: "light" | "dark";
  /** Preview trio — background, brand, foreground (in this order). */
  swatches: readonly [string, string, string];
  /** Monaco theme IDs registered by `defineReelThemes` in `./monaco.ts`. */
  monaco: {
    light: string;
    dark: string;
  };
};

export const THEMES: readonly ThemeMeta[] = [
  {
    id: "salon",
    label: "Salon",
    description: "Parchment & terracotta — Anthropic inspired",
    mood: "light",
    swatches: ["#f5f4ed", "#c96442", "#141413"],
    monaco: { light: "reel-salon-light", dark: "reel-salon-dark" },
  },
  {
    id: "airbnb",
    label: "Airbnb",
    description: "Chợ du lịch — coral đỏ ấm, ảnh chụp làm chủ đạo",
    mood: "light",
    swatches: ["#ffffff", "#ff385c", "#222222"],
    monaco: { light: "reel-airbnb-light", dark: "reel-airbnb-dark" },
  },
  {
    id: "apple",
    label: "Apple",
    description: "Minimal white, SF Pro, blue accent",
    mood: "light",
    swatches: ["#f5f5f7", "#0071e3", "#1d1d1f"],
    monaco: { light: "reel-apple-light", dark: "reel-apple-dark" },
  },
  {
    id: "binance",
    label: "Binance",
    description: "Sàn crypto — vàng rực trên nền monochrome",
    mood: "dark",
    swatches: ["#222126", "#F0B90B", "#fafafa"],
    monaco: { light: "reel-binance-light", dark: "reel-binance-dark" },
  },
  {
    id: "claude",
    label: "Claude",
    description: "Warm parchment, terracotta, editorial serif",
    mood: "light",
    swatches: ["#f5f4ed", "#c96442", "#141413"],
    monaco: { light: "reel-claude-light", dark: "reel-claude-dark" },
  },
  {
    id: "cursor",
    label: "Cursor",
    description: "Warm cream with urgent orange accent",
    mood: "light",
    swatches: ["#f2f1ed", "#f54e00", "#26251e"],
    monaco: { light: "reel-cursor-light", dark: "reel-cursor-dark" },
  },
  {
    id: "figma",
    label: "Figma",
    description: "Black & white gallery with vibrant purple accent",
    mood: "light",
    swatches: ["#ffffff", "#6d4dea", "#000000"],
    monaco: { light: "reel-figma-light", dark: "reel-figma-dark" },
  },
  {
    id: "framer",
    label: "Framer",
    description: "Website builder — đen tuyền với xanh Framer, chuyển động",
    mood: "dark",
    swatches: ["#000000", "#0099ff", "#ffffff"],
    monaco: { light: "reel-framer-light", dark: "reel-framer-dark" },
  },
  {
    id: "linear",
    label: "Linear",
    description: "Ultra-minimal dark, indigo-violet accent",
    mood: "dark",
    swatches: ["#08090a", "#5e6ad2", "#f7f8f8"],
    monaco: { light: "reel-linear-light", dark: "reel-linear-dark" },
  },
  {
    id: "meta",
    label: "Meta",
    description: "Tech retail — ảnh làm chủ, Meta Blue CTA",
    mood: "light",
    swatches: ["#ffffff", "#0064E0", "#1C2B33"],
    monaco: { light: "reel-meta-light", dark: "reel-meta-dark" },
  },
  {
    id: "mintlify",
    label: "Mintlify",
    description: "Tài liệu sạch, nhấn xanh mint, tối ưu đọc",
    mood: "light",
    swatches: ["#ffffff", "#18E299", "#0d0d0d"],
    monaco: { light: "reel-mintlify-light", dark: "reel-mintlify-dark" },
  },
  {
    id: "nike",
    label: "Nike",
    description: "Thể thao — monochrome, chữ hoa khổng lồ",
    mood: "light",
    swatches: ["#ffffff", "#111111", "#111111"],
    monaco: { light: "reel-nike-light", dark: "reel-nike-dark" },
  },
  {
    id: "notion",
    label: "Notion",
    description: "Warm white pages, serif headings, blue CTA",
    mood: "light",
    swatches: ["#f6f5f4", "#0075de", "#141413"],
    monaco: { light: "reel-notion-light", dark: "reel-notion-dark" },
  },
  {
    id: "nvidia",
    label: "Nvidia",
    description: "Sức mạnh GPU — đen và xanh neon năng lượng",
    mood: "dark",
    swatches: ["#000000", "#76b900", "#ffffff"],
    monaco: { light: "reel-nvidia-light", dark: "reel-nvidia-dark" },
  },
  {
    id: "playstation",
    label: "PlayStation",
    description: "Console game — đen/trắng/xám với xanh cyan hover",
    mood: "dark",
    swatches: ["#000000", "#0070cc", "#ffffff"],
    monaco: {
      light: "reel-playstation-light",
      dark: "reel-playstation-dark",
    },
  },
  {
    id: "raycast",
    label: "Raycast",
    description: "Near-black chrome with punctuation red",
    mood: "dark",
    swatches: ["#07080a", "#ff6363", "#f9f9f9"],
    monaco: { light: "reel-raycast-light", dark: "reel-raycast-dark" },
  },
  {
    id: "resend",
    label: "Resend",
    description: "API email — tối giản, frost border, mono accent",
    mood: "dark",
    swatches: ["#000000", "#ffffff", "#f0f0f0"],
    monaco: { light: "reel-resend-light", dark: "reel-resend-dark" },
  },
  {
    id: "sanity",
    label: "Sanity",
    description: "CMS — coral đỏ ấm, editorial content-first",
    mood: "dark",
    swatches: ["#0b0b0b", "#f36458", "#ffffff"],
    monaco: { light: "reel-sanity-light", dark: "reel-sanity-dark" },
  },
  {
    id: "sentry",
    label: "Sentry",
    description: "Giám sát lỗi — tím đậm, lavender và lime accent",
    mood: "dark",
    swatches: ["#1f1633", "#6a5fc1", "#ffffff"],
    monaco: { light: "reel-sentry-light", dark: "reel-sentry-dark" },
  },
  {
    id: "shopify",
    label: "Shopify",
    description: "Thương mại — đen điện ảnh với neon green",
    mood: "dark",
    swatches: ["#000000", "#36F4A4", "#ffffff"],
    monaco: { light: "reel-shopify-light", dark: "reel-shopify-dark" },
  },
  {
    id: "spotify",
    label: "Spotify",
    description: "Immersive dark, bold Spotify green",
    mood: "dark",
    swatches: ["#121212", "#1ed760", "#ffffff"],
    monaco: { light: "reel-spotify-light", dark: "reel-spotify-dark" },
  },
  {
    id: "stripe",
    label: "Stripe",
    description: "Signature purple on white, navy headings",
    mood: "light",
    swatches: ["#ffffff", "#533afd", "#061b31"],
    monaco: { light: "reel-stripe-light", dark: "reel-stripe-dark" },
  },
  {
    id: "superhuman",
    label: "Superhuman",
    description: "Email cao cấp — tím Amethyst, cream ấm, keyboard-first",
    mood: "light",
    swatches: ["#ffffff", "#714cb6", "#292827"],
    monaco: {
      light: "reel-superhuman-light",
      dark: "reel-superhuman-dark",
    },
  },
  {
    id: "supabase",
    label: "Supabase",
    description: "Dark-mode emerald, border-driven depth",
    mood: "dark",
    swatches: ["#171717", "#3ecf8e", "#fafafa"],
    monaco: { light: "reel-supabase-light", dark: "reel-supabase-dark" },
  },
  {
    id: "tesla",
    label: "Tesla",
    description: "Xe điện — trắng tinh, ảnh full viewport, tối giản triệt để",
    mood: "light",
    swatches: ["#ffffff", "#3E6AE1", "#171A20"],
    monaco: { light: "reel-tesla-light", dark: "reel-tesla-dark" },
  },
  {
    id: "uber",
    label: "Uber",
    description: "Di chuyển — đen trắng mạnh, chữ chặt, đô thị",
    mood: "light",
    swatches: ["#ffffff", "#000000", "#000000"],
    monaco: { light: "reel-uber-light", dark: "reel-uber-dark" },
  },
  {
    id: "vercel",
    label: "Vercel",
    description: "Achromatic precision, Geist-style geometry",
    mood: "light",
    swatches: ["#ffffff", "#171717", "#0a72ef"],
    monaco: { light: "reel-vercel-light", dark: "reel-vercel-dark" },
  },
] as const;

export const THEME_IDS: readonly ThemeId[] = THEMES.map((t) => t.id);
export const DEFAULT_THEME: ThemeId = "salon";

/**
 * Resolve a theme by id, with a safe fallback to the default.
 *
 * Handles the first-paint case where `useTheme()` returns `undefined` before
 * hydration completes, plus any stale localStorage value for a theme that
 * has since been removed from the registry.
 */
export function getTheme(id: string | undefined | null): ThemeMeta {
  if (!id) return THEMES[0];
  return THEMES.find((t) => t.id === id) ?? THEMES[0];
}

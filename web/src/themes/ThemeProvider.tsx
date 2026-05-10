/* ═══════════════════════════════════════════════════════════════════════════
 * <ThemeProvider>
 *
 *   Thin wrapper over `next-themes` pre-configured for the dashboard:
 *     • attribute="data-theme" — matches CSS selectors in themes/*.css
 *     • themes list comes from the registry so adding a theme is one edit
 *     • enableSystem=false — theme is a deliberate choice, not OS-derived
 *     • storageKey="reel-theme" — namespaced so it won't collide
 *     • disableTransitionOnChange — no colour animation during a swap
 * ═══════════════════════════════════════════════════════════════════════════ */

import { ThemeProvider as NextThemesProvider } from "next-themes";
import type { ReactNode } from "react";
import { DEFAULT_THEME, THEME_IDS } from "./registry";

export function ThemeProvider({ children }: { children: ReactNode }) {
  return (
    <NextThemesProvider
      attribute="data-theme"
      defaultTheme={DEFAULT_THEME}
      themes={[...THEME_IDS]}
      enableSystem={false}
      storageKey="reel-theme"
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  );
}

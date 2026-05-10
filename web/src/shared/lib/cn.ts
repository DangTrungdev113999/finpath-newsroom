import clsx, { type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * `cn` — classname merge helper.
 *
 * Combines `clsx` (conditional class composition) with `tailwind-merge`
 * (dedupe conflicting Tailwind utilities). Use everywhere that components
 * accept a `className` override so later classes win predictably.
 */
export function cn(...args: ClassValue[]): string {
  return twMerge(clsx(args));
}

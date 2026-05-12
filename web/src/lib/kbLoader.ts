import { extractHeadings, parseFrontmatter } from './kbParse';
import type { KbDoc, Sector } from './kbTypes';
import { SECTORS } from './kbTypes';

// Vite import.meta.glob: at build time, every kb/**/*.md is read as raw text.
// Dev mode needs vite.config.ts server.fs.allow ['..', '.'] (set in Task 1).

const allRawModules = import.meta.glob('../../../kb/**/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>;

function pathToSlugAndSector(path: string): { slug: string; sector: Sector } | null {
  // '../../../kb/bds/frameworks/bds-res-land-bank-nav.md' → sector='bds', slug='bds-res-land-bank-nav'
  const match = path.match(/\/kb\/([^/]+)\/.*\/([^/]+)\.md$/);
  if (!match) return null;

  const rawSector = match[1];
  const slug = match[2];

  // Map folder name to sector ID
  const sector = rawSector as Sector;
  if (!SECTORS.includes(sector)) return null;

  return { slug, sector };
}

function buildAllDocs(): Map<Sector, KbDoc[]> {
  const map = new Map<Sector, KbDoc[]>();
  for (const s of SECTORS) map.set(s, []);

  for (const [path, raw] of Object.entries(allRawModules)) {
    const parsed = pathToSlugAndSector(path);
    if (!parsed) continue;

    const { slug, sector } = parsed;
    const { meta, body } = parseFrontmatter(raw);
    const headings = extractHeadings(body);

    map.get(sector)!.push({ slug, sector, meta, body, headings });
  }

  // Sort each sector's docs
  for (const docs of map.values()) {
    docs.sort((a, b) => a.slug.localeCompare(b.slug));
  }

  return map;
}

const ALL_DOCS = buildAllDocs();

export function docsForSector(sector: Sector): KbDoc[] {
  return ALL_DOCS.get(sector) ?? [];
}

export function findDoc(sector: Sector, slug: string): KbDoc | undefined {
  return docsForSector(sector).find((d) => d.slug === slug);
}

export function allDocs(): KbDoc[] {
  const result: KbDoc[] = [];
  for (const docs of ALL_DOCS.values()) {
    result.push(...docs);
  }
  return result;
}

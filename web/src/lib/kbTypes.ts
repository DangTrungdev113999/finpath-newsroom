export interface KbMeta {
  category?: string;
  title?: string;
  last_updated?: string;
  applies_to?: string[];
  notion_page_id?: string;
  source_url?: string;
  [extra: string]: unknown;
}

export interface Heading {
  level: 2 | 3;
  text: string;
  slug: string;
}

export interface KbDoc {
  slug: string;
  sector: 'bds' | 'bank' | 'ck';
  meta: KbMeta;
  body: string;
  headings: Heading[];
}

export interface GroupConfig {
  id: string;
  icon: string;
  label: string;
  match: (slug: string) => boolean;
}

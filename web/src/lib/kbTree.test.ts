import { describe, expect, it } from 'vitest';
import { BDS_GROUPS, BDS_TITLES, groupForSlug, titleForSlug } from './kbTree';

describe('BDS_GROUPS — catch-all guarantee', () => {
  it('last group matches anything (catch-all)', () => {
    const last = BDS_GROUPS[BDS_GROUPS.length - 1];
    expect(last.id).toBe('other');
    expect(last.match('completely-unknown-slug')).toBe(true);
  });

  it('master slug matches master group', () => {
    expect(groupForSlug('bds-industry-master-reference').id).toBe('master');
  });

  it('res prefix → residential group', () => {
    expect(groupForSlug('bds-res-land-bank-nav').id).toBe('res');
    expect(groupForSlug('bds-res-project-lifecycle').id).toBe('res');
  });

  it('macro/legal/debt/revenue/hybrid prefixes → general group', () => {
    expect(groupForSlug('bds-macro-cycle-credit').id).toBe('general');
    expect(groupForSlug('bds-legal-framework').id).toBe('general');
    expect(groupForSlug('bds-debt-leverage').id).toBe('general');
    expect(groupForSlug('bds-revenue-recognition-vas').id).toBe('general');
    expect(groupForSlug('bds-hybrid-business-models').id).toBe('general');
  });

  it('kcn/retail/office/resort/dc prefixes → respective groups', () => {
    expect(groupForSlug('bds-kcn-lease-structure').id).toBe('kcn');
    expect(groupForSlug('bds-retail-footfall-mechanism').id).toBe('retail');
    expect(groupForSlug('bds-office-class-tiering').id).toBe('office');
    expect(groupForSlug('bds-resort-tourism-cycle').id).toBe('resort');
    expect(groupForSlug('bds-dc-hyperscaler-power').id).toBe('dc');
  });

  it('unknown slug falls through to catch-all "other"', () => {
    expect(groupForSlug('bds-newcategory-foo').id).toBe('other');
    expect(groupForSlug('something-random').id).toBe('other');
  });
});

describe('titleForSlug — fallback chain', () => {
  it('returns mapped VN title when in BDS_TITLES', () => {
    expect(titleForSlug('bds-res-land-bank-nav', '', undefined)).toBe('Quỹ đất & NAV');
    expect(titleForSlug('bds-industry-master-reference', '', undefined)).toBe('Tham chiếu ngành');
  });

  it('falls back to H1 of body when slug not mapped', () => {
    const body = '# My Custom Title\n\nbody content';
    expect(titleForSlug('bds-unknown-foo', body, undefined)).toBe('My Custom Title');
  });

  it('falls back to frontmatter title when no H1', () => {
    expect(titleForSlug('bds-unknown-foo', 'body without h1', 'Frontmatter Title'))
      .toBe('Frontmatter Title');
  });

  it('falls back to slug when nothing else', () => {
    expect(titleForSlug('bds-unknown-foo', 'body', undefined)).toBe('bds-unknown-foo');
  });

  it('mapped title wins over body H1 + frontmatter (consistency rule)', () => {
    const body = '# Ngành bất động sản Việt Nam — Tham chiếu ngành';
    expect(titleForSlug('bds-industry-master-reference', body, 'Some Frontmatter Title'))
      .toBe('Tham chiếu ngành');
  });
});

describe('BDS_TITLES — all 21 expected slugs present', () => {
  const expectedSlugs = [
    'bds-industry-master-reference',
    'bds-macro-cycle-credit',
    'bds-legal-framework',
    'bds-debt-leverage',
    'bds-revenue-recognition-vas',
    'bds-hybrid-business-models',
    'bds-res-land-bank-nav',
    'bds-res-project-lifecycle',
    'bds-res-presales-backlog',
    'bds-kcn-fdi-demand-mechanism',
    'bds-kcn-lease-structure',
    'bds-kcn-inventory-pricing',
    'bds-retail-footfall-mechanism',
    'bds-retail-anchor-vs-sme-tenants',
    'bds-retail-tenant-mix-quality',
    'bds-office-class-tiering',
    'bds-office-hybrid-work-impact',
    'bds-resort-tourism-cycle',
    'bds-resort-condotel-legal-pitfalls',
    'bds-resort-hybrid-model',
    'bds-dc-hyperscaler-power',
  ];
  for (const slug of expectedSlugs) {
    it(`has VN title for ${slug}`, () => {
      expect(BDS_TITLES[slug]).toBeTruthy();
      expect(BDS_TITLES[slug]).not.toBe(slug);
    });
  }
});

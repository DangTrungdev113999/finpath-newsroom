export function formatCrawledAt(iso: string): string {
  const d = new Date(iso);
  const dd = String(d.getDate()).padStart(2, '0');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const yyyy = d.getFullYear();
  const hh = String(d.getHours()).padStart(2, '0');
  const mi = String(d.getMinutes()).padStart(2, '0');
  return `${dd}/${mm}/${yyyy} ${hh}:${mi}`;
}

export function formatPublishedDate(iso: string): string {
  const d = new Date(iso);
  const dd = String(d.getDate()).padStart(2, '0');
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const yyyy = d.getFullYear();
  return `${dd}/${mm}/${yyyy}`;
}

const KEY_VIEW_COLOR: Record<string, string> = {
  'lạc quan': 'bg-green-100 text-green-800',
  'thận trọng': 'bg-amber-100 text-amber-800',
  'trung lập': 'bg-gray-100 text-gray-800',
};

export function keyViewBadgeClass(keyView: string): string {
  return KEY_VIEW_COLOR[keyView] ?? 'bg-gray-100 text-gray-800';
}

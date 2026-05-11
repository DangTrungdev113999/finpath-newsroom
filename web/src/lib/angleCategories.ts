/**
 * The 5 deep_question categories that Story Editor assigns to each article.
 * Filter axis: "Hướng tiếp cận" — angle of analysis.
 */

export type AngleCategoryId =
  | 'paradox'
  | 'why_now'
  | 'hidden_mechanism'
  | 'comparison_deep'
  | 'early_signal';

export interface AngleCategory {
  id: AngleCategoryId;
  label: string;
  short: string;
  description: string;
}

export const ANGLE_CATEGORIES: readonly AngleCategory[] = [
  {
    id: 'paradox',
    label: 'Nghịch lý',
    short: 'Nghịch lý',
    description: '2 sự kiện ngược chiều cùng lúc',
  },
  {
    id: 'why_now',
    label: 'Vì sao bây giờ',
    short: 'Vì sao',
    description: 'Timing của hành động lớn',
  },
  {
    id: 'hidden_mechanism',
    label: 'Cơ chế ngầm',
    short: 'Cơ chế',
    description: 'Cơ chế đằng sau con số',
  },
  {
    id: 'comparison_deep',
    label: 'So sánh sâu',
    short: 'So sánh',
    description: 'So sánh 2 nhóm góc nhìn mới',
  },
  {
    id: 'early_signal',
    label: 'Chỉ dấu sớm',
    short: 'Chỉ dấu',
    description: 'Tín hiệu sớm cho chu kỳ',
  },
] as const;

export function getAngleCategory(
  id: string | undefined,
): AngleCategory | undefined {
  if (!id) return undefined;
  return ANGLE_CATEGORIES.find((c) => c.id === id);
}

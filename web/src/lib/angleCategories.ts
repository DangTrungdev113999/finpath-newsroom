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
    description:
      'Cùng lúc xảy ra 2 sự kiện ngược chiều (ví dụ: lãi kỷ lục nhưng nợ xấu cũng tăng) — bài đi tìm vì sao cả 2 cùng đến.',
  },
  {
    id: 'why_now',
    label: 'Vì sao bây giờ',
    short: 'Vì sao',
    description:
      'Doanh nghiệp vừa ra quyết định lớn — vì sao chọn ĐÚNG thời điểm này, không phải năm trước hay năm sau?',
  },
  {
    id: 'hidden_mechanism',
    label: 'Cơ chế ngầm',
    short: 'Cơ chế',
    description:
      'Con số chỉ là kết quả. Bài đào sâu cơ chế kinh doanh đứng sau: tiền đến từ đâu, ai trả, vì sao bền vững được.',
  },
  {
    id: 'comparison_deep',
    label: 'So sánh sâu',
    short: 'So sánh',
    description:
      'Đặt 2 nhóm cạnh nhau với góc ít người để ý — ví dụ Big4 vs tư nhân, hay 2 chiến lược ngược chiều cùng quý.',
  },
  {
    id: 'early_signal',
    label: 'Chỉ dấu sớm',
    short: 'Chỉ dấu',
    description:
      'Một chỉ số nhỏ đang nhấp nháy — có thể là tín hiệu sớm cho chu kỳ 6-12 tháng tới. Bài check chỉ số đó.',
  },
] as const;

export function getAngleCategory(
  id: string | undefined,
): AngleCategory | undefined {
  if (!id) return undefined;
  return ANGLE_CATEGORIES.find((c) => c.id === id);
}

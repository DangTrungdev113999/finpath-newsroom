/**
 * The 4 article formats (V5.1 Format Director step 3.5).
 * Filter axis: "Định dạng bài" — cách trình bày + độ dài.
 */

import type { FormatId } from '../types';

export interface FormatCategory {
  id: FormatId;
  label: string;
  short: string;
  wordRange: string;
  description: string;
}

export const FORMAT_CATEGORIES: readonly FormatCategory[] = [
  {
    id: 'flash_qa',
    label: 'Flash Q&A',
    short: 'Flash',
    wordRange: '100-150 từ',
    description:
      'Bài cực ngắn — 1 câu hỏi + 1 đoạn trả lời + verdict. Dùng khi mã đang Hot (top tăng/giảm/bùng nổ/cạn cung), người đọc cần info nhanh.',
  },
  {
    id: 'standard_qa',
    label: 'Q&A chuẩn',
    short: 'Q&A',
    wordRange: '200-300 từ',
    description:
      '1 câu hỏi sắc xoáy sâu — opening + 2-3 bullet + closing. Dùng khi có nghịch lý hoặc câu hỏi why_now rõ ràng, data vừa.',
  },
  {
    id: 'standard_listicle',
    label: 'Liệt kê',
    short: 'List',
    wordRange: '250-350 từ',
    description:
      'Listicle 4-6 bullet — opening + nhiều điểm song song + closing. Dùng khi data nhiều, cần nhiều luận điểm cùng trọng số.',
  },
  {
    id: 'standard_narrative',
    label: 'Kể chuyện',
    short: 'Story',
    wordRange: '250-350 từ',
    description:
      'Kể chuyện theo dòng — 2-3 paragraph prose, ít/không bullet. Dùng khi cần dẫn dắt cảm xúc hoặc kể quá trình hơn liệt kê.',
  },
] as const;

export function getFormatCategory(
  id: string | undefined,
): FormatCategory | undefined {
  if (!id) return undefined;
  return FORMAT_CATEGORIES.find((c) => c.id === id);
}

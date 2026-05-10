import type { DeepQuestionOption } from '../types';

export function QuestionOptions({
  options,
  chosenIdx,
  pickReason,
  skipReasons,
}: {
  options: DeepQuestionOption[];
  chosenIdx: number;
  pickReason: string;
  skipReasons: Record<string, string>;
}) {
  if (!options || options.length === 0) return null;
  return (
    <section>
      <h3 className="section-pill">Tổng biên tập đề xuất {options.length} câu hỏi đào sâu</h3>
      <ol className="space-y-3">
        {options.map((opt, i) => {
          const isPicked = i === chosenIdx;
          return (
            <li key={i} className="leading-relaxed">
              {isPicked ? (
                <>
                  <strong className="text-done">(✓ Đã chọn)</strong>{' '}
                  <strong>{opt.question}</strong>
                  <div className="text-sm text-fg-2 mt-1">
                    <em>Phóng viên pick vì</em>: {pickReason || opt.pick_hint}
                  </div>
                </>
              ) : (
                <>
                  {opt.question}
                  <div className="text-sm text-fg-3 mt-1">
                    <em>Skip vì</em>: {skipReasons[String(i)] || 'Không có lý do ghi'}
                  </div>
                </>
              )}
            </li>
          );
        })}
      </ol>
    </section>
  );
}

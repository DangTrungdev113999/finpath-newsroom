import { useEffect, useState } from 'react';
import type { ArticleMeta } from '../types';
import { QuestionOptions } from './QuestionOptions';
import { DataTrail } from './DataTrail';
import { InsightCallout } from './InsightCallout';
import { PipelineObservability } from './PipelineObservability';
import { FormatPickPanel } from './FormatPickPanel';
import { formatPublishedDate } from '../lib/format';

export function RightColumn({ meta }: { meta: ArticleMeta }) {
  const src = meta.right_source;
  const [isDesktop, setIsDesktop] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia('(min-width: 768px)');
    setIsDesktop(mq.matches);
    const listener = (e: MediaQueryListEvent) => setIsDesktop(e.matches);
    mq.addEventListener('change', listener);
    return () => mq.removeEventListener('change', listener);
  }, []);

  return (
    <details open={isDesktop} className="md:block">
      <summary className="cursor-pointer font-semibold mb-4 md:hidden">
        Mở metadata + nguồn (7 sections)
      </summary>
      <div className="space-y-6">
      {/* Section 1: Bài gốc */}
      <section>
        <h3 className="section-pill">Bài gốc</h3>
        <p className="font-semibold">{src.raw_title}</p>
        <p className="text-sm text-fg-3 italic">
          Nguồn:{' '}
          <a href={src.url} target="_blank" rel="noopener noreferrer">
            {src.name}
          </a>{' '}
          · Published {formatPublishedDate(src.published)}
        </p>
      </section>

      {/* Section 2: Vì sao chọn */}
      {meta.why_chosen_narrative && (
        <section>
          <h3 className="section-pill">Vì sao chọn bài này</h3>
          <p className="leading-relaxed">{meta.why_chosen_narrative}</p>
        </section>
      )}

      {/* Section 2b: Format chọn — V5.0 Format Director (graceful degrade for legacy) */}
      <FormatPickPanel data={meta.format_director} />

      {/* Section 3: Hướng tiếp cận */}
      {meta.angle_label && (
        <section>
          <h3 className="section-pill">Hướng tiếp cận</h3>
          <p className="leading-relaxed">
            <strong>{meta.angle_label}</strong>
            {meta.angle_narrative && <> — {meta.angle_narrative}</>}
          </p>
        </section>
      )}

      {/* Section 4: Question options + Master pick */}
      <QuestionOptions
        options={meta.deep_question_options}
        chosenIdx={meta.chosen_question_idx}
        pickReason={meta.chosen_pick_reason}
        skipReasons={meta.skip_reasons || {}}
      />

      {/* Section 4b: Insight cuối */}
      {meta.insight && (
        <section>
          <h3 className="section-pill">Insight cuối</h3>
          <InsightCallout insight={meta.insight} />
        </section>
      )}

      {/* Section 5: Master data trail */}
      <DataTrail
        title="Phóng viên đã tra ở đâu"
        trail={meta.master_data_trail}
      />

      {/* Section 6: Skeptic data trail — ẩn khi Step 5 paused (2026-05-12) */}
      {meta.skeptic_data_trail && meta.skeptic_data_trail.length > 0 && (
        <DataTrail
          title="Reviewer ngoài đã tra ở đâu"
          trail={meta.skeptic_data_trail}
        />
      )}

      {/* Section 7: Đọc bài gốc — link only, NO embed */}
      <section>
        <h3 className="section-pill">Đọc bài gốc</h3>
        <p>
          → <a href={meta.raw_article_url} target="_blank" rel="noopener noreferrer">
            {src.name} — {src.raw_title}
          </a>{' '}
          ({formatPublishedDate(src.published)})
        </p>
      </section>

      {/* Appendix: Pipeline observability — Phase F T11 */}
      <PipelineObservability pipelineLog={meta.pipeline_log} />
      </div>
    </details>
  );
}

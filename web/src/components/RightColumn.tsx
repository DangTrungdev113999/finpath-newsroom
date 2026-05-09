import type { ArticleMeta } from '../types';
import { CrawlFunnel } from './CrawlFunnel';
import { QuestionOptions } from './QuestionOptions';
import { DataTrail } from './DataTrail';
import { InsightCallout } from './InsightCallout';
import { formatPublishedDate } from '../lib/format';

export function RightColumn({ meta }: { meta: ArticleMeta }) {
  const src = meta.right_source;
  return (
    <section className="space-y-6">
      {/* Section 1: Bài gốc */}
      <section>
        <h3>📰 Bài gốc</h3>
        <p className="font-semibold">{src.raw_title}</p>
        <p className="text-sm text-gray-500 italic">
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
          <h3>🎯 Vì sao chọn bài này</h3>
          <p className="leading-relaxed">{meta.why_chosen_narrative}</p>
        </section>
      )}

      {/* Section 3: Hướng tiếp cận */}
      {meta.angle_label && (
        <section>
          <h3>🧭 Hướng tiếp cận</h3>
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
          <h3>💡 Insight cuối</h3>
          <InsightCallout insight={meta.insight} />
        </section>
      )}

      {/* Section 5: Crawl funnel */}
      {meta.crawl_funnel && (
        <CrawlFunnel data={meta.crawl_funnel} funnelBatchId={meta.funnel_batch_id} />
      )}

      {/* Section 6: Master data trail */}
      <DataTrail
        title="Phóng viên đã tra ở đâu"
        emoji="📋"
        trail={meta.master_data_trail}
      />

      {/* Section 7: Skeptic data trail */}
      <DataTrail
        title="Reviewer ngoài đã tra ở đâu"
        emoji="🔍"
        trail={meta.skeptic_data_trail}
      />

      {/* Section 8: Đọc bài gốc — link only, NO embed */}
      <section>
        <h3>📖 Đọc bài gốc</h3>
        <p>
          → <a href={meta.raw_article_url} target="_blank" rel="noopener noreferrer">
            {src.name} — {src.raw_title}
          </a>{' '}
          ({formatPublishedDate(src.published)})
        </p>
      </section>
    </section>
  );
}

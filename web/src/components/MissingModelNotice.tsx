import { cn } from '../shared/lib/cn';
import {
  type ArticleModel,
  ClaudeMark,
  GeminiMark,
  GrokMark,
} from './ModelToggle';

const MODEL_LABEL: Record<ArticleModel, string> = {
  claude: 'Claude',
  gemini: 'Gemini',
  grok: 'Grok',
};

function ModelMark({
  model,
  className,
}: {
  model: ArticleModel;
  className?: string;
}) {
  if (model === 'grok') return <GrokMark className={className} />;
  if (model === 'gemini')
    return <GeminiMark className={className} monochrome />;
  return <ClaudeMark className={className} />;
}

type Props =
  | { slot: 'card-title'; model: ArticleModel }
  | { slot: 'article-title'; model: ArticleModel }
  | { slot: 'article-body'; model: ArticleModel; ticker?: string };

/**
 * Editorial "missing model" notice. Renders when the user has Gemini or Grok
 * selected but this particular article has no body for that side — instead of
 * silently falling back to Claude (which would lie about whose voice they are
 * reading), we surface the gap. Three slots:
 *
 *  - `card-title`     fills the h3 slot of ArticleCard (flex-1, keeps footer).
 *  - `article-title`  replaces the h1 slot of CompareFeedLayout.
 *  - `article-body`   replaces LeftColumn body when the side has no markdown.
 */
export function MissingModelNotice(props: Props) {
  const label = MODEL_LABEL[props.model];

  if (props.slot === 'card-title') {
    return (
      <div className="mt-0 mb-5 flex flex-1 flex-col items-start gap-2">
        <span className="inline-flex items-center gap-1.5 rounded-md border border-dashed border-warn/55 bg-warn/8 px-2 py-1 font-mono text-[10px] font-semibold uppercase tracking-[0.16em] text-warn">
          <ModelMark model={props.model} className="h-2.5 w-2.5" />
          {label} · chưa có
        </span>
        <p className="text-[14px] italic leading-snug text-fg-3">
          Bài này chưa có phiên bản{' '}
          <span className="not-italic font-semibold text-fg-2">{label}</span>.
        </p>
      </div>
    );
  }

  if (props.slot === 'article-title') {
    return (
      <div className="flex flex-col items-start gap-3">
        <span className="inline-flex items-center gap-2 rounded-md border border-dashed border-warn/55 bg-warn/8 px-2.5 py-1 font-mono text-[10.5px] font-bold uppercase tracking-[0.2em] text-warn">
          <ModelMark model={props.model} className="h-3 w-3" />
          {label} · không có sẵn
        </span>
        <p className="m-0 font-display text-[28px] italic leading-tight text-fg-2 sm:text-[34px]">
          Bài này chưa được {label} viết.
        </p>
      </div>
    );
  }

  // article-body
  return (
    <div className="not-prose flex flex-col gap-4 border-l-2 border-warn/50 py-2 pl-5">
      <p className="m-0 text-[14.5px] leading-relaxed text-fg-2">
        Pipeline {props.ticker ? `cho ${props.ticker}` : ''} chạy không sinh
        bản <span className="font-semibold text-fg-1">{label}</span> — có thể{' '}
        Step 4.{props.model === 'gemini' ? '3' : '4'} {label} Writer bị tắt,
        API trả lỗi, hoặc article được publish trước khi side này được bật.
      </p>
      <p className="m-0 text-[13.5px] leading-relaxed text-fg-3">
        Đổi toggle phía trên về{' '}
        <em className="not-italic font-medium text-fg-1">Claude</em> để đọc
        bản gốc, hoặc chọn model khác có sẵn cho bài.
      </p>
      <div
        aria-hidden
        className={cn(
          'mt-2 inline-flex items-center gap-2 self-start',
          'font-mono text-[10px] font-medium uppercase tracking-[0.22em] text-fg-3',
        )}
      >
        <span className="h-px w-8 bg-fg-4/60" />
        <span>không fallback</span>
      </div>
    </div>
  );
}

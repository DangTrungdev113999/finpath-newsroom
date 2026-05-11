import { useEffect, useMemo, useRef, useState } from 'react';
import {
  Check,
  Gauge,
  Loader2,
  Mic2,
  Pause,
  Play,
  Settings2,
  Sparkles,
  Square,
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from '../shared/ui/dropdown-menu';
import { cn } from '../shared/lib/cn';
import { chunkForTTS, stripMarkdown } from '../lib/tts';
import {
  DEFAULT_PUTER_VOICE_ID,
  PUTER_VIETNAMESE_VOICES,
  isPuterReady,
  synthesizePuter,
  waitForPuter,
  type PuterVoice,
} from '../lib/puterTTS';

const RATE_PRESETS: { value: number; label: string }[] = [
  { value: 0.9, label: '0.9×' },
  { value: 1.0, label: '1×' },
  { value: 1.15, label: '1.15×' },
  { value: 1.3, label: '1.3×' },
  { value: 1.5, label: '1.5×' },
];

function VoiceGlyph({
  gender,
  active,
}: {
  gender: 'female' | 'male';
  active: boolean;
}) {
  // Stylised waveform glyph — gender hint via accent color, not generic icon
  const bars = gender === 'female' ? [3, 8, 5, 11, 7] : [4, 10, 6, 9, 5];
  return (
    <span
      aria-hidden
      className={cn(
        'flex h-6 w-6 shrink-0 items-end justify-center gap-[2px] rounded-md px-[3px] py-[2px]',
        active
          ? 'bg-brand/15 ring-1 ring-brand/40'
          : gender === 'female'
            ? 'bg-fg-4/15'
            : 'bg-fg-4/15',
      )}
    >
      {bars.map((h, i) => (
        <span
          key={i}
          style={{ height: `${h * 6}%` }}
          className={cn(
            'w-[2px] rounded-full',
            active ? 'bg-brand' : 'bg-fg-3',
          )}
        />
      ))}
    </span>
  );
}

type TTSState = 'idle' | 'loading' | 'playing' | 'paused';

const STORAGE_VOICE = 'tts.puterVoice';
const STORAGE_RATE = 'tts.rate';
const DEFAULT_RATE = 1.15;
const CHUNK_LEN = 2500;

export function TTSButton({
  text,
  label = 'Nghe bài',
}: {
  text: string;
  label?: string;
}) {
  const [state, setState] = useState<TTSState>('idle');
  const [voiceId, setVoiceId] = useState<string>(
    () => localStorage.getItem(STORAGE_VOICE) ?? DEFAULT_PUTER_VOICE_ID,
  );
  const [rate, setRate] = useState<number>(() => {
    const raw = localStorage.getItem(STORAGE_RATE);
    const n = raw ? parseFloat(raw) : NaN;
    return Number.isFinite(n) && n >= 0.5 && n <= 2 ? n : DEFAULT_RATE;
  });
  const [puterReady, setPuterReady] = useState(isPuterReady());
  const [settingsOpen, setSettingsOpen] = useState(false);

  const queueRef = useRef<string[]>([]);
  const indexRef = useRef(0);
  const stopRequestedRef = useRef(false);
  const rateRef = useRef(rate);
  const audioCacheRef = useRef<Map<number, HTMLAudioElement>>(new Map());
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);

  const cleanText = useMemo(() => stripMarkdown(text), [text]);
  const activeVoice = useMemo<PuterVoice>(
    () =>
      PUTER_VIETNAMESE_VOICES.find((v) => v.id === voiceId) ??
      PUTER_VIETNAMESE_VOICES[0],
    [voiceId],
  );

  // Persist + sync refs
  useEffect(() => {
    rateRef.current = rate;
    localStorage.setItem(STORAGE_RATE, String(rate));
    if (currentAudioRef.current) currentAudioRef.current.playbackRate = rate;
  }, [rate]);
  useEffect(() => {
    localStorage.setItem(STORAGE_VOICE, voiceId);
  }, [voiceId]);

  // Wait for Puter.js to load
  useEffect(() => {
    if (puterReady) return;
    waitForPuter(8000).then(setPuterReady);
  }, [puterReady]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      currentAudioRef.current?.pause();
      audioCacheRef.current.clear();
    };
  }, []);

  const fetchChunk = async (idx: number): Promise<HTMLAudioElement | null> => {
    if (audioCacheRef.current.has(idx)) return audioCacheRef.current.get(idx)!;
    const chunk = queueRef.current[idx];
    if (!chunk) return null;
    try {
      const audio = await synthesizePuter(chunk, activeVoice);
      audio.preload = 'auto';
      audio.playbackRate = rateRef.current;
      audioCacheRef.current.set(idx, audio);
      return audio;
    } catch (e) {
      // eslint-disable-next-line no-console
      console.warn('Puter synth error:', e);
      return null;
    }
  };

  const playNext = async () => {
    if (stopRequestedRef.current) return;
    const idx = indexRef.current;
    if (idx >= queueRef.current.length) {
      setState('idle');
      indexRef.current = 0;
      queueRef.current = [];
      audioCacheRef.current.clear();
      return;
    }

    setState('loading');
    let audio = audioCacheRef.current.get(idx);
    if (!audio) audio = (await fetchChunk(idx)) ?? undefined;

    if (stopRequestedRef.current) return;
    if (!audio) {
      indexRef.current += 1;
      playNext();
      return;
    }

    currentAudioRef.current = audio;
    audio.playbackRate = rateRef.current;
    audio.onended = () => {
      indexRef.current += 1;
      playNext();
    };
    setState('playing');
    audio.play().catch((err) => {
      // eslint-disable-next-line no-console
      console.warn('Audio play error:', err);
    });

    if (idx + 1 < queueRef.current.length) {
      fetchChunk(idx + 1);
    }
  };

  const start = async () => {
    if (!cleanText) return;
    if (!isPuterReady()) {
      setState('loading');
      const ready = await waitForPuter(8000);
      if (!ready) {
        setState('idle');
        // eslint-disable-next-line no-console
        console.warn('Puter.js không tải được. Refresh page rồi thử lại.');
        return;
      }
    }
    stopRequestedRef.current = false;
    audioCacheRef.current.clear();
    queueRef.current = chunkForTTS(cleanText, CHUNK_LEN);
    indexRef.current = 0;
    playNext();
  };

  const pause = () => {
    currentAudioRef.current?.pause();
    setState('paused');
  };

  const resume = () => {
    currentAudioRef.current?.play();
    setState('playing');
  };

  const stop = () => {
    stopRequestedRef.current = true;
    currentAudioRef.current?.pause();
    if (currentAudioRef.current) currentAudioRef.current.currentTime = 0;
    audioCacheRef.current.clear();
    indexRef.current = 0;
    queueRef.current = [];
    setState('idle');
  };

  const handleClick = () => {
    if (state === 'playing') return pause();
    if (state === 'paused') return resume();
    if (state === 'loading') return;
    start();
  };

  const isActive = state !== 'idle';

  const buttonLabel = (() => {
    if (state === 'loading') return 'Đang tải';
    if (state === 'playing') return 'Đang đọc';
    if (state === 'paused') return 'Tiếp tục';
    return label;
  })();

  return (
    <div className="inline-flex items-center gap-1">
      <button
        type="button"
        onClick={handleClick}
        disabled={state === 'loading'}
        aria-label={
          state === 'playing'
            ? 'Tạm dừng đọc bài'
            : state === 'paused'
              ? 'Tiếp tục đọc'
              : state === 'loading'
                ? 'Đang tải audio'
                : 'Đọc bài lên'
        }
        title={`Đọc bài (${activeVoice.label})`}
        className={cn(
          'inline-flex h-7 items-center gap-1.5 rounded-pill border px-2.5 font-sans text-[11px] font-medium transition-all duration-fast ease-out-quart',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
          'disabled:cursor-wait',
          isActive
            ? 'border-brand/60 bg-brand text-brand-fg shadow-sm shadow-brand/25'
            : 'border-fg-4/40 bg-bg-1 text-fg-2 hover:border-brand/40 hover:text-brand',
        )}
      >
        {state === 'loading' ? (
          <Loader2 className="h-3 w-3 animate-spin" strokeWidth={2.5} aria-hidden />
        ) : state === 'playing' ? (
          <Pause className="h-3 w-3" strokeWidth={2.5} aria-hidden />
        ) : (
          <Play className="h-3 w-3" strokeWidth={2.5} aria-hidden />
        )}
        <span>{buttonLabel}</span>
        {state === 'playing' && (
          <span
            aria-hidden
            className="relative ml-0.5 inline-flex h-1.5 w-1.5 items-center justify-center"
          >
            <span className="absolute inline-block h-1.5 w-1.5 animate-ping rounded-full bg-brand-fg/70" />
            <span className="relative inline-block h-1 w-1 rounded-full bg-brand-fg" />
          </span>
        )}
        {state === 'idle' && (
          <Sparkles
            className="h-2.5 w-2.5 text-brand"
            strokeWidth={2.5}
            aria-hidden
          />
        )}
      </button>

      {isActive && (
        <button
          type="button"
          onClick={stop}
          aria-label="Dừng đọc"
          title="Dừng"
          className={cn(
            'inline-flex h-7 w-7 items-center justify-center rounded-pill border border-fg-4/40 bg-bg-1 text-fg-2',
            'transition-colors duration-fast hover:border-rec/50 hover:text-rec',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rec/35',
          )}
        >
          <Square
            className="h-2.5 w-2.5"
            strokeWidth={2.5}
            aria-hidden
            fill="currentColor"
          />
        </button>
      )}

      <DropdownMenu open={settingsOpen} onOpenChange={setSettingsOpen}>
        <DropdownMenuTrigger
          className={cn(
            'inline-flex h-7 w-7 items-center justify-center rounded-pill border border-fg-4/40 bg-bg-1 text-fg-2',
            'transition-colors duration-fast hover:border-brand/40 hover:text-brand',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/35',
          )}
          aria-label="Cài đặt giọng đọc"
          title="Đổi giọng / tốc độ"
        >
          <Settings2 className="h-3 w-3" strokeWidth={2} aria-hidden />
        </DropdownMenuTrigger>

        <DropdownMenuContent
          align="end"
          side="bottom"
          sideOffset={8}
          className="w-[296px] overflow-hidden p-0"
        >
          {/* Header */}
          <div className="border-b border-fg-4/30 bg-bg-2/40 px-3.5 py-2.5">
            <div className="flex items-center gap-2">
              <Sparkles
                className="h-3.5 w-3.5 text-brand"
                strokeWidth={2.5}
                aria-hidden
              />
              <span className="font-sans text-[12px] font-semibold text-fg-0">
                Cài đặt giọng đọc
              </span>
            </div>
          </div>

          <div className="px-3.5 py-3">
            {/* Rate section */}
            <DropdownMenuLabel className="!mb-1.5 !p-0 flex items-center gap-1.5 font-sans text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-3">
              <Gauge className="h-3 w-3" strokeWidth={2} aria-hidden />
              Tốc độ
              <span className="ml-auto font-mono text-[11px] font-bold normal-case tracking-normal text-fg-0">
                {rate.toFixed(2)}×
              </span>
            </DropdownMenuLabel>
            <div className="relative pb-2 pt-1">
              <input
                type="range"
                min={0.7}
                max={1.8}
                step={0.05}
                value={rate}
                onChange={(e) => setRate(parseFloat(e.currentTarget.value))}
                className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-fg-4/40 accent-brand"
                style={{
                  background: `linear-gradient(to right, hsl(var(--brand)) 0%, hsl(var(--brand)) ${((rate - 0.7) / 1.1) * 100}%, hsl(var(--fg-4) / 0.4) ${((rate - 0.7) / 1.1) * 100}%, hsl(var(--fg-4) / 0.4) 100%)`,
                }}
                aria-label="Tốc độ đọc"
              />
              <div className="mt-2 flex items-center justify-between">
                {RATE_PRESETS.map((p) => {
                  const active = Math.abs(rate - p.value) < 0.025;
                  return (
                    <button
                      key={p.value}
                      type="button"
                      onClick={() => setRate(p.value)}
                      className={cn(
                        'rounded px-1 font-mono text-[9px] tabular-nums transition-colors duration-fast',
                        active
                          ? 'font-bold text-brand'
                          : 'text-fg-3 hover:text-fg-1',
                      )}
                    >
                      {p.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Voice section */}
            <DropdownMenuLabel className="!mb-1.5 !mt-3 !p-0 flex items-center gap-1.5 font-sans text-[10px] font-semibold uppercase tracking-[0.14em] text-fg-3">
              <Mic2 className="h-3 w-3" strokeWidth={2} aria-hidden />
              Giọng đọc
              <span className="ml-auto font-mono text-[10px] normal-case tracking-normal text-fg-3">
                {PUTER_VIETNAMESE_VOICES.length} giọng
              </span>
            </DropdownMenuLabel>

            <div className="-mr-1 max-h-64 space-y-3 overflow-y-auto pr-1">
              {(['male', 'female'] as const).map((gender) => {
                const voices = PUTER_VIETNAMESE_VOICES.filter(
                  (v) => v.gender === gender,
                );
                if (voices.length === 0) return null;
                return (
                  <div key={gender} className="space-y-0.5">
                    <div className="flex items-center gap-2 px-1 pb-1">
                      <span className="font-mono text-[9px] uppercase tracking-[0.18em] text-fg-3">
                        {gender === 'male' ? 'Nam' : 'Nữ'}
                      </span>
                      <div className="h-px flex-1 bg-fg-4/30" />
                    </div>
                    {voices.map((v) => {
                      const active = activeVoice.id === v.id;
                      const isDefault = v.id === DEFAULT_PUTER_VOICE_ID;
                      return (
                        <button
                          type="button"
                          key={v.id}
                          onClick={() => {
                            setVoiceId(v.id);
                            if (state !== 'idle')
                              audioCacheRef.current.clear();
                          }}
                          className={cn(
                            'group/voice relative flex w-full items-center gap-2.5 rounded-lg px-1.5 py-1.5 text-left transition-all duration-fast',
                            active
                              ? 'bg-brand/[0.09] ring-1 ring-brand/40'
                              : 'hover:bg-bg-2',
                          )}
                        >
                          {/* Active indicator bar */}
                          {active && (
                            <span
                              aria-hidden
                              className="absolute inset-y-2 left-0 w-[2px] rounded-r-full bg-brand"
                            />
                          )}
                          <VoiceGlyph gender={v.gender} active={active} />
                          <span className="flex min-w-0 flex-1 flex-col">
                            <span
                              className={cn(
                                'truncate font-sans text-[12px] font-medium',
                                active ? 'text-fg-0' : 'text-fg-1',
                              )}
                            >
                              {v.label}
                            </span>
                            {v.note && (
                              <span className="truncate font-sans text-[10px] text-fg-3">
                                {v.note}
                              </span>
                            )}
                          </span>
                          {isDefault && !active && (
                            <span
                              className="shrink-0 rounded-pill border border-fg-4/50 bg-bg-1 px-1.5 py-[1px] font-sans text-[9px] font-medium uppercase tracking-wider text-fg-3"
                              title="Giọng mặc định"
                            >
                              mặc định
                            </span>
                          )}
                          {active && (
                            <Check
                              className="h-3.5 w-3.5 shrink-0 text-brand"
                              strokeWidth={3}
                              aria-hidden
                            />
                          )}
                        </button>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </div>

          {!puterReady && (
            <div className="border-t border-fg-4/30 bg-bg-2/40 px-3.5 py-2">
              <p className="flex items-center gap-1.5 font-sans text-[10px] text-fg-3">
                <Loader2
                  className="h-2.5 w-2.5 animate-spin"
                  strokeWidth={2.5}
                  aria-hidden
                />
                Đang tải bộ tổng hợp giọng từ Puter…
              </p>
            </div>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

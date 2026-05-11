import { useEffect, useMemo, useRef, useState } from 'react';
import { Loader2, Pause, Play, Settings2, Sparkles, Square } from 'lucide-react';
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
          sideOffset={6}
          className="w-80 p-3"
        >
          <DropdownMenuLabel className="!p-0 !pb-2 text-fg-2">
            Tốc độ
          </DropdownMenuLabel>
          <div className="mb-3 flex items-center gap-3">
            <input
              type="range"
              min={0.7}
              max={1.8}
              step={0.05}
              value={rate}
              onChange={(e) => setRate(parseFloat(e.currentTarget.value))}
              className="flex-1 accent-brand"
              aria-label="Tốc độ đọc"
            />
            <span className="w-12 text-right font-mono text-[11px] tabular-nums text-fg-0">
              {rate.toFixed(2)}×
            </span>
          </div>

          <DropdownMenuLabel className="!p-0 !pb-2 text-fg-2">
            Giọng đọc
          </DropdownMenuLabel>

          <div className="max-h-56 space-y-0.5 overflow-y-auto pr-1">
            {PUTER_VIETNAMESE_VOICES.map((v) => {
              const active = activeVoice.id === v.id;
              return (
                <button
                  type="button"
                  key={v.id}
                  onClick={() => {
                    setVoiceId(v.id);
                    if (state !== 'idle') audioCacheRef.current.clear();
                  }}
                  className={cn(
                    'flex w-full items-center justify-between gap-2 rounded-md px-2 py-1.5 text-left font-sans text-[11px] transition-colors duration-fast',
                    active
                      ? 'bg-brand/10 text-fg-0 ring-1 ring-brand/40'
                      : 'text-fg-1 hover:bg-bg-2',
                  )}
                >
                  <span className="flex min-w-0 flex-1 items-center gap-1.5">
                    <span className="font-medium">{v.label}</span>
                    <span className="text-fg-3">
                      {v.gender === 'female' ? '· nữ' : '· nam'}
                    </span>
                    {v.note && (
                      <span className="truncate text-fg-3">· {v.note}</span>
                    )}
                  </span>
                  <span
                    className={cn(
                      'shrink-0 rounded-pill px-1.5 py-[1px] font-mono text-[9px] uppercase tracking-wider',
                      v.provider === 'openai'
                        ? 'bg-brand/15 text-brand'
                        : 'bg-fg-4/30 text-fg-2',
                    )}
                  >
                    {v.provider}
                  </span>
                </button>
              );
            })}
          </div>

          {!puterReady && (
            <p className="mt-3 rounded-md border border-fg-4/40 bg-bg-2/40 p-2 font-sans text-[10px] leading-relaxed text-fg-2">
              Đang tải Puter.js từ CDN…
            </p>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

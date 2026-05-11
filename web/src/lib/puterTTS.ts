/**
 * Curated voice catalogue for Vietnamese via Puter.com.
 *
 * Puter proxies to OpenAI/Gemini/ElevenLabs/AWS Polly — all free, no signup.
 * AWS Polly has no Vietnamese, so we skip it. OpenAI gpt-4o-mini-tts and
 * Gemini's multilingual voices handle Vietnamese well.
 */

export interface PuterVoice {
  id: string;
  label: string;
  provider: 'openai' | 'gemini';
  voice: string;
  model?: string;
  gender: 'female' | 'male';
  note?: string;
}

/**
 * Labels are Vietnamese descriptors (not the underlying engine voice name)
 * so the UI feels native. Internal `voice` field keeps the OpenAI/Gemini id.
 */
export const PUTER_VIETNAMESE_VOICES: PuterVoice[] = [
  // ─── Nam ────────────────────────────────────────────────────────────
  {
    id: 'openai-echo',
    label: 'Nam điềm tĩnh',
    provider: 'openai',
    voice: 'echo',
    model: 'gpt-4o-mini-tts',
    gender: 'male',
    note: 'rõ, đều',
  },
  {
    id: 'openai-onyx',
    label: 'Nam trầm',
    provider: 'openai',
    voice: 'onyx',
    model: 'gpt-4o-mini-tts',
    gender: 'male',
    note: 'sâu, chắc',
  },
  {
    id: 'openai-fable',
    label: 'Nam kể chuyện',
    provider: 'openai',
    voice: 'fable',
    model: 'gpt-4o-mini-tts',
    gender: 'male',
    note: 'biểu cảm',
  },
  {
    id: 'gemini-Puck',
    label: 'Nam năng động',
    provider: 'gemini',
    voice: 'Puck',
    gender: 'male',
    note: 'sống động',
  },
  // ─── Nữ ─────────────────────────────────────────────────────────────
  {
    id: 'openai-nova',
    label: 'Nữ sáng',
    provider: 'openai',
    voice: 'nova',
    model: 'gpt-4o-mini-tts',
    gender: 'female',
    note: 'trẻ, sáng',
  },
  {
    id: 'openai-coral',
    label: 'Nữ ấm',
    provider: 'openai',
    voice: 'coral',
    model: 'gpt-4o-mini-tts',
    gender: 'female',
    note: 'ấm, gần',
  },
  {
    id: 'openai-shimmer',
    label: 'Nữ nhẹ',
    provider: 'openai',
    voice: 'shimmer',
    model: 'gpt-4o-mini-tts',
    gender: 'female',
    note: 'mềm, dịu',
  },
  {
    id: 'gemini-Zephyr',
    label: 'Nữ thanh',
    provider: 'gemini',
    voice: 'Zephyr',
    gender: 'female',
    note: 'thanh thoát',
  },
  {
    id: 'gemini-Kore',
    label: 'Nữ trung',
    provider: 'gemini',
    voice: 'Kore',
    gender: 'female',
    note: 'cân bằng',
  },
];

export const DEFAULT_PUTER_VOICE_ID = 'openai-echo';

/** Synthesize one chunk via Puter and return a playable HTMLAudioElement. */
export async function synthesizePuter(
  text: string,
  voice: PuterVoice,
  instructions?: string,
): Promise<HTMLAudioElement> {
  if (!window.puter?.ai?.txt2speech) {
    throw new Error('Puter.js chưa load xong. Refresh page rồi thử lại.');
  }
  const audio = await window.puter.ai.txt2speech(text, {
    provider: voice.provider,
    voice: voice.voice,
    model: voice.model,
    language: 'vi-VN',
    instructions:
      instructions ?? 'Speak naturally in Vietnamese with clear pronunciation.',
    response_format: 'mp3',
  });
  return audio;
}

/** Quick check whether Puter.js global is available right now. */
export function isPuterReady(): boolean {
  return !!window.puter?.ai?.txt2speech;
}

/** Wait for Puter.js to load (returns true if ready within timeout). */
export function waitForPuter(timeoutMs = 5000): Promise<boolean> {
  if (isPuterReady()) return Promise.resolve(true);
  return new Promise((resolve) => {
    const start = Date.now();
    const id = window.setInterval(() => {
      if (isPuterReady()) {
        window.clearInterval(id);
        resolve(true);
      } else if (Date.now() - start > timeoutMs) {
        window.clearInterval(id);
        resolve(false);
      }
    }, 100);
  });
}

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

export const PUTER_VIETNAMESE_VOICES: PuterVoice[] = [
  // OpenAI multilingual (gpt-4o-mini-tts) — strong Vietnamese pronunciation
  {
    id: 'openai-nova',
    label: 'Nova',
    provider: 'openai',
    voice: 'nova',
    model: 'gpt-4o-mini-tts',
    gender: 'female',
    note: 'sáng, năng động',
  },
  {
    id: 'openai-shimmer',
    label: 'Shimmer',
    provider: 'openai',
    voice: 'shimmer',
    model: 'gpt-4o-mini-tts',
    gender: 'female',
    note: 'nhẹ nhàng',
  },
  {
    id: 'openai-coral',
    label: 'Coral',
    provider: 'openai',
    voice: 'coral',
    model: 'gpt-4o-mini-tts',
    gender: 'female',
    note: 'ấm, kể chuyện',
  },
  {
    id: 'openai-onyx',
    label: 'Onyx',
    provider: 'openai',
    voice: 'onyx',
    model: 'gpt-4o-mini-tts',
    gender: 'male',
    note: 'trầm, chắc',
  },
  {
    id: 'openai-echo',
    label: 'Echo',
    provider: 'openai',
    voice: 'echo',
    model: 'gpt-4o-mini-tts',
    gender: 'male',
    note: 'điềm tĩnh',
  },
  {
    id: 'openai-fable',
    label: 'Fable',
    provider: 'openai',
    voice: 'fable',
    model: 'gpt-4o-mini-tts',
    gender: 'male',
    note: 'kể chuyện',
  },
  // Gemini multilingual
  {
    id: 'gemini-Kore',
    label: 'Kore',
    provider: 'gemini',
    voice: 'Kore',
    gender: 'female',
    note: 'Gemini · ấm',
  },
  {
    id: 'gemini-Zephyr',
    label: 'Zephyr',
    provider: 'gemini',
    voice: 'Zephyr',
    gender: 'female',
    note: 'Gemini · thanh',
  },
  {
    id: 'gemini-Puck',
    label: 'Puck',
    provider: 'gemini',
    voice: 'Puck',
    gender: 'male',
    note: 'Gemini · năng động',
  },
];

export const DEFAULT_PUTER_VOICE_ID = 'openai-nova';

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

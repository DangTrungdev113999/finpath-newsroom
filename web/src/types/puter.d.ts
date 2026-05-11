/**
 * Minimal Puter.js typing — only the txt2speech surface we use.
 * Full surface: https://docs.puter.com/AI/txt2speech/
 */
declare global {
  interface Window {
    puter?: {
      ai: {
        txt2speech: (
          text: string,
          options?: {
            provider?: 'openai' | 'gemini' | 'elevenlabs' | 'aws-polly' | 'xai';
            voice?: string;
            model?: string;
            language?: string;
            response_format?: 'mp3' | 'opus' | 'aac' | 'flac' | 'wav' | 'pcm';
            instructions?: string;
          },
        ) => Promise<HTMLAudioElement>;
      };
    };
  }
}

export {};

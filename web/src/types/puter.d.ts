/**
 * Minimal Puter.js typing — only the surfaces we use.
 * - txt2speech: https://docs.puter.com/AI/txt2speech/
 * - auth:       https://docs.puter.com/Auth/
 */
declare global {
  interface PuterUser {
    uuid?: string;
    username?: string;
    email_confirmed?: boolean;
  }

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
      auth?: {
        isSignedIn: () => boolean;
        signIn: (options?: {
          attempt_temp_user_creation?: boolean;
        }) => Promise<PuterUser | boolean>;
        signOut: () => Promise<void> | void;
        getUser: () => Promise<PuterUser>;
      };
    };
  }
}

export {};

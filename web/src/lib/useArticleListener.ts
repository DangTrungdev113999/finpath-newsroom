import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * TTS playback queue cho danh sách bài. Dùng Web Speech API (browser-native,
 * không tốn token). Tự advance khi 1 utterance kết thúc; intentional stop /
 * unmount cleanup qua ref guard để tránh race với `speechSynthesis.cancel()`.
 *
 * `items` = mảng text cuối cùng đọc lên — caller chuẩn bị trước (vd title + key_view).
 */

export type ListenState = 'idle' | 'playing' | 'paused';

export interface UseArticleListener {
  state: ListenState;
  currentIdx: number;
  total: number;
  supported: boolean;
  play: () => void;
  pause: () => void;
  stop: () => void;
  next: () => void;
}

const supported =
  typeof window !== 'undefined' && 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;

export function useArticleListener(
  items: string[],
  opts: { lang?: string; rate?: number } = {},
): UseArticleListener {
  const [state, setState] = useState<ListenState>('idle');
  const [currentIdx, setCurrentIdx] = useState(-1);
  const intentionalStopRef = useRef(false);
  const itemsRef = useRef(items);
  itemsRef.current = items;

  const speakAt = useCallback(
    (idx: number) => {
      const list = itemsRef.current;
      if (idx >= list.length) {
        setState('idle');
        setCurrentIdx(-1);
        return;
      }
      const u = new SpeechSynthesisUtterance(list[idx]);
      u.lang = opts.lang ?? 'vi-VN';
      u.rate = opts.rate ?? 1.0;
      u.onend = () => {
        if (intentionalStopRef.current) return;
        const nextIdx = idx + 1;
        if (nextIdx < itemsRef.current.length) {
          setCurrentIdx(nextIdx);
          speakAt(nextIdx);
        } else {
          setState('idle');
          setCurrentIdx(-1);
        }
      };
      u.onerror = () => {
        if (intentionalStopRef.current) return;
        // Skip on error, try next
        const nextIdx = idx + 1;
        if (nextIdx < itemsRef.current.length) {
          setCurrentIdx(nextIdx);
          speakAt(nextIdx);
        } else {
          setState('idle');
          setCurrentIdx(-1);
        }
      };
      window.speechSynthesis.cancel(); // clear any pending
      window.speechSynthesis.speak(u);
    },
    [opts.lang, opts.rate],
  );

  const play = useCallback(() => {
    if (!supported) return;
    if (state === 'paused') {
      window.speechSynthesis.resume();
      setState('playing');
      return;
    }
    if (itemsRef.current.length === 0) return;
    intentionalStopRef.current = false;
    setState('playing');
    setCurrentIdx(0);
    speakAt(0);
  }, [state, speakAt]);

  const pause = useCallback(() => {
    if (!supported) return;
    if (state !== 'playing') return;
    window.speechSynthesis.pause();
    setState('paused');
  }, [state]);

  const stop = useCallback(() => {
    if (!supported) return;
    intentionalStopRef.current = true;
    window.speechSynthesis.cancel();
    setState('idle');
    setCurrentIdx(-1);
  }, []);

  const next = useCallback(() => {
    if (!supported) return;
    if (state === 'idle') return;
    const upcoming = currentIdx + 1;
    if (upcoming >= itemsRef.current.length) {
      // No more — stop
      intentionalStopRef.current = true;
      window.speechSynthesis.cancel();
      setState('idle');
      setCurrentIdx(-1);
      return;
    }
    intentionalStopRef.current = true; // skip the natural-end advance
    window.speechSynthesis.cancel();
    // Reset guard then advance
    requestAnimationFrame(() => {
      intentionalStopRef.current = false;
      setCurrentIdx(upcoming);
      speakAt(upcoming);
    });
  }, [state, currentIdx, speakAt]);

  // Chrome bug: speechSynthesis tự dừng sau ~15s. Workaround: pause/resume
  // mỗi 10s khi đang playing — không ảnh hưởng audio thực tế.
  useEffect(() => {
    if (!supported || state !== 'playing') return;
    const t = window.setInterval(() => {
      if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
        window.speechSynthesis.pause();
        window.speechSynthesis.resume();
      }
    }, 10000);
    return () => window.clearInterval(t);
  }, [state]);

  // Cleanup khi unmount
  useEffect(() => {
    return () => {
      intentionalStopRef.current = true;
      if (supported) window.speechSynthesis.cancel();
    };
  }, []);

  return {
    state,
    currentIdx,
    total: items.length,
    supported,
    play,
    pause,
    stop,
    next,
  };
}

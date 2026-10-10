import React from 'react';
import { useCurrentFrame } from 'remotion';
import { WordTimestamp } from '../types';
import { useTheme } from '../ThemeContext';

interface SubtitleOverlayProps {
  words?: WordTimestamp[];
  aspectRatio: '9:16' | '16:9';
  narrationFallback?: string;
}

// Word-by-word highlight, synced to word timings (from TTS).
export const SubtitleOverlay: React.FC<SubtitleOverlayProps> = ({ words, aspectRatio, narrationFallback }) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const currentSec = frame / 30;
  const vertical = aspectRatio === '9:16';
  const pos = vertical ? 'bottom-28' : 'bottom-10';
  const light = t.name === 'light-grid';
  const box: React.CSSProperties = {
    background: light ? '#ffffff' : 'rgba(2,6,23,0.85)',
    border: `1px solid ${light ? '#e5e7eb' : t.cardBorder}`,
    boxShadow: light ? '0 6px 20px rgba(15,23,42,0.08)' : '0 0 30px rgba(0,0,0,0.8)',
  };

  if (!words || words.length === 0) {
    if (!narrationFallback) return null;
    return (
      <div className={`absolute w-full px-8 flex justify-center text-center pointer-events-none z-30 ${pos}`}>
        <div className="px-6 py-3 rounded-2xl backdrop-blur-md" style={box}>
          <p className="text-xl md:text-2xl font-semibold tracking-wide" style={{ color: t.text }}>{narrationFallback}</p>
        </div>
      </div>
    );
  }

  let activeIndex = -1;
  for (let i = 0; i < words.length; i++) {
    if (currentSec >= words[i].start && currentSec <= words[i].end + 0.1) { activeIndex = i; break; }
  }
  const chunkSize = vertical ? 5 : 8;
  const chunkIndex = activeIndex >= 0 ? Math.floor(activeIndex / chunkSize) : 0;
  const chunk = words.slice(chunkIndex * chunkSize, (chunkIndex + 1) * chunkSize);

  return (
    <div className={`absolute w-full px-6 flex justify-center text-center pointer-events-none z-30 ${pos}`}>
      <div className="px-6 py-3.5 rounded-2xl backdrop-blur-md flex flex-wrap items-center justify-center gap-2 max-w-[90%]" style={box}>
        {chunk.map((w, idx) => {
          const g = chunkIndex * chunkSize + idx;
          const isActive = g === activeIndex;
          const isPast = g < activeIndex;
          const color = isActive ? '#0a0a0a' : isPast ? t.accent : t.textMuted;
          return (
            <span key={g} className={`px-1.5 py-0.5 rounded font-bold ${vertical ? 'text-2xl' : 'text-xl'}`}
              style={{
                color,
                background: isActive ? '#f59e0b' : 'transparent',
                opacity: !isActive && !isPast ? 0.6 : 1,
                transform: isActive ? 'scale(1.1)' : 'none',
              }}>
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};

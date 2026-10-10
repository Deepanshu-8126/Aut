import React from 'react';
import { useCurrentFrame } from 'remotion';
import { WordTimestamp } from '../types';
import { useTheme } from '../ThemeContext';

interface SubtitleOverlayProps {
  words?: WordTimestamp[];
  aspectRatio: '9:16' | '16:9';
  narrationFallback?: string;
}

// Karaoke caption: bada, black pill box, active word yellow. Phone par bhi padhne layak.
export const SubtitleOverlay: React.FC<SubtitleOverlayProps> = ({ words, aspectRatio, narrationFallback }) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const currentSec = frame / 30;
  const vertical = aspectRatio === '9:16';
  const box: React.CSSProperties = {
    background: 'rgba(10,10,10,0.92)',
    boxShadow: '0 10px 30px rgba(0,0,0,0.25)',
    minHeight: vertical ? 120 : 92,
    borderRadius: 22,
    padding: vertical ? '20px 26px' : '16px 34px',
    maxWidth: vertical ? '92%' : '78%',
  };
  const wordSize = vertical ? 46 : 38;

  if (!words || words.length === 0) {
    if (!narrationFallback) return null;
    return (
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: vertical ? 220 : 64, display: 'flex', justifyContent: 'center', zIndex: 30 }}>
        <div style={box}>
          <p style={{ margin: 0, color: '#ffffff', fontSize: wordSize, fontWeight: 700, lineHeight: 1.3, textAlign: 'center' }}>{narrationFallback}</p>
        </div>
      </div>
    );
  }

  let activeIndex = -1;
  for (let i = 0; i < words.length; i++) {
    if (currentSec >= words[i].start && currentSec <= words[i].end + 0.1) { activeIndex = i; break; }
  }
  if (activeIndex < 0) {
    // Word gap ya scene ke end par: pichhla word active rakho
    for (let i = words.length - 1; i >= 0; i--) { if (currentSec > words[i].end) { activeIndex = i; break; } }
  }
  const chunkSize = vertical ? 4 : 6;
  const chunkIndex = activeIndex >= 0 ? Math.floor(activeIndex / chunkSize) : 0;
  const chunk = words.slice(chunkIndex * chunkSize, (chunkIndex + 1) * chunkSize);

  return (
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: vertical ? 220 : 64, display: 'flex', justifyContent: 'center', zIndex: 30, pointerEvents: 'none' }}>
      <div style={{ ...box, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center', gap: 10 }}>
        {chunk.map((w, idx) => {
          const g = chunkIndex * chunkSize + idx;
          const isActive = g === activeIndex;
          const isPast = g < activeIndex;
          return (
            <span key={g} style={{
              fontSize: wordSize, fontWeight: 800, lineHeight: 1.25, padding: '2px 8px', borderRadius: 8,
              color: isActive ? '#0a0a0a' : isPast ? '#ffffff' : 'rgba(255,255,255,0.55)',
              background: isActive ? '#facc15' : 'transparent',
              transform: isActive ? 'scale(1.06)' : 'none',
            }}>{w.word}</span>
          );
        })}
      </div>
    </div>
  );
};

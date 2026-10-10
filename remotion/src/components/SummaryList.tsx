import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { SummaryListProps } from '../types';
import { useTheme } from '../ThemeContext';

// Recap: items stagger in, each with a green check (light) or cyan check (dark).
export const SummaryList: React.FC<SummaryListProps & { aspectRatio: '9:16' | '16:9' }> = ({ title, items, aspectRatio }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const entrance = spring({ frame, fps, config: { damping: 14, mass: 0.9 } });
  const vertical = aspectRatio === '9:16';
  const light = t.name === 'light-grid';

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8 relative z-10"
      style={{ transform: `scale(${interpolate(entrance, [0, 1], [0.92, 1])})`, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      <h2 className="font-black tracking-tight text-6xl mb-10 text-center" style={{ color: t.text }}>{title}</h2>
      <div className={`w-full flex flex-col gap-4 ${vertical ? 'max-w-[940px] w-[94%]' : 'max-w-5xl'}`}>
        {items.map((item, idx) => {
          const s = spring({ frame: frame - idx * 8, fps, config: { damping: 12 } });
          return (
            <div key={idx} className={`rounded-2xl flex items-center ${vertical ? 'p-6 gap-5' : 'p-4 gap-4'}`}
              style={{
                opacity: interpolate(s, [0, 1], [0, 1]),
                transform: `translateX(${interpolate(s, [0, 1], [-20, 0])}px)`,
                background: t.card,
                border: `1px solid ${t.cardBorder}`,
                boxShadow: light ? '0 6px 18px rgba(15,23,42,0.06)' : 'none',
              }}>
              <div className={`rounded-xl flex items-center justify-center shrink-0 font-bold ${vertical ? 'w-10 h-10 text-xl' : 'w-12 h-12 text-2xl'}`}
                style={{ background: t.okBg, color: t.okText }}>✓</div>
              <p className={`font-medium leading-snug ${vertical ? 'text-xl' : 'text-3xl'}`} style={{ color: t.text }}>{item}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

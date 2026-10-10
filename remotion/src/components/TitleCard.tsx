import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TitleCardProps } from '../types';
import { useTheme } from '../ThemeContext';

// Light: black pill badge + bold heading. Dark: vdo cyan glow look.
export const TitleCard: React.FC<TitleCardProps & { aspectRatio: '9:16' | '16:9' }> = ({
  title, subtitle, badge = 'AI & ENGINEERING', tags = [], aspectRatio,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const entrance = spring({ frame, fps, config: { damping: 14, mass: 0.8 } });
  const scale = interpolate(entrance, [0, 1], [0.85, 1]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);
  const vertical = aspectRatio === '9:16';
  const light = t.name === 'light-grid';

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8 relative z-10 text-center"
      style={{ transform: `scale(${scale})`, opacity }}>
      <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full font-mono text-sm tracking-wider uppercase mb-6"
        style={{ background: t.pillBg, color: t.pillText, border: light ? 'none' : `1px solid ${t.cardBorder}`,
          fontWeight: 700 }}>
        <span>{badge}</span>
      </div>

      <h1 className={`font-black tracking-tight leading-tight max-w-4xl ${vertical ? 'text-5xl md:text-6xl px-2' : 'text-6xl md:text-7xl'}`}
        style={light
          ? { color: t.text }
          : { background: `linear-gradient(90deg, #fff, #cffafe, ${t.accent})`, WebkitBackgroundClip: 'text', color: 'transparent' }}>
        {title}
      </h1>

      {subtitle && (
        <p className={`font-medium max-w-2xl mt-6 leading-relaxed ${vertical ? 'text-xl' : 'text-2xl'}`}
          style={{ color: t.textMuted }}>
          {subtitle}
        </p>
      )}

      {tags && tags.length > 0 && (
        <div className="flex flex-wrap items-center justify-center gap-2.5 mt-8 max-w-xl">
          {tags.map((tag, i) => (
            <span key={i} className="px-3 py-1 rounded-lg font-mono text-xs tracking-wide"
              style={{ background: t.card, border: `1px solid ${t.cardBorder}`, color: t.accent }}>
              #{tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

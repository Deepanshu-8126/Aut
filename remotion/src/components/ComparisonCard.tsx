import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { ComparisonCardProps } from '../types';
import { useTheme } from '../ThemeContext';

// Two cards (List vs Generator style). Right card highlighted with the accent + green badge.
export const ComparisonCard: React.FC<ComparisonCardProps & { aspectRatio: '9:16' | '16:9' }> = ({
  title, leftTitle, leftPoints, rightTitle, rightPoints, aspectRatio,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const entrance = spring({ frame, fps, config: { damping: 14, mass: 0.9 } });
  const vertical = aspectRatio === '9:16';
  const light = t.name === 'light-grid';

  const card = (highlight: boolean): React.CSSProperties => ({
    flex: 1,
    padding: 24,
    borderRadius: 24,
    background: highlight && !light ? t.accentSoft : t.card,
    border: `${highlight ? 2 : 1}px solid ${highlight ? t.accent : t.cardBorder}`,
    boxShadow: light ? '0 8px 24px rgba(15,23,42,0.06)' : 'none',
  });

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8 relative z-10"
      style={{ transform: `scale(${interpolate(entrance, [0, 1], [0.92, 1])})`, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      <h2 className="font-black tracking-tight mb-10 text-center text-6xl" style={{ color: t.text }}>{title}</h2>

      <div className={`flex gap-5 w-full ${vertical ? 'flex-col max-w-[940px] w-[94%]' : 'flex-row max-w-6xl'}`}>
        <div className="flex flex-col" style={card(false)}>
          <div className="flex items-center gap-2.5 mb-3 pb-3" style={{ borderBottom: `1px solid ${t.cardBorder}` }}>
            <div className="w-3 h-3 rounded-full" style={{ background: '#f87171' }} />
            <h3 className={`font-bold ${vertical ? 'text-2xl' : 'text-4xl'}`} style={{ color: t.text }}>{leftTitle}</h3>
          </div>
          <ul className="space-y-2.5">
            {leftPoints.map((p, i) => (
              <li key={i} className={`flex items-start gap-3 ${vertical ? 'text-lg' : 'text-3xl'}`} style={{ color: t.textMuted }}>
                <span className="mt-2 w-2 h-2 rounded-full shrink-0" style={{ background: '#f87171' }} />
                <span>{p}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="flex flex-col" style={card(true)}>
          <div className="flex items-center gap-2.5 mb-3 pb-3" style={{ borderBottom: `1px solid ${t.cardBorder}` }}>
            <span className="px-3 py-1 rounded-full text-xl font-bold" style={{ background: t.okBg, color: t.okText }}>
              {rightTitle}
            </span>
          </div>
          <ul className="space-y-2.5">
            {rightPoints.map((p, i) => (
              <li key={i} className={`flex items-start gap-3 font-medium ${vertical ? 'text-lg' : 'text-3xl'}`} style={{ color: t.text }}>
                <span className="mt-1 font-bold" style={{ color: t.okText }}>✓</span>
                <span>{p}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

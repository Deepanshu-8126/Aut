import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { getTheme, ThemeName } from '../theme';

export const Background: React.FC<{ aspectRatio: '9:16' | '16:9'; theme?: ThemeName }> = ({ aspectRatio, theme }) => {
  const frame = useCurrentFrame();
  const t = getTheme(theme);

  if (t.name === 'light-grid') {
    // White page with a fine grid, like the reference videos
    return (
      <div className="absolute inset-0 w-full h-full overflow-hidden" style={{
        background: t.bg,
        backgroundImage: `linear-gradient(${t.gridLine} 1px, transparent 1px), linear-gradient(90deg, ${t.gridLine} 1px, transparent 1px)`,
        backgroundSize: aspectRatio === '9:16' ? '48px 48px' : '60px 60px',
      }} />
    );
  }

  // dark-vdo: original vdo look (grid + floating glows)
  const glowY = interpolate(frame, [0, 300], [0, 40], { extrapolateRight: 'wrap' });
  const glowX = interpolate(frame, [0, 300], [0, -30], { extrapolateRight: 'wrap' });
  return (
    <div className="absolute inset-0 w-full h-full overflow-hidden" style={{ background: t.bg }}>
      <div className="absolute inset-0 opacity-[0.07]" style={{
        backgroundImage: `linear-gradient(to right, #38bdf8 1px, transparent 1px), linear-gradient(to bottom, #38bdf8 1px, transparent 1px)`,
        backgroundSize: aspectRatio === '9:16' ? '40px 40px' : '60px 60px',
      }} />
      <div className="absolute w-[600px] h-[600px] rounded-full blur-[140px] pointer-events-none opacity-20" style={{
        background: 'radial-gradient(circle, #38bdf8 0%, rgba(56,189,248,0) 70%)',
        top: -100, right: -100, transform: `translate(${glowX}px, ${glowY}px)`,
      }} />
      <div className="absolute w-[600px] h-[600px] rounded-full blur-[150px] pointer-events-none opacity-25" style={{
        background: 'radial-gradient(circle, #818cf8 0%, rgba(129,140,248,0) 70%)',
        bottom: -100, left: -100, transform: `translate(${-glowX}px, ${-glowY}px)`,
      }} />
    </div>
  );
};

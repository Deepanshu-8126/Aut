import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { OutroCardProps } from '../types';
import { useTheme } from '../ThemeContext';

// Closing card. No default handle: set your own in the project JSON.
export const OutroCard: React.FC<OutroCardProps & { aspectRatio: '9:16' | '16:9' }> = ({
  title = 'Thanks for Watching!', subtitle, twitterHandle, youtubePrompt = 'Like & Subscribe', aspectRatio,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const entrance = spring({ frame, fps, config: { damping: 14, mass: 0.8 } });
  const pulse = Math.sin(frame / 6) * 0.08 + 1;

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8 relative z-10 text-center"
      style={{ transform: `scale(${interpolate(entrance, [0, 1], [0.88, 1])})`, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      <div className="inline-block px-5 py-2 rounded-full font-bold text-lg mb-6 uppercase tracking-wider"
        style={{ background: t.pillBg, color: t.pillText, transform: `scale(${pulse})` }}>{youtubePrompt}</div>
      <h2 className={`font-black tracking-tight ${aspectRatio === '9:16' ? 'text-5xl' : 'text-6xl'}`} style={{ color: t.text }}>{title}</h2>
      {subtitle && <p className="text-2xl mt-6 max-w-2xl" style={{ color: t.textMuted }}>{subtitle}</p>}
      {twitterHandle && <p className="font-mono text-xl mt-8" style={{ color: t.accent }}>{twitterHandle}</p>}
    </div>
  );
};

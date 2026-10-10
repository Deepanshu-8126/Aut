import React from 'react';
import { OffthreadVideo, staticFile, useCurrentFrame, interpolate } from 'remotion';
import { useTheme } from '../ThemeContext';

// Manim ka clip. Clip ka white background grid mein multiply se mil jaata hai (koi white box nahi).
export const ManimClip: React.FC<{ src: string; heading?: string; aspectRatio: '9:16' | '16:9' }> = ({ src, heading, aspectRatio }) => {
  const t = useTheme();
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: 'clamp' });
  const vertical = aspectRatio === '9:16';
  return (
    <div className="w-full h-full relative" style={{ opacity }}>
      {heading && (
        <h2 className={`absolute left-0 right-0 text-center font-black tracking-tight ${vertical ? 'text-4xl top-24' : 'text-5xl top-12'}`}
          style={{ color: t.text }}>{heading}</h2>
      )}
      <div className="absolute inset-0 flex items-center justify-center" style={{ paddingTop: vertical ? 140 : 80 }}>
        <OffthreadVideo src={staticFile(src)} muted style={{ mixBlendMode: 'multiply', width: vertical ? '94%' : 'auto', height: vertical ? 'auto' : '62%' }} />
      </div>
    </div>
  );
};

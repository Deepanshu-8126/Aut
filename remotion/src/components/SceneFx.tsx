import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';

// Scene ke andar smooth fade-in (local frame). Scene switch ko soft banata hai.
export const SceneFade: React.FC<{ children: React.ReactNode; frames?: number }> = ({ children, frames = 12 }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, frames], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const y = interpolate(f, [0, frames], [10, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return <div style={{ width: '100%', height: '100%', opacity: o, transform: `translateY(${y}px)` }}>{children}</div>;
};

// Video ke upar thin progress bar + kaun sa scene chal raha hai (global frame).
export const GlobalProgress: React.FC<{ totalFrames: number }> = ({ totalFrames }) => {
  const f = useCurrentFrame();
  const t = useTheme();
  const pct = Math.min(100, (f / Math.max(1, totalFrames)) * 100);
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, top: 0, height: 6, background: 'rgba(15,23,42,0.08)', zIndex: 60 }}>
      <div style={{ width: `${pct}%`, height: '100%', background: t.accent, borderRadius: '0 3px 3px 0' }} />
    </div>
  );
};

export const useTotalFrames = (scenes: { durationInFrames?: number }[]) => {
  const { fps } = useVideoConfig();
  void fps;
  return scenes.reduce((a, s) => a + (s.durationInFrames || 90), 0);
};


// Key idea card: scene ke beech mein spring se pop hota hai, ek line ka takeaway.
export const KeyIdea: React.FC<{ text: string; delaySec?: number }> = ({ text, delaySec = 1.2 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const start = Math.round(delaySec * fps);
  const local = Math.max(0, f - start);
  const pop = spring({ frame: local, fps, config: { damping: 11, mass: 0.7 } });
  const scale = interpolate(pop, [0, 1], [0.6, 1]);
  return (
    <div style={{
      position: 'absolute', top: 40, right: 48, zIndex: 40, maxWidth: 620,
      transform: `scale(${scale})`, transformOrigin: 'top right', opacity: interpolate(pop, [0, 1], [0, 1]),
      background: t.card, border: `2px solid ${t.accent}`, borderRadius: 18, padding: '14px 22px 14px 18px',
      boxShadow: `0 16px 36px -14px ${t.accent}88`, display: 'flex', alignItems: 'center', gap: 14,
    }}>
      <div style={{ width: 10, alignSelf: 'stretch', borderRadius: 5, background: t.accent }} />
      <div>
        <div style={{ fontFamily: 'monospace', fontSize: 16, fontWeight: 800, letterSpacing: 2, color: t.accent }}>KEY IDEA</div>
        <div style={{ fontSize: 28, fontWeight: 700, color: t.text, lineHeight: 1.25, marginTop: 4 }}>{text}</div>
      </div>
    </div>
  );
};

// Chapter label: video ke upar-left mein module ka naam (roadmap context).
export const ChapterLabel: React.FC<{ text: string }> = ({ text }) => {
  const f = useCurrentFrame();
  const t = useTheme();
  const o = interpolate(f, [0, 10], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <div style={{
      position: 'absolute', top: 30, left: 44, zIndex: 40, opacity: o,
      fontFamily: 'monospace', fontSize: 20, fontWeight: 800, letterSpacing: 2, color: t.textMuted,
      background: 'rgba(255,255,255,0.9)', border: `1px solid ${t.cardBorder}`, borderRadius: 999, padding: '6px 16px',
    }}>
      {text.toUpperCase()}
    </div>
  );
};

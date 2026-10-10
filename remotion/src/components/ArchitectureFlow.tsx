import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { ArchitectureFlowProps } from '../types';
import { useTheme } from '../ThemeContext';

// Flow / tree / roadmap diagram. Light-grid theme mein clear, narration ke saath steps move karte hain.
// stepAt (seconds, pipeline se): har step kab active hota hai. Na ho to activeStepIndex fixed rehta hai.
export const ArchitectureFlow: React.FC<
  ArchitectureFlowProps & { aspectRatio: '9:16' | '16:9'; stepAt?: number[] }
> = ({ title, steps, activeStepIndex = 0, aspectRatio, stepAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const vertical = aspectRatio === '9:16';

  const entrance = spring({ frame, fps, config: { damping: 16, mass: 0.8 } });

  let active = activeStepIndex;
  if (stepAt && stepAt.length === steps.length) {
    const sec = frame / fps;
    active = 0;
    for (let i = 0; i < stepAt.length; i++) if (sec >= stepAt[i]) active = i;
  }

  return (
    <div
      style={{
        width: '100%', height: '100%', display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', padding: vertical ? 40 : 60,
        transform: `scale(${interpolate(entrance, [0, 1], [0.94, 1])})`,
        opacity: interpolate(entrance, [0, 1], [0, 1]),
      }}
    >
      <div style={{ fontSize: vertical ? 56 : 52, fontWeight: 900, color: t.text, letterSpacing: -1, marginBottom: vertical ? 50 : 44, textAlign: 'center' }}>
        {title}
      </div>

      <div style={{
        display: 'flex', flexDirection: vertical ? 'column' : 'row', alignItems: 'center',
        justifyContent: 'center', gap: vertical ? 14 : 40, width: '100%',
      }}>
        {steps.map((step, idx) => {
          const isActive = idx === active;
          const isDone = idx < active;
          const isPending = idx > active;
          const cardW = vertical ? '92%' : 340;
          const border = isActive ? t.accent : isDone ? '#86efac' : t.cardBorder;
          return (
            <React.Fragment key={idx}>
              <div style={{
                position: 'relative', width: cardW, minHeight: vertical ? 120 : 230, padding: vertical ? '18px 16px' : '40px 22px 26px',
                boxSizing: 'border-box', borderRadius: 22, background: isActive ? t.accentSoft : t.card,
                border: `3px solid ${border}`,
                boxShadow: isActive ? `0 18px 40px -12px ${t.accent}66` : '0 6px 16px rgba(15,23,42,0.06)',
                opacity: isPending ? 0.45 : 1,
                transform: isActive ? 'scale(1.06)' : 'scale(1)',
                transition: 'none',
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center',
              }}>
                <div style={{
                  position: 'absolute', top: -16, left: 18, background: isDone ? '#16a34a' : isActive ? t.accent : '#9ca3af',
                  color: '#fff', fontFamily: 'monospace', fontSize: vertical ? 18 : 24, fontWeight: 800, borderRadius: 999, padding: '4px 12px',
                }}>
                  {isDone ? 'DONE' : `STEP ${idx + 1}`}
                </div>
                <div style={{ fontSize: vertical ? 34 : 40, fontWeight: 800, color: t.text, lineHeight: 1.15 }}>{step.title}</div>
                {step.desc && (
                  <div style={{ marginTop: 10, fontSize: vertical ? 24 : 29, color: t.textMuted, lineHeight: 1.3 }}>{step.desc}</div>
                )}
              </div>

              {idx < steps.length - 1 && (
                <div style={{ position: 'relative', width: vertical ? 4 : 72, height: vertical ? 40 : 4,
                  background: isDone ? '#86efac' : '#d1d5db', borderRadius: 2, flexShrink: 0 }}>
                  {isDone && (
                    // Moving dot: data flow ka animation
                    <div style={{
                      position: 'absolute', width: 12, height: 12, borderRadius: 6, background: t.accent,
                      top: vertical ? `${(frame % 24) / 24 * 100}%` : -4,
                      left: vertical ? -4 : `${(frame % 24) / 24 * 100}%`,
                    }} />
                  )}
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

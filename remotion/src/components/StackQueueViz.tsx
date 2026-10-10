import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';
import { activeStepIndex } from './stepUtil';

// Stack / Queue visual. kind: "stack" | "queue".
// steps: [{ at?, op: "push"|"pop"|"enqueue"|"dequeue", value?, label }]  (state har step par apply hota hai)
export interface SQStep { at?: string; op: 'push' | 'pop' | 'enqueue' | 'dequeue'; value?: string | number; label: string }
export interface StackQueueVizProps { title: string; kind: 'stack' | 'queue'; steps: SQStep[] }

export const StackQueueViz: React.FC<StackQueueVizProps & { aspectRatio: '9:16' | '16:9'; stepAt?: number[] }> = ({
  title, kind, steps, aspectRatio, stepAt,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const vertical = aspectRatio === '9:16';
  const entrance = spring({ frame, fps, config: { damping: 18 } });
  const idx = activeStepIndex(steps.length, stepAt, frame / fps);

  // state banao: steps[0..idx] apply karo
  const items: (string | number)[] = [];
  let lastOp: SQStep | undefined;
  for (let i = 0; i <= idx && i < steps.length; i++) {
    const s = steps[i]; lastOp = s;
    if ((s.op === 'push' || s.op === 'enqueue') && s.value !== undefined) items.push(s.value);
    if (s.op === 'pop') items.pop();
    if (s.op === 'dequeue') items.shift();
  }
  const isStack = kind === 'stack';
  const ITEM = vertical ? 120 : 130;

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      padding: vertical ? 40 : 60, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      <div style={{ fontSize: 52, fontWeight: 900, color: t.text, marginBottom: 16, textAlign: 'center' }}>{title}</div>
      {steps[idx] && (
        <div style={{ marginBottom: 24, background: t.okBg, color: t.okText, padding: '12px 24px', borderRadius: 14,
          fontSize: 30, fontWeight: 700, maxWidth: vertical ? 900 : 1400, textAlign: 'center' }}>{steps[idx].label}</div>
      )}

      {isStack ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, minHeight: 3 * ITEM }}>
          {items.length > 0 && <div style={{ fontSize: 26, color: t.textMuted, marginBottom: 6 }}>TOP ↑</div>}
          {items.length === 0 && <div style={{ fontSize: 34, color: t.textMuted }}>(khali)</div>}
          {/* top item sabse upar dikhta hai; array ko ulta render karte hain */}
          {[...items].reverse().map((v, i) => {
            const isTop = i === 0;
            return (
              <div key={i} style={{ width: 300, height: ITEM * 0.7, borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: isTop ? t.accent : t.card, color: isTop ? '#fff' : t.text,
                border: `3px solid ${isTop ? t.accent : t.cardBorder}`, fontSize: 44, fontWeight: 800, fontFamily: 'monospace' }}>{String(v)}</div>
            );
          })}
          <div style={{ width: 300, height: 8, background: t.textMuted, borderRadius: 4, marginTop: 6 }} />
        </div>
      ) : (
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div style={{ fontSize: 26, color: t.textMuted, marginRight: 8 }}>FRONT</div>
          {items.length === 0 && <div style={{ fontSize: 34, color: t.textMuted }}>(khali)</div>}
          {items.map((v, i) => (
            <div key={i} style={{ width: ITEM * 0.9, height: ITEM * 0.9, borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: i === 0 ? t.accent : t.card, color: i === 0 ? '#fff' : t.text,
              border: `3px solid ${i === 0 ? t.accent : t.cardBorder}`, fontSize: 44, fontWeight: 800, fontFamily: 'monospace' }}>{String(v)}</div>
          ))}
          <div style={{ fontSize: 26, color: t.textMuted, marginLeft: 8 }}>BACK</div>
        </div>
      )}

      {lastOp && (
        <div style={{ marginTop: 34, fontSize: 30, fontWeight: 800, color: t.accent, fontFamily: 'monospace' }}>
          {lastOp.op}{lastOp.value !== undefined ? `(${lastOp.value})` : '()'}
        </div>
      )}
    </div>
  );
};

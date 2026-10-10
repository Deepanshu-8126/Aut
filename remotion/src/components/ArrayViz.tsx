import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';
import { activeStepIndex } from './stepUtil';

// Array visual: values boxes, index neeche, pointers (left/right) aur sliding window ka highlight.
// steps: [{ at?, label, pointers?: {name: index}, window?: [l, r], highlight?: [indices], compare?: [i, j] }]
export interface ArrayStep {
  at?: string;
  label: string;
  pointers?: Record<string, number>;
  window?: [number, number];
  highlight?: number[];
  compare?: [number, number];
}
export interface ArrayVizProps {
  title: string;
  values: (string | number)[];
  steps: ArrayStep[];
}

export const ArrayViz: React.FC<ArrayVizProps & { aspectRatio: '9:16' | '16:9'; stepAt?: number[] }> = ({
  title, values, steps, aspectRatio, stepAt,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const vertical = aspectRatio === '9:16';
  const entrance = spring({ frame, fps, config: { damping: 18 } });
  const idx = activeStepIndex(steps.length, stepAt, frame / fps);
  const st: ArrayStep | undefined = steps[idx];
  const n = values.length;
  const cell = vertical ? Math.min(110, 760 / Math.max(n, 1)) : Math.min(150, 1400 / Math.max(n, 1));
  const gap = 10;
  const inWin = (i: number) => !!st?.window && i >= st.window[0] && i <= st.window[1];
  const hi = (i: number) => !!st?.highlight?.includes(i) || (!!st?.compare && st.compare.includes(i));

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      padding: vertical ? 40 : 60, opacity: interpolate(entrance, [0, 1], [0, 1]), transform: `scale(${interpolate(entrance, [0, 1], [0.95, 1])})` }}>
      <div style={{ fontSize: vertical ? 52 : 52, fontWeight: 900, color: t.text, marginBottom: 40, textAlign: 'center' }}>{title}</div>

      <div style={{ position: 'relative', display: 'flex', gap, alignItems: 'flex-end' }}>
        {/* sliding window band */}
        {st?.window && (
          <div style={{ position: 'absolute', top: -58, height: 44, left: st.window[0] * (cell + gap) - 6,
            width: (st.window[1] - st.window[0] + 1) * (cell + gap) - gap + 12, borderRadius: 12,
            border: `3px dashed ${t.accent}`, background: `${t.accent}14`, boxSizing: 'border-box' }} />
        )}
        {values.map((v, i) => (
          <div key={i} style={{ width: cell, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{
              width: cell, height: cell * 0.8, borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: Math.min(56, cell * 0.38), fontWeight: 800, fontFamily: 'monospace',
              background: hi(i) ? t.accent : inWin(i) ? t.accentSoft : t.card,
              color: hi(i) ? '#fff' : t.text, border: `3px solid ${hi(i) ? t.accent : t.cardBorder}`,
              boxShadow: hi(i) ? `0 12px 28px -10px ${t.accent}` : '0 4px 10px rgba(15,23,42,0.06)',
            }}>{String(v)}</div>
            <div style={{ marginTop: 8, fontSize: 24, color: t.textMuted, fontFamily: 'monospace' }}>{i}</div>
          </div>
        ))}
      </div>

      {/* pointers */}
      <div style={{ position: 'relative', width: n * (cell + gap), height: 90, marginTop: 6 }}>
        {Object.entries(st?.pointers ?? {}).map(([name, i]) => (
          <div key={name} style={{ position: 'absolute', left: i * (cell + gap) + cell / 2 - 40, top: 0, width: 80, textAlign: 'center' }}>
            <div style={{ fontSize: 22, fontWeight: 800, color: t.accent }}>▲</div>
            <div style={{ fontSize: 22, fontWeight: 800, color: t.accent }}>{name}</div>
          </div>
        ))}
      </div>

      {st && (
        <div style={{ marginTop: 30, background: t.okBg, color: t.okText, padding: '14px 26px', borderRadius: 14,
          fontSize: 30, fontWeight: 700, maxWidth: vertical ? 900 : 1400, textAlign: 'center' }}>{st.label}</div>
      )}
    </div>
  );
};

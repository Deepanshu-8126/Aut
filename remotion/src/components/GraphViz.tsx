import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';
import { activeStepIndex } from './stepUtil';

// Graph visual (BFS/DFS). nodes: [{id, label}], edges: [[a, b]].
// steps: [{ at?, label, current?, visited?: ids, queue?: ids, stack?: ids }]
export interface GraphNode { id: string; label: string }
export interface GraphStep { at?: string; label: string; current?: string; visited?: string[]; queue?: string[]; stack?: string[] }
export interface GraphVizProps { title: string; nodes: GraphNode[]; edges: [string, string][]; steps: GraphStep[] }

export const GraphViz: React.FC<GraphVizProps & { aspectRatio: '9:16' | '16:9'; stepAt?: number[] }> = ({
  title, nodes, edges, steps, aspectRatio, stepAt,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const vertical = aspectRatio === '9:16';
  const entrance = spring({ frame, fps, config: { damping: 18 } });
  const idx = activeStepIndex(steps.length, stepAt, frame / fps);
  const st = steps[idx];

  const W = vertical ? 900 : 1000, H = vertical ? 900 : 620;
  const cx = W / 2, cy = H / 2, rad = Math.min(W, H) * 0.36;
  const pos = new Map<string, { x: number; y: number }>();
  nodes.forEach((n, i) => {
    const a = (2 * Math.PI * i) / nodes.length - Math.PI / 2;
    pos.set(n.id, { x: cx + rad * Math.cos(a), y: cy + rad * Math.sin(a) });
  });
  const visited = new Set(st?.visited ?? []);
  const R = 50;

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      padding: vertical ? 30 : 50, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      <div style={{ fontSize: 52, fontWeight: 900, color: t.text, marginBottom: 16, textAlign: 'center' }}>{title}</div>
      <div style={{ display: 'flex', gap: 40, alignItems: 'center' }}>
        <svg width={W} height={H}>
          {edges.map(([a, b], i) => {
            const p = pos.get(a), q = pos.get(b); if (!p || !q) return null;
            const active = st?.current && (st.current === a || st.current === b) && visited.has(a) && visited.has(b);
            return <line key={i} x1={p.x} y1={p.y} x2={q.x} y2={q.y} stroke={active ? t.accent : t.cardBorder} strokeWidth={active ? 7 : 4} />;
          })}
          {nodes.map((n) => {
            const p = pos.get(n.id)!;
            const isCur = st?.current === n.id, isVis = visited.has(n.id);
            return (
              <g key={n.id}>
                <circle cx={p.x} cy={p.y} r={R} fill={isCur ? t.accent : isVis ? t.accentSoft : t.card} stroke={isCur ? t.accent : t.cardBorder} strokeWidth={4} />
                <text x={p.x} y={p.y + 12} textAnchor="middle" fontSize={34} fontWeight={800} fill={isCur ? '#fff' : t.text}>{n.label}</text>
              </g>
            );
          })}
        </svg>
        {!vertical && (st?.queue || st?.stack) && (
          <div style={{ minWidth: 260, display: 'flex', flexDirection: 'column', gap: 18 }}>
            {st?.queue && (
              <div style={{ background: t.card, border: `2px solid ${t.cardBorder}`, borderRadius: 16, padding: 18 }}>
                <div style={{ fontSize: 24, fontWeight: 800, color: t.textMuted }}>QUEUE (BFS)</div>
                <div style={{ fontSize: 34, fontFamily: 'monospace', color: t.text }}>{st.queue.join(' → ') || '(khali)'}</div>
              </div>
            )}
            {st?.stack && (
              <div style={{ background: t.card, border: `2px solid ${t.cardBorder}`, borderRadius: 16, padding: 18 }}>
                <div style={{ fontSize: 24, fontWeight: 800, color: t.textMuted }}>STACK (DFS)</div>
                <div style={{ fontSize: 34, fontFamily: 'monospace', color: t.text }}>{st.stack.join(' | ') || '(khali)'}</div>
              </div>
            )}
            <div style={{ background: t.card, border: `2px solid ${t.cardBorder}`, borderRadius: 16, padding: 18 }}>
              <div style={{ fontSize: 24, fontWeight: 800, color: t.textMuted }}>VISITED</div>
              <div style={{ fontSize: 34, fontFamily: 'monospace', color: t.text }}>{[...visited].join(', ') || '(none)'}</div>
            </div>
          </div>
        )}
      </div>
      {st && (
        <div style={{ marginTop: 16, background: t.okBg, color: t.okText, padding: '14px 26px', borderRadius: 14,
          fontSize: 30, fontWeight: 700, maxWidth: vertical ? 900 : 1400, textAlign: 'center' }}>{st.label}</div>
      )}
    </div>
  );
};

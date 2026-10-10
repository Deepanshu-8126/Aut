import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';
import { activeStepIndex } from './stepUtil';

// Generic boxes + animated arrows diagram. Kisi bhi topic ke liye (flow, pipeline, request path, process).
// nodes: [{id, label, sub?}]   edges: [{from, to, label?}]
// steps: [{at?, label, focus?: [nodeId], arrow?: edgeIndex}]
//   - arrow: is step par ye edge (index) animate hoke aata hai. Edges order mein dikhte hain.
//   - focus: in nodes ko highlight karo (baaki dim).
export interface DiagramNode { id: string; label: string; sub?: string }
export interface DiagramEdge { from: string; to: string; label?: string }
export interface DiagramStep { at?: string; label: string; focus?: string[]; arrow?: number }
export interface DiagramFlowProps { title: string; nodes: DiagramNode[]; edges: DiagramEdge[]; steps: DiagramStep[] }

export const DiagramFlow: React.FC<DiagramFlowProps & { aspectRatio: '9:16' | '16:9'; stepAt?: number[] }> = ({
  title, nodes, edges, steps, aspectRatio, stepAt,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const vertical = aspectRatio === '9:16';
  const entrance = spring({ frame, fps, config: { damping: 18 } });
  const sec = frame / fps;
  const idx = activeStepIndex(steps.length, stepAt, sec);
  const cur = steps[idx];

  // Layout: 16:9 mein ek row, 9:16 mein ek column. Zyada nodes ho to grid (3 per row).
  const W = vertical ? 900 : 1500;
  const H = vertical ? 1000 : 600;
  const n = Math.max(1, nodes.length);
  const perRow = vertical ? 1 : Math.min(n, 4);
  const rows = Math.ceil(n / perRow);
  const BW = vertical ? 620 : 300, BH = vertical ? 130 : 130;
  const pos = new Map<string, { x: number; y: number }>();
  nodes.forEach((nd, i) => {
    const r = Math.floor(i / perRow), c = i % perRow;
    const inRow = Math.min(perRow, n - r * perRow);
    const x = ((c + 0.5) / inRow) * W;
    const y = ((r + 0.5) / rows) * H;
    pos.set(nd.id, { x, y });
  });

  // Arrows: step ke "arrow" tak ke sab edges visible; current edge ka progress animate hota hai.
  const revealed = new Set<number>();
  for (let i = 0; i <= idx && i < steps.length; i++) {
    if (typeof steps[i].arrow === 'number') revealed.add(steps[i].arrow as number);
  }
  const curArrow = typeof cur?.arrow === 'number' ? cur.arrow : -1;
  const stepStart = stepAt && stepAt.length === steps.length ? stepAt[idx] : 0;
  const drawProgress = curArrow >= 0
    ? interpolate(sec - stepStart, [0, 0.6], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : 1;
  const focus = new Set(cur?.focus ?? []);
  const hasFocus = focus.size > 0;

  // Line box ke border se shuru/khatam ho (center se nahi), taaki arrowhead box ke andar na chhupe
  const edgePoint = (from: { x: number; y: number }, to: { x: number; y: number }) => {
    const dx = to.x - from.x, dy = to.y - from.y;
    const len = Math.hypot(dx, dy) || 1;
    const hw = BW / 2 + 2, hh = BH / 2 + 2;
    // distance jahan line box ki boundary cross karti hai
    const dAlongX = Math.abs(dx) > 0.001 ? (hw * len) / Math.abs(dx) : Infinity;
    const dAlongY = Math.abs(dy) > 0.001 ? (hh * len) / Math.abs(dy) : Infinity;
    const k = Math.min(dAlongX, dAlongY, len);
    return { x: from.x + (dx / len) * k, y: from.y + (dy / len) * k };
  };

  const nodeBox = (nd: DiagramNode) => {
    const p = pos.get(nd.id)!;
    const on = !hasFocus || focus.has(nd.id);
    return (
      <div key={nd.id} style={{
        position: 'absolute', left: p.x - BW / 2, top: p.y - BH / 2, width: BW, height: BH,
        borderRadius: 16, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        background: on && hasFocus ? t.accent : t.card,
        color: on && hasFocus ? '#fff' : on ? t.text : t.textMuted,
        border: `3px solid ${on && hasFocus ? t.accent : t.cardBorder}`, zIndex: 1,
        boxShadow: on && hasFocus ? `0 8px 24px ${t.accentSoft}` : 'none',
        fontWeight: 800, textAlign: 'center', padding: '0 12px',
      }}>
        <div style={{ fontSize: 34 }}>{nd.label}</div>
        {nd.sub && <div style={{ fontSize: 22, fontWeight: 600, opacity: 0.8, marginTop: 4 }}>{nd.sub}</div>}
      </div>
    );
  };

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      padding: vertical ? 40 : 50, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      <div style={{ fontSize: 52, fontWeight: 900, color: t.text, marginBottom: 16, textAlign: 'center' }}>{title}</div>
      {cur && (
        <div style={{ marginBottom: 16, background: t.okBg, color: t.okText, padding: '12px 24px', borderRadius: 14,
          fontSize: 30, fontWeight: 700, maxWidth: vertical ? 900 : 1400, textAlign: 'center' }}>{cur.label}</div>
      )}
      <div style={{ position: 'relative', width: W, height: H }}>
        {nodes.map(nodeBox)}
        <svg width={W} height={H} style={{ position: 'absolute', left: 0, top: 0, overflow: 'visible', zIndex: 2, pointerEvents: 'none' }}>
          <defs>
            <marker id="df-arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
              <path d="M0,0 L12,6 L0,12 z" fill={t.accent} />
            </marker>
          </defs>
          {edges.map((e, i) => {
            const pa = pos.get(e.from), pb = pos.get(e.to);
            if (!pa || !pb || !(revealed.has(i) || i === curArrow)) return null;
            const isCur = i === curArrow;
            const a = edgePoint(pa, pb);
            const b = edgePoint(pb, pa);
            const x2 = isCur ? a.x + (b.x - a.x) * drawProgress : b.x;
            const y2 = isCur ? a.y + (b.y - a.y) * drawProgress : b.y;
            const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
            return (
              <g key={'e' + i}>
                <line x1={a.x} y1={a.y} x2={x2} y2={y2} stroke={t.accent} strokeWidth={5} />
                {(!isCur || drawProgress > 0.95) && (() => {
                  const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1;
                  const ux = dx / L, uy = dy / L, px2 = -uy, py2 = ux, AH = 22, AW = 11;
                  const bx = b.x - ux * AH, by = b.y - uy * AH;
                  return <polygon points={`${b.x},${b.y} ${bx + px2 * AW},${by + py2 * AW} ${bx - px2 * AW},${by - py2 * AW}`} fill={t.accent} />;
                })()}
                {e.label && (!isCur || drawProgress > 0.9) && (
                  <text x={mx} y={my - 12} textAnchor="middle" fontSize={24} fontWeight={700} fill={t.textMuted}>{e.label}</text>
                )}
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
};

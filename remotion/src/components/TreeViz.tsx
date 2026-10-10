import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';
import { activeStepIndex } from './stepUtil';

// Binary tree visual. nodes: [{id, value, left?, right?}], root: id.
// steps: [{ at?, label, visit?: id (is step par visited/current), }] - visited set steps ke saath jama hota jata hai.
export interface TreeNode { id: string; value: string | number; left?: string; right?: string }
export interface TreeStep { at?: string; label: string; visit?: string }
export interface TreeVizProps { title: string; root: string; nodes: TreeNode[]; steps: TreeStep[] }

export const TreeViz: React.FC<TreeVizProps & { aspectRatio: '9:16' | '16:9'; stepAt?: number[] }> = ({
  title, root, nodes, steps, aspectRatio, stepAt,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const vertical = aspectRatio === '9:16';
  const entrance = spring({ frame, fps, config: { damping: 18 } });
  const idx = activeStepIndex(steps.length, stepAt, frame / fps);
  const byId = new Map(nodes.map((n) => [n.id, n]));

  // layout: inorder x, depth y (fraction 0..1)
  const pos = new Map<string, { x: number; y: number }>();
  let counter = 0;
  const maxDepth = { d: 0 };
  const walk = (id: string | undefined, depth: number) => {
    if (!id || !byId.has(id)) return;
    maxDepth.d = Math.max(maxDepth.d, depth);
    walk(byId.get(id)!.left, depth + 1);
    pos.set(id, { x: counter++, y: depth });
    walk(byId.get(id)!.right, depth + 1);
  };
  walk(root, 0);
  const cols = Math.max(1, counter);
  const W = vertical ? 900 : 1500, H = vertical ? 1100 : 640;
  const px = (x: number) => ((x + 0.5) / cols) * W;
  const py = (y: number) => 60 + (y / (maxDepth.d + 1)) * (H - 120) + 40;

  const visited = new Set<string>();
  for (let i = 0; i <= idx && i < steps.length; i++) if (steps[i].visit) visited.add(steps[i].visit!);
  const cur = steps[idx]?.visit;
  const R = vertical ? 34 : 38;

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      padding: vertical ? 40 : 50, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      <div style={{ fontSize: 52, fontWeight: 900, color: t.text, marginBottom: 16, textAlign: 'center' }}>{title}</div>
      {steps[idx] && (
        <div style={{ marginBottom: 16, background: t.okBg, color: t.okText, padding: '12px 24px', borderRadius: 14,
          fontSize: 30, fontWeight: 700, maxWidth: vertical ? 900 : 1400, textAlign: 'center' }}>{steps[idx].label}</div>
      )}
      <svg width={W} height={H}>
        {nodes.map((n) => {
          const p = pos.get(n.id); if (!p) return null;
          return [n.left, n.right].map((c) => {
            const q = c && pos.get(c); if (!q) return null;
            return <line key={n.id + '-' + c} x1={px(p.x)} y1={py(p.y)} x2={px(q.x)} y2={py(q.y)} stroke={t.cardBorder} strokeWidth={4} />;
          });
        })}
        {nodes.map((n) => {
          const p = pos.get(n.id); if (!p) return null;
          const isCur = cur === n.id, isVis = visited.has(n.id);
          const fill = isCur ? t.accent : isVis ? t.accentSoft : t.card;
          return (
            <g key={n.id}>
              <circle cx={px(p.x)} cy={py(p.y)} r={R} fill={fill} stroke={isCur ? t.accent : t.cardBorder} strokeWidth={4} />
              <text x={px(p.x)} y={py(p.y) + 10} textAnchor="middle" fontSize={30} fontWeight={800}
                fill={isCur ? '#fff' : t.text} fontFamily="monospace">{String(n.value)}</text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

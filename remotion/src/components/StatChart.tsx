import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { useTheme } from '../ThemeContext';

// Math/stats scene: data se animated chart (bar | line | scatter) + formula card.
// Bars grow, line draws, points pop in. Style 3b1b jaisa nahi: clean data chart.
export interface StatChartProps {
  title: string;
  kind: 'bar' | 'line' | 'scatter';
  labels?: string[];          // bar/line x labels
  values?: number[];          // bar/line values
  points?: [number, number][]; // scatter
  xLabel?: string;
  yLabel?: string;
  formula?: string;           // e.g. "mean = (sum of x) / n"
  highlight?: number;         // bar index to highlight (mean/median etc)
  startFrame?: number;
  typeFrames?: number;
}

const W = 760, H = 480, PAD = 60;

export const StatChart: React.FC<StatChartProps> = ({
  title, kind, labels = [], values = [], points = [], xLabel, yLabel, formula,
  highlight, startFrame = 0, typeFrames = 90,
}) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const local = frame - startFrame;
  const p = interpolate(local, [0, typeFrames], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  const maxV = Math.max(1, ...values, ...points.map((q) => q[1]));
  const maxX = Math.max(1, ...points.map((q) => q[0]));
  const plotW = W - PAD * 2, plotH = H - PAD * 2;

  const axes = (
    <g>
      <line x1={PAD} y1={H - PAD} x2={W - PAD} y2={H - PAD} stroke={t.textMuted} strokeWidth={2} />
      <line x1={PAD} y1={PAD} x2={PAD} y2={H - PAD} stroke={t.textMuted} strokeWidth={2} />
      {xLabel && <text x={W / 2} y={H - 14} textAnchor="middle" fontSize={20} fill={t.textMuted}>{xLabel}</text>}
      {yLabel && <text x={PAD} y={PAD - 16} fontSize={20} fill={t.textMuted}>{yLabel}</text>}
    </g>
  );

  let body: React.ReactNode = null;
  if (kind === 'bar') {
    const bw = plotW / Math.max(1, values.length) * 0.6;
    body = values.map((v, i) => {
      const x = PAD + (plotW / values.length) * (i + 0.2);
      const h = (v / maxV) * plotH * p;
      const hl = highlight === i;
      return (
        <g key={i}>
          <rect x={x} y={H - PAD - h} width={bw} height={h} rx={6}
            fill={hl ? t.accent : t.accentSoft} stroke={t.cardBorder} />
          <text x={x + bw / 2} y={H - PAD - h - 10} textAnchor="middle" fontSize={20} fill={t.text}
            opacity={p > 0.6 ? 1 : 0}>{v}</text>
          <text x={x + bw / 2} y={H - PAD + 28} textAnchor="middle" fontSize={20} fill={t.textMuted}>{labels[i] ?? ''}</text>
        </g>
      );
    });
  } else if (kind === 'line') {
    const pts = values.map((v, i) => [
      PAD + (values.length > 1 ? (plotW * i) / (values.length - 1) : 0),
      H - PAD - (v / maxV) * plotH,
    ]);
    const d = pts.map((q, i) => `${i === 0 ? 'M' : 'L'}${q[0]},${q[1]}`).join(' ');
    const len = plotW * 1.6;
    body = (
      <g>
        <path d={d} fill="none" stroke={t.accent} strokeWidth={5} strokeLinejoin="round"
          strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
        {pts.map((q, i) => (
          <g key={i}>
            <circle cx={q[0]} cy={q[1]} r={7} fill={t.accent} opacity={p > i / pts.length ? 1 : 0} />
            <text x={q[0]} y={H - PAD + 28} textAnchor="middle" fontSize={20} fill={t.textMuted}>{labels[i] ?? ''}</text>
          </g>
        ))}
      </g>
    );
  } else {
    const shown = Math.floor(p * points.length);
    body = points.slice(0, shown).map((q, i) => (
      <circle key={i} cx={PAD + (q[0] / maxX) * plotW} cy={H - PAD - (q[1] / maxV) * plotH}
        r={9} fill={t.accent} opacity={0.85} />
    ));
  }

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-10 relative z-10">
      <div className="text-5xl font-extrabold mb-6" style={{ color: t.text }}>{title}</div>
      <div className="flex items-start gap-10">
        <div className="rounded-2xl p-6" style={{ background: t.card, border: `2px solid ${t.cardBorder}` }}>
          <svg width={W} height={H}>
            {axes}
            {body}
          </svg>
        </div>
        {formula && (
          <div className="rounded-2xl p-6 font-mono text-3xl max-w-xs" style={{ background: t.okBg, color: t.okText, opacity: p > 0.3 ? 1 : 0 }}>
            {formula}
          </div>
        )}
      </div>
    </div>
  );
};

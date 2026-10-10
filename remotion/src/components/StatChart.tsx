import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { useTheme } from '../ThemeContext';

// Statistics scene. kind:
//  bar        : labels + values (highlight index optional)
//  line       : labels + values (trend)
//  scatter    : points [x,y] + least-squares regression line (correlation)
//  histogram  : raw data -> bins (distribution)
//  boxplot    : raw data -> Q1, median, Q3, whiskers (1.5*IQR), outliers as dots
//  normal     : bell curve from mean & sd, shaded mean±1sd
// Animation: bars grow, line/regression draws, points pop, bell curve sweeps.

export interface StatChartProps {
  title: string;
  kind: 'bar' | 'line' | 'scatter' | 'histogram' | 'boxplot' | 'normal';
  labels?: string[];
  values?: number[];
  points?: [number, number][];
  data?: number[];           // histogram / boxplot raw values
  bins?: number;             // histogram bin count (default 6)
  mean?: number;             // normal
  sd?: number;               // normal
  showRegression?: boolean;  // scatter
  xLabel?: string;
  yLabel?: string;
  formula?: string;          // card text (monospace)
  highlight?: number;
  startFrame?: number;
  typeFrames?: number;
}

const W = 760, H = 480, PAD = 60;

const quantile = (sorted: number[], q: number) => {
  const pos = (sorted.length - 1) * q;
  const lo = Math.floor(pos), hi = Math.ceil(pos);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
};

const boxStats = (data: number[]) => {
  const s = [...data].sort((a, b) => a - b);
  const q1 = quantile(s, 0.25), med = quantile(s, 0.5), q3 = quantile(s, 0.75);
  const iqr = q3 - q1;
  const loF = q1 - 1.5 * iqr, hiF = q3 + 1.5 * iqr;
  const inside = s.filter((v) => v >= loF && v <= hiF);
  const outliers = s.filter((v) => v < loF || v > hiF);
  return { q1, med, q3, lo: Math.min(...inside), hi: Math.max(...inside), outliers, min: s[0], max: s[s.length - 1] };
};

export const StatChart: React.FC<StatChartProps> = ({
  title, kind, labels = [], values = [], points = [], data = [], bins = 6,
  mean = 0, sd = 1, showRegression = false, xLabel, yLabel, formula, highlight,
  startFrame = 0, typeFrames = 90,
}) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const local = frame - startFrame;
  const p = interpolate(local, [0, typeFrames], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const plotW = W - PAD * 2, plotH = H - PAD * 2;
  const axis = (
    <g>
      <line x1={PAD} y1={H - PAD} x2={W - PAD} y2={H - PAD} stroke={t.textMuted} strokeWidth={2} />
      <line x1={PAD} y1={PAD} x2={PAD} y2={H - PAD} stroke={t.textMuted} strokeWidth={2} />
      {xLabel && <text x={W / 2} y={H - 14} textAnchor="middle" fontSize={20} fill={t.textMuted}>{xLabel}</text>}
      {yLabel && <text x={PAD} y={PAD - 16} fontSize={20} fill={t.textMuted}>{yLabel}</text>}
    </g>
  );
  let body: React.ReactNode = null;

  if (kind === 'bar') {
    const maxV = Math.max(1, ...values);
    const slot = plotW / Math.max(1, values.length);
    body = values.map((v, i) => {
      const bw = slot * 0.6, x = PAD + slot * i + slot * 0.2;
      const h = (v / maxV) * plotH * p, hl = highlight === i;
      return (
        <g key={i}>
          <rect x={x} y={H - PAD - h} width={bw} height={h} rx={6} fill={hl ? t.accent : t.accentSoft} stroke={t.cardBorder} />
          <text x={x + bw / 2} y={H - PAD - h - 10} textAnchor="middle" fontSize={20} fill={t.text} opacity={p > 0.6 ? 1 : 0}>{v}</text>
          <text x={x + bw / 2} y={H - PAD + 28} textAnchor="middle" fontSize={20} fill={t.textMuted}>{labels[i] ?? ''}</text>
        </g>
      );
    });
  } else if (kind === 'line') {
    const maxV = Math.max(1, ...values);
    const pts = values.map((v, i) => [PAD + (values.length > 1 ? (plotW * i) / (values.length - 1) : 0), H - PAD - (v / maxV) * plotH]);
    const d = pts.map((q, i) => `${i === 0 ? 'M' : 'L'}${q[0]},${q[1]}`).join(' ');
    const len = plotW * 1.6;
    body = (
      <g>
        <path d={d} fill="none" stroke={t.accent} strokeWidth={5} strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
        {pts.map((q, i) => (
          <g key={i}>
            <circle cx={q[0]} cy={q[1]} r={7} fill={t.accent} opacity={p > i / pts.length ? 1 : 0} />
            <text x={q[0]} y={H - PAD + 28} textAnchor="middle" fontSize={20} fill={t.textMuted}>{labels[i] ?? ''}</text>
          </g>
        ))}
      </g>
    );
  } else if (kind === 'scatter') {
    const maxX = Math.max(1, ...points.map((q) => q[0]));
    const maxY = Math.max(1, ...points.map((q) => q[1]));
    const sx = (x: number) => PAD + (x / maxX) * plotW;
    const sy = (y: number) => H - PAD - (y / maxY) * plotH;
    const shown = Math.floor(p * points.length);
    let reg: React.ReactNode = null;
    if (showRegression && points.length > 1) {
      const n = points.length;
      const mx = points.reduce((a, q) => a + q[0], 0) / n;
      const my = points.reduce((a, q) => a + q[1], 0) / n;
      const b = points.reduce((a, q) => a + (q[0] - mx) * (q[1] - my), 0) / points.reduce((a, q) => a + (q[0] - mx) ** 2, 0);
      const a0 = my - b * mx;
      const x1 = 0, x2 = maxX;
      const len = 1000;
      reg = (
        <line x1={sx(x1)} y1={sy(a0 + b * x1)} x2={sx(x2)} y2={sy(a0 + b * x2)} stroke={t.okText} strokeWidth={4}
          strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
      );
    }
    body = (
      <g>
        {points.slice(0, shown).map((q, i) => <circle key={i} cx={sx(q[0])} cy={sy(q[1])} r={9} fill={t.accent} opacity={0.85} />)}
        {reg}
      </g>
    );
  } else if (kind === 'histogram') {
    const lo = Math.min(...data), hi = Math.max(...data);
    const w = (hi - lo) / bins || 1;
    const counts = Array.from({ length: bins }, (_, i) =>
      data.filter((v) => v >= lo + i * w && (i === bins - 1 ? v <= hi : v < lo + (i + 1) * w)).length);
    const maxC = Math.max(1, ...counts);
    const slot = plotW / bins;
    body = counts.map((c, i) => {
      const h = (c / maxC) * plotH * p;
      const x = PAD + slot * i;
      return (
        <g key={i}>
          <rect x={x + 3} y={H - PAD - h} width={slot - 6} height={h} fill={t.accentSoft} stroke={t.accent} strokeWidth={2} />
          <text x={x + slot / 2} y={H - PAD - h - 8} textAnchor="middle" fontSize={20} fill={t.text} opacity={p > 0.6 ? 1 : 0}>{c}</text>
          <text x={x + slot / 2} y={H - PAD + 28} textAnchor="middle" fontSize={18} fill={t.textMuted}>{(lo + i * w).toFixed(0)}</text>
        </g>
      );
    });
  } else if (kind === 'boxplot') {
    const s = boxStats(data);
    const lo = s.min - 5, hi = s.max + 5;
    const sy = (v: number) => H - PAD - ((v - lo) / (hi - lo)) * plotH;
    const cx = W / 2, bw = 180;
    const g = p;
    body = (
      <g opacity={g}>
        <line x1={cx} y1={sy(s.lo)} x2={cx} y2={sy(s.q1)} stroke={t.text} strokeWidth={3} />
        <line x1={cx} y1={sy(s.q3)} x2={cx} y2={sy(s.hi)} stroke={t.text} strokeWidth={3} />
        <line x1={cx - 50} y1={sy(s.lo)} x2={cx + 50} y2={sy(s.lo)} stroke={t.text} strokeWidth={3} />
        <line x1={cx - 50} y1={sy(s.hi)} x2={cx + 50} y2={sy(s.hi)} stroke={t.text} strokeWidth={3} />
        <rect x={cx - bw / 2} y={sy(s.q3)} width={bw} height={sy(s.q1) - sy(s.q3)} fill={t.accentSoft} stroke={t.accent} strokeWidth={3} rx={6} />
        <line x1={cx - bw / 2} y1={sy(s.med)} x2={cx + bw / 2} y2={sy(s.med)} stroke={t.accent} strokeWidth={5} />
        <text x={cx + bw / 2 + 14} y={sy(s.med) + 7} fontSize={20} fill={t.text}>median {s.med.toFixed(1)}</text>
        {s.outliers.map((v, i) => (
          <circle key={i} cx={cx} cy={sy(v)} r={10} fill="#ef4444" opacity={p > 0.5 ? 1 : 0} />
        ))}
        {s.outliers.length > 0 && (
          <text x={cx - bw / 2 - 14} y={sy(s.outliers[0]) + 7} textAnchor="end" fontSize={20} fill="#ef4444">
            outlier {s.outliers.map((v) => v.toFixed(0)).join(', ')}
          </text>
        )}
      </g>
    );
  } else if (kind === 'normal') {
    const xmin = mean - 4 * sd, xmax = mean + 4 * sd;
    const pdf = (x: number) => Math.exp(-0.5 * ((x - mean) / sd) ** 2) / (sd * Math.sqrt(2 * Math.PI));
    const peak = pdf(mean);
    const sx = (x: number) => PAD + ((x - xmin) / (xmax - xmin)) * plotW;
    const sy = (y: number) => H - PAD - (y / peak) * plotH * 0.9;
    const N = 120;
    const xs = Array.from({ length: N + 1 }, (_, i) => xmin + ((xmax - xmin) * i) / N);
    const d = xs.map((x, i) => `${i === 0 ? 'M' : 'L'}${sx(x)},${sy(pdf(x))}`).join(' ');
    const shadeXs = Array.from({ length: 60 }, (_, i) => mean - sd + (2 * sd * i) / 59);
    const shade = shadeXs.map((x, i) => `${i === 0 ? 'M' : 'L'}${sx(x)},${sy(pdf(x))}`).join(' ') + ` L${sx(mean + sd)},${H - PAD} L${sx(mean - sd)},${H - PAD} Z`;
    body = (
      <g>
        <path d={shade} fill={t.accentSoft} opacity={p > 0.8 ? 1 : 0} />
        <path d={d} fill="none" stroke={t.accent} strokeWidth={5} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
        {[-1, 0, 1].map((k) => (
          <text key={k} x={sx(mean + k * sd)} y={H - PAD + 28} textAnchor="middle" fontSize={20} fill={t.textMuted}>
            {k === 0 ? `μ=${mean}` : `${k > 0 ? '+' : ''}${k}σ`}
          </text>
        ))}
      </g>
    );
  }

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-10 relative z-10">
      <div className="text-5xl font-extrabold mb-6" style={{ color: t.text }}>{title}</div>
      <div className="flex items-start gap-10">
        <div className="rounded-2xl p-6" style={{ background: t.card, border: `2px solid ${t.cardBorder}` }}>
          <svg width={W} height={H}>
            {axis}
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

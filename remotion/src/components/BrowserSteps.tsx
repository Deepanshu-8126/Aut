import React from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';

// Browser setup walkthrough (generic mock page, kisi brand ka asli UI nahi).
// navigate step: URL address bar mein type hota hai, page load hota hai (headline + buttons).
// click step: cursor pichle page ke button par jaata hai, ripple, phir naya page (step ke headline/buttons).
export interface BrowserStep {
  type: 'navigate' | 'click';
  url?: string;
  pageTitle?: string;
  headline?: string;
  subtitle?: string;
  buttons?: string[];    // is step ke baad wale page ke buttons
  label?: string;        // click step: pichle page ka kaunsa button
  note?: string;         // neeche ka hint bar
  at?: string;           // narration ka word (pipeline set karta hai)
}

export interface BrowserStepsProps {
  title?: string;
  steps: BrowserStep[];
  stepAt?: number[];
}

const FONT = "'Inter', 'Helvetica Neue', Arial, sans-serif";
const MONO = "'JetBrains Mono', Menlo, Consolas, monospace";

// Pichle pages ka state: navigate step khud page hai; click step ka page uske pehle wale step se
const pageBefore = (steps: BrowserStep[], idx: number) => {
  const cur = steps[idx];
  const start = cur.type === 'click' ? idx - 1 : idx;
  const find = <K extends keyof BrowserStep>(k: K, fallback: BrowserStep[K] | undefined) => {
    for (let j = start; j >= 0; j--) { const v = steps[j][k]; if (v !== undefined) return v as BrowserStep[K]; }
    return fallback;
  };
  return {
    pageTitle: find('pageTitle', 'Home') as string,
    headline: find('headline', '') as string,
    subtitle: find('subtitle', '') as string,
    buttons: (find('buttons', []) as string[]) || [],
  };
};

export const BrowserSteps: React.FC<BrowserStepsProps & { aspectRatio: '9:16' | '16:9' }> = ({
  title, steps, stepAt, aspectRatio,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const vertical = aspectRatio === '9:16';
  const sec = frame / fps;

  const n = steps.length;
  const starts = stepAt && stepAt.length === n ? stepAt : steps.map((_, i) => (i * 6) / Math.max(1, n));
  let idx = 0;
  for (let i = 0; i < n; i++) if (sec >= starts[i]) idx = i;
  const step = steps[idx];
  const local = Math.max(0, sec - starts[idx]);
  const before = pageBefore(steps, idx);

  // ---- Navigate: URL type + page fade-in
  const url = step.url || '';
  const typedChars = step.type === 'navigate' ? Math.min(url.length, Math.floor(local / 0.045)) : url.length;
  const lastUrl = (() => { for (let j = idx; j >= 0; j--) if (steps[j].url) return steps[j].url as string; return ''; })();
  const urlText = step.type === 'navigate' ? url.slice(0, typedChars) : lastUrl;
  const pageFade = interpolate(local, [0.25, 0.8], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // ---- Click: cursor move, ripple, page change
  const CLICK_AT = 0.9;
  const clickIdx = step.type === 'click' ? before.buttons.indexOf(step.label || '') : -1;
  const btnCount = Math.max(1, before.buttons.length);
  const btnX = (i: number) => 22 + ((i + 1) / (btnCount + 1)) * 56;
  const targetX = clickIdx >= 0 ? btnX(clickIdx) : 50;
  const targetY = 60;
  const moveP = step.type === 'click' ? interpolate(local, [0, CLICK_AT], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) : 0;
  const cx = interpolate(moveP, [0, 1], [50, targetX]);
  const cy = interpolate(moveP, [0, 1], [28, targetY]);
  const rippleP = step.type === 'click' ? interpolate(local, [CLICK_AT, CLICK_AT + 0.45], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) : 0;
  const after = step.type === 'click' && local >= CLICK_AT + 0.25;

  // Page jo abhi dikh raha hai
  const showTitle = after ? (step.pageTitle || before.pageTitle) : before.pageTitle;
  const showHeadline = step.type === 'navigate' ? (step.headline || '') : (after ? (step.headline || '') : before.headline);
  const showSubtitle = step.type === 'navigate' ? (step.subtitle || '') : (after ? (step.subtitle || '') : before.subtitle);
  const showButtons = step.type === 'navigate' ? (step.buttons || []) : (after ? (step.buttons || []) : before.buttons);
  const pressed = step.type === 'click' && !after && local > CLICK_AT - 0.2 ? clickIdx : -1;

  const W = vertical ? 900 : 1500;
  const H = vertical ? 1000 : 600;

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, padding: 30, boxSizing: 'border-box' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 22, marginBottom: 18 }}>
        {title && <div style={{ fontSize: vertical ? 44 : 46, fontWeight: 900, color: t.text, textAlign: 'center' }}>{title}</div>}
        <div style={{ fontFamily: MONO, fontSize: 22, color: t.accent, fontWeight: 800, background: t.accentSoft, borderRadius: 999, padding: '6px 16px' }}>STEP {idx + 1} / {n}</div>
      </div>

      <div style={{ width: W, height: H, background: '#ffffff', borderRadius: 22, border: `1px solid ${t.cardBorder}`, boxShadow: '0 30px 60px -20px rgba(15,23,42,0.28)', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        {/* Tab bar */}
        <div style={{ height: 56, background: '#f1f3f4', display: 'flex', alignItems: 'flex-end', gap: 10, padding: '0 18px' }}>
          <div style={{ display: 'flex', gap: 8, alignSelf: 'center', marginRight: 14 }}>
            <div style={{ width: 16, height: 16, borderRadius: 8, background: '#ef4444' }} />
            <div style={{ width: 16, height: 16, borderRadius: 8, background: '#f59e0b' }} />
            <div style={{ width: 16, height: 16, borderRadius: 8, background: '#22c55e' }} />
          </div>
          <div style={{ height: 44, minWidth: 300, background: '#ffffff', borderRadius: '14px 14px 0 0', display: 'flex', alignItems: 'center', padding: '0 20px', fontSize: 22, color: '#374151', fontWeight: 600 }}>
            {showTitle}
          </div>
        </div>

        {/* Address bar */}
        <div style={{ height: 66, background: '#ffffff', borderBottom: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', gap: 14, padding: '0 22px' }}>
          <div style={{ width: 40, height: 40, borderRadius: 20, background: '#f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22, color: '#6b7280' }}>&#8592;</div>
          <div style={{ flex: 1, height: 44, borderRadius: 22, background: '#f3f4f6', display: 'flex', alignItems: 'center', padding: '0 20px', fontFamily: MONO, fontSize: 24, color: '#111827' }}>
            <span style={{ width: 12, height: 12, borderRadius: 6, background: '#16a34a', marginRight: 14, display: 'inline-block' }} />
            {urlText}
            {step.type === 'navigate' && typedChars < url.length && <span style={{ width: 3, height: 26, background: t.accent, marginLeft: 3 }} />}
          </div>
        </div>

        {/* Page */}
        <div style={{ position: 'relative', flex: 1, minHeight: 0, overflow: 'hidden', background: '#ffffff', opacity: step.type === 'navigate' ? pageFade : 1 }}>
          <div style={{ height: 70, background: '#0f172a', display: 'flex', alignItems: 'center', padding: '0 34px', justifyContent: 'space-between' }}>
            <div style={{ width: 150, height: 26, borderRadius: 6, background: '#38bdf8', opacity: 0.9 }} />
            <div style={{ display: 'flex', gap: 22 }}>
              {['Docs', 'Download', 'Help'].map((x) => (<div key={x} style={{ color: '#cbd5e1', fontSize: 20 }}>{x}</div>))}
            </div>
          </div>
          <div style={{ padding: vertical ? '50px 40px' : '36px 90px', textAlign: 'center' }}>
            <div style={{ fontSize: vertical ? 48 : 60, fontWeight: 900, color: '#0a0a0a', lineHeight: 1.1 }}>{showHeadline}</div>
            {showSubtitle && <div style={{ marginTop: 16, fontSize: vertical ? 26 : 30, color: '#4b5563' }}>{showSubtitle}</div>}
            <div style={{ marginTop: vertical ? 46 : 28, display: 'flex', justifyContent: 'center', gap: 26, flexWrap: 'wrap' }}>
              {showButtons.map((b, i) => {
                const hot = pressed === i;
                return (
                  <div key={b} style={{
                    padding: '20px 38px', borderRadius: 14, fontSize: 28, fontWeight: 800,
                    background: hot ? '#1d4ed8' : t.accent, color: '#ffffff',
                    boxShadow: hot ? `0 0 0 8px ${t.accent}40` : '0 8px 18px rgba(37,99,235,0.25)',
                    transform: hot ? 'scale(0.96)' : 'scale(1)',
                  }}>{b}</div>
                );
              })}
            </div>
          </div>

          {step.type === 'click' && clickIdx >= 0 && rippleP > 0 && rippleP < 1 && (
            <div style={{
              position: 'absolute', left: `${targetX}%`, top: `${targetY}%`, width: 120, height: 120,
              marginLeft: -60, marginTop: -60, borderRadius: 60, border: `4px solid ${t.accent}`,
              opacity: 1 - rippleP, transform: `scale(${0.4 + rippleP})`,
            }} />
          )}

          {step.type === 'click' && !after && (
            <svg style={{ position: 'absolute', left: `${cx}%`, top: `${cy}%`, width: 44, height: 52, filter: 'drop-shadow(0 3px 4px rgba(0,0,0,0.35))' }} viewBox="0 0 24 30">
              <path d="M2 2 L2 24 L8 18 L12 28 L16 26 L12 17 L20 17 Z" fill="#0a0a0a" stroke="#ffffff" strokeWidth="1.5" strokeLinejoin="round" />
            </svg>
          )}
        </div>

        {step.note && (
          <div style={{ flexShrink: 0, background: '#fef9c3', borderTop: '1px solid #fde68a', padding: '14px 24px', fontSize: 26, fontWeight: 700, color: '#713f12' }}>
            {step.note}
          </div>
        )}
      </div>

    </div>
  );
};

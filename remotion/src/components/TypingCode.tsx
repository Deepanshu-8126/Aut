import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { useTheme } from '../ThemeContext';

// Python ke liye chhota regex highlighter (typing ke saath har frame par chalta hai, isliye shiki ki jagah ye).
const TOKEN = /(#[^\n]*)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|\b(def|return|for|in|if|else|elif|while|import|from|class|True|False|None|and|or|not)\b|\b(print|len|append|range|type)\b|\b(\d+)\b/g;

export function highlightPy(src: string, t: { codeText: string; accent: string; textMuted: string; okText: string; tipText: string; }) {
  const out: React.ReactNode[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  let k = 0;
  TOKEN.lastIndex = 0;
  while ((m = TOKEN.exec(src)) !== null) {
    if (m.index > last) out.push(<span key={k++} style={{ color: t.codeText }}>{src.slice(last, m.index)}</span>);
    const [txt, comment, str, kw, fn, num] = m;
    let color = t.codeText;
    if (comment) color = t.textMuted;
    else if (str) color = t.okText;
    else if (kw) color = '#c026d3';
    else if (fn) color = t.accent;
    else if (num) color = '#d97706';
    out.push(<span key={k++} style={{ color, fontStyle: comment ? 'italic' : 'normal' }}>{txt}</span>);
    last = m.index + txt.length;
  }
  if (last < src.length) out.push(<span key={k++} style={{ color: t.codeText }}>{src.slice(last)}</span>);
  return out;
}

// Code keyboard ki tarah type hota hai. `startFrame`..`startFrame+typeFrames` mein saare chars type honge.
type DiffLine = { type: 'same' | 'del' | 'add'; text: string };

export const TypingCode: React.FC<{ code: string; filename?: string; language?: string; startFrame?: number; typeFrames: number; highlightLines?: number[]; diff?: DiffLine[] }> = ({
  code, filename = 'lists.py', language = 'python', startFrame = 0, typeFrames, highlightLines = [], diff,
}) => {
  if (diff && diff.length) {
    return <DiffMorph diff={diff} filename={filename} language={language} startFrame={startFrame} typeFrames={typeFrames} />;
  }
  const frame = useCurrentFrame();
  const t = useTheme();
  const light = t.name === 'light-grid';
  const total = code.length;
  const progress = interpolate(frame - startFrame, [0, Math.max(1, typeFrames)], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const shown = Math.floor(progress * total);
  const typed = code.slice(0, shown);
  const lines = typed.split('\n');
  const allLines = code.split('\n');
  const cursorOn = Math.floor(frame / 15) % 2 === 0;

  return (
    <div className="w-full h-full flex items-center justify-center p-10 relative z-10">
      <div className="w-full max-w-6xl rounded-3xl overflow-hidden" style={{ background: t.codeBg, border: `1px solid ${t.cardBorder}`,
        boxShadow: light ? '0 22px 60px rgba(15,23,42,0.14)' : '0 25px 70px rgba(0,0,0,0.85)' }}>
        <div className="px-6 py-4 flex items-center justify-between" style={{ background: t.winBar, borderBottom: `1px solid ${t.cardBorder}` }}>
          <div className="flex items-center gap-2.5">
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#ff5f57' }} />
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#febc2e' }} />
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#28c840' }} />
          </div>
          <div className="font-mono text-xl px-4 py-1.5 rounded-lg" style={{ color: t.codeText, background: t.codeBg, border: `1px solid ${t.cardBorder}` }}>{filename}</div>
          <div className="font-mono text-xs uppercase tracking-wider" style={{ color: t.textMuted }}>{language}</div>
        </div>
        <div className="font-mono text-4xl leading-relaxed p-10 min-h-[420px]" style={{ whiteSpace: 'pre' }}>
          {allLines.map((line, idx) => {
            const n = idx + 1;
            const isLineShown = idx < lines.length;
            const isCurrent = idx === lines.length - 1;
            const text = isLineShown ? (isCurrent ? lines[idx] : line) : '';
            const hl = highlightLines.includes(n) && isLineShown;
            return (
              <div key={idx} className="flex items-center rounded-md px-2"
                style={{ background: hl ? t.accentSoft : 'transparent', borderLeft: hl ? `4px solid ${t.accent}` : '4px solid transparent', minHeight: 40 }}>
                <span className="w-14 text-right pr-6 text-2xl select-none" style={{ color: t.textMuted }}>{n}</span>
                <span>{highlightPy(text, t)}</span>
                {isCurrent && cursorOn && <span style={{ display: 'inline-block', width: 16, height: 40, background: t.accent, marginLeft: 2 }} />}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// Purana code (same + del lines) pehle dikhta hai. Phir del lines red strike hokar fade hoti hain,
// aur add lines ek-ek character type hoti hain. Same lines apni jagah rehti hain.
const DiffMorph: React.FC<{ diff: DiffLine[]; filename: string; language: string; startFrame: number; typeFrames: number }> = ({
  diff, filename, language, startFrame, typeFrames,
}) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const light = t.name === 'light-grid';
  const local = frame - startFrame;
  const addTotal = diff.filter((d) => d.type === 'add').reduce((a, d) => a + d.text.length + 1, 0);
  const addProgress = interpolate(local, [0, Math.max(1, typeFrames)], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  let addBudget = Math.floor(addProgress * addTotal);
  const delFade = interpolate(local, [0, 18], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const morphing = local >= 0;

  return (
    <div className="w-full h-full flex items-center justify-center p-10 relative z-10">
      <div className="w-full max-w-6xl rounded-3xl overflow-hidden" style={{ background: t.codeBg, border: `1px solid ${t.cardBorder}`,
        boxShadow: light ? '0 22px 60px rgba(15,23,42,0.14)' : '0 25px 70px rgba(0,0,0,0.85)' }}>
        <div className="px-6 py-4 flex items-center justify-between" style={{ background: t.winBar, borderBottom: `1px solid ${t.cardBorder}` }}>
          <div className="flex items-center gap-2.5">
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#ff5f57' }} />
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#febc2e' }} />
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#28c840' }} />
          </div>
          <div className="font-mono text-xl px-4 py-1.5 rounded-lg" style={{ color: t.codeText, background: t.codeBg, border: `1px solid ${t.cardBorder}` }}>{filename}</div>
          <div className="font-mono text-xs uppercase tracking-wider" style={{ color: t.textMuted }}>{language}</div>
        </div>
        <div className="font-mono text-4xl leading-relaxed p-10 min-h-[420px]" style={{ whiteSpace: 'pre' }}>
          {diff.map((d, idx) => {
            let opacity = 1;
            let text = d.text;
            let deco: 'none' | 'line-through' = 'none';
            let bg = 'transparent';
            if (d.type === 'del') {
              if (!morphing) { bg = light ? '#fee2e2' : 'rgba(239,68,68,0.15)'; }
              else { opacity = delFade; deco = 'line-through'; bg = light ? '#fee2e2' : 'rgba(239,68,68,0.15)'; }
            } else if (d.type === 'add') {
              if (!morphing) { opacity = 0; }
              else {
                const take = Math.max(0, Math.min(text.length, addBudget));
                addBudget -= text.length + 1;
                text = take > 0 ? text.slice(0, take) : '';
                opacity = take > 0 ? 1 : 0;
                bg = light ? '#dcfce7' : 'rgba(34,197,94,0.15)';
              }
            }
            if (opacity === 0 && d.type === 'add') return <div key={idx} style={{ minHeight: 40 }} />;
            return (
              <div key={idx} className="flex items-center rounded-md px-2" style={{ background: bg, opacity, minHeight: 40 }}>
                <span className="w-14 text-right pr-6 text-2xl select-none" style={{ color: t.textMuted }}>{idx + 1}</span>
                <span style={{ textDecoration: deco }}>{highlightPy(text, t)}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

import React, { useEffect, useState } from 'react';
import { continueRender, delayRender, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CodeExplainerProps } from '../types';
import { FileCode, CheckCircle2 } from 'lucide-react';
import { createHighlighter, Highlighter } from 'shiki';
import { useTheme } from '../ThemeContext';

let cachedHighlighter: Highlighter | null = null;
const SHIKI_THEME = (light: boolean) => (light ? 'github-light-default' : 'github-dark-default');

// White code window (light) or dark editor (vdo). Lines reveal progressively.
export const CodeExplainer: React.FC<CodeExplainerProps & { aspectRatio: '9:16' | '16:9' }> = ({
  code, language = 'python', filename = 'main.py', highlightLines = [], lineNotes = [], aspectRatio,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const light = t.name === 'light-grid';

  const [highlighter, setHighlighter] = useState<Highlighter | null>(cachedHighlighter);
  const [handle] = useState(() => (cachedHighlighter ? null : delayRender('Shiki highlighter loading')));

  useEffect(() => {
    if (cachedHighlighter) return;
    createHighlighter({
      themes: ['github-dark-default', 'github-light-default'],
      langs: ['python', 'javascript', 'typescript', 'jsx', 'tsx', 'json', 'bash', 'c', 'cpp', 'rust'],
    })
      .then((h) => { cachedHighlighter = h; setHighlighter(h); if (handle !== null) continueRender(handle); })
      .catch((err) => { console.error('Highlighter error:', err); if (handle !== null) continueRender(handle); });
  }, [handle]);

  const entrance = spring({ frame, fps, config: { damping: 14, mass: 0.9 } });
  const scale = interpolate(entrance, [0, 1], [0.92, 1]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);
  const lines = code.trim().split('\n');
  const visibleLineCount = Math.min(
    lines.length,
    Math.floor(interpolate(frame, [0, Math.min(lines.length * 4, 30)], [1, lines.length], { extrapolateRight: 'clamp' })),
  );
  const vertical = aspectRatio === '9:16';

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-6 relative z-10"
      style={{ transform: `scale(${scale})`, opacity }}>
      <div className={`w-full rounded-3xl overflow-hidden flex flex-col ${vertical ? 'max-w-[940px] w-[94%]' : 'max-w-6xl'}`}
        style={{
          background: t.codeBg,
          border: `1px solid ${light ? '#e5e7eb' : t.cardBorder}`,
          boxShadow: light ? '0 18px 50px rgba(15,23,42,0.10)' : '0 25px 70px rgba(0,0,0,0.85)',
        }}>
        {/* Window bar: mac dots, filename, language */}
        <div className="px-6 py-4 flex items-center justify-between" style={{ background: t.winBar, borderBottom: `1px solid ${t.cardBorder}` }}>
          <div className="flex items-center gap-2.5">
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#ff5f57' }} />
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#febc2e' }} />
            <div className="w-3.5 h-3.5 rounded-full" style={{ background: '#28c840' }} />
          </div>
          <div className={`flex items-center gap-2 font-mono px-3.5 py-1.5 rounded-lg ${vertical ? 'text-base' : 'text-lg'}`}
            style={{ color: t.codeText, background: t.codeBg, border: `1px solid ${t.cardBorder}` }}>
            <FileCode className="w-4 h-4" style={{ color: t.accent }} />
            <span>{filename}</span>
          </div>
          <div className={`font-mono uppercase tracking-wider ${vertical ? 'text-sm' : 'text-base'}`} style={{ color: t.textMuted }}>
            {language}
          </div>
        </div>

        <div className={`font-mono leading-relaxed overflow-x-auto ${vertical ? 'p-8 text-xl' : 'p-8 text-3xl'}`}>
          {lines.slice(0, visibleLineCount).map((rawLine, idx) => {
            const lineNum = idx + 1;
            const isHighlighted = highlightLines.includes(lineNum);
            const lineNote = lineNotes.find((n) => n.line === lineNum);
            let lineHtml = '';
            if (highlighter) {
              try {
                lineHtml = highlighter.codeToHtml(rawLine, { lang: language, theme: SHIKI_THEME(light) });
                const m = lineHtml.match(/<code>([\s\S]*?)<\/code>/);
                if (m) lineHtml = m[1];
              } catch { lineHtml = rawLine; }
            }
            return (
              <div key={idx} className="relative flex items-center px-3 py-1 rounded-md"
                style={{
                  background: isHighlighted ? t.accentSoft : 'transparent',
                  borderLeft: isHighlighted ? `6px solid ${t.accent}` : '6px solid transparent',
                  // Focus mode: highlight hone par baaki lines dim ho jaati hain
                  opacity: highlightLines.length > 0 && !isHighlighted ? 0.32 : 1,
                  boxShadow: isHighlighted ? `0 8px 24px -10px ${t.accent}88` : 'none',
                  transition: 'opacity 0.2s',
                }}>
                <span className={`select-none text-right pr-4 font-mono ${vertical ? 'w-10 text-base' : 'w-12 text-2xl'}`}
                  style={{ color: isHighlighted ? t.accent : t.textMuted, fontWeight: isHighlighted ? 700 : 400 }}>
                  {lineNum}
                </span>
                <span className="flex-1" style={{ color: t.codeText }}
                  dangerouslySetInnerHTML={{ __html: lineHtml || rawLine.replace(/ /g, '&nbsp;') }} />
              </div>
            );
          })}
        </div>
        {lineNotes.length > 0 && (
          <div className={`flex flex-col gap-2 border-t ${vertical ? 'p-6' : 'px-8 py-5'}`} style={{ borderColor: t.cardBorder }}>
            {lineNotes.map((n, i) => (
              <div key={i} className={`flex items-center gap-3 rounded-xl font-sans font-semibold ${vertical ? 'px-4 py-2 text-lg' : 'px-5 py-3 text-2xl'}`}
                style={{ background: t.okBg, color: t.okText, border: `1px solid ${t.okText}33` }}>
                <CheckCircle2 className={vertical ? 'w-5 h-5 shrink-0' : 'w-7 h-7 shrink-0'} />
                <span>Line {n.line}: {n.note}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};


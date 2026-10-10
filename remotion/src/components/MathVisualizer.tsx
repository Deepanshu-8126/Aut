import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { MathVisualizerProps } from '../types';
import katex from 'katex';
import { useTheme } from '../ThemeContext';

// Formula card (LaTeX via KaTeX) + variable breakdown.
export const MathVisualizer: React.FC<MathVisualizerProps & { aspectRatio: '9:16' | '16:9' }> = ({
  title, formula, explanation, variables = [], aspectRatio,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const entrance = spring({ frame, fps, config: { damping: 14, mass: 0.9 } });
  const vertical = aspectRatio === '9:16';
  const light = t.name === 'light-grid';

  let formulaHtml = '';
  try { formulaHtml = katex.renderToString(formula, { displayMode: true, throwOnError: false }); }
  catch { formulaHtml = formula; }

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8 relative z-10"
      style={{ transform: `scale(${interpolate(entrance, [0, 1], [0.9, 1])})`, opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      {title && <h2 className={`font-black tracking-tight mb-6 text-center ${vertical ? 'text-3xl max-w-sm' : 'text-4xl'}`} style={{ color: t.text }}>{title}</h2>}

      <div className={`w-full rounded-2xl p-6 flex flex-col items-center justify-center mb-6 text-center ${vertical ? 'max-w-md py-8' : 'max-w-3xl py-10'}`}
        style={{ background: t.card, border: `1px solid ${t.cardBorder}`,
          boxShadow: light ? '0 10px 30px rgba(15,23,42,0.08)' : '0 0 50px rgba(56,189,248,0.2)' }}>
        <div className={`overflow-x-auto max-w-full ${vertical ? 'text-2xl' : 'text-4xl'}`} style={{ color: t.text }}
          dangerouslySetInnerHTML={{ __html: formulaHtml }} />
        {explanation && <p className="text-sm md:text-base mt-4 max-w-xl" style={{ color: t.textMuted }}>{explanation}</p>}
      </div>

      {variables.length > 0 && (
        <div className={`grid gap-3 w-full ${vertical ? 'grid-cols-1 max-w-md' : 'grid-cols-3 max-w-3xl'}`}>
          {variables.map((item, idx) => {
            let sym = item.symbol;
            try { sym = katex.renderToString(item.symbol, { displayMode: false, throwOnError: false }); } catch { /* keep raw */ }
            return (
              <div key={idx} className="rounded-xl p-3 flex items-center gap-3" style={{ background: t.card, border: `1px solid ${t.cardBorder}` }}>
                <div className="w-10 h-10 rounded-lg flex items-center justify-center font-bold shrink-0"
                  style={{ background: t.accentSoft, color: t.accent }} dangerouslySetInnerHTML={{ __html: sym }} />
                <div className="text-left leading-tight text-xs" style={{ color: t.textMuted }}>{item.meaning}</div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

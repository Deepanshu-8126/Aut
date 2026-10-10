import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';

export interface TerminalLine {
  lineNum?: number | string;
  text: string;
  type?: 'command' | 'normal' | 'add' | 'remove' | 'drift' | 'comment';
}
export interface TerminalPane {
  title: string;
  command?: string;
  lines: TerminalLine[];
  caption?: string;
}
export interface TerminalSplitProps {
  title?: string;
  badge?: string;
  bottomText?: string;
  bottomSubtext?: string;
  leftPane: TerminalPane;
  rightPane?: TerminalPane;
  aspectRatio: '9:16' | '16:9';
}

// Black terminal card with `$ command` + output (light), or dark terminal (vdo).
export const TerminalSplit: React.FC<TerminalSplitProps> = ({
  title, badge, bottomText, bottomSubtext, leftPane, rightPane, aspectRatio,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const light = t.name === 'light-grid';
  const vertical = aspectRatio === '9:16';
  const entrance = spring({ frame, fps, config: { damping: 14, mass: 0.8 } });

  const lineColor = (type?: TerminalLine['type']) => {
    if (type === 'drift') return { color: '#fda4af', background: 'rgba(244,63,94,0.15)', fontWeight: 700 };
    if (type === 'add') return { color: '#86efac', background: 'rgba(34,197,94,0.12)' };
    if (type === 'remove') return { color: '#f87171', background: 'rgba(239,68,68,0.12)' };
    if (type === 'comment') return { color: '#64748b', fontStyle: 'italic' as const };
    return { color: '#e5e7eb' };
  };

  const pane = (p: TerminalPane, i: number) => {
    const s = spring({ frame: frame - i * 6, fps, config: { damping: 13 } });
    return (
      <div className="flex-1 flex flex-col rounded-2xl overflow-hidden"
        style={{ transform: `translateY(${interpolate(s, [0, 1], [30, 0])}px)`, opacity: interpolate(s, [0, 1], [0, 1]),
          background: t.termBg, border: `1px solid ${light ? '#111827' : t.cardBorder}`,
          boxShadow: light ? '0 14px 40px rgba(15,23,42,0.18)' : '0 25px 60px rgba(0,0,0,0.6)' }}>
        <div className="px-4 py-2.5 flex items-center gap-2" style={{ background: '#1f2937' }}>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full" style={{ background: '#ff5f57' }} />
            <div className="w-3 h-3 rounded-full" style={{ background: '#febc2e' }} />
            <div className="w-3 h-3 rounded-full" style={{ background: '#28c840' }} />
          </div>
          <span className="font-mono text-xs md:text-sm ml-2 font-medium" style={{ color: '#d1d5db' }}>{p.title}</span>
        </div>
        <div className="p-4 font-mono text-xs md:text-sm flex flex-col gap-1.5 flex-1" style={{ color: t.termText }}>
          {p.command && (
            <div className="font-semibold mb-2 flex items-center gap-2" style={{ color: '#67e8f9' }}>
              <span style={{ color: '#f472b6' }}>$</span> {p.command}
            </div>
          )}
          {p.lines.map((line, idx) => (
            <div key={idx} className="flex items-start gap-3 px-2 py-0.5 rounded" style={lineColor(line.type)}>
              {line.lineNum && <span className="select-none w-5 text-right text-xs" style={{ color: '#4b5563' }}>{line.lineNum}</span>}
              <span className="flex-1 whitespace-pre-wrap">{line.text}</span>
            </div>
          ))}
        </div>
        {p.caption && (
          <div className="px-3 py-1.5 text-right text-base font-semibold" style={{ color: '#fcd34d' }}>{p.caption}</div>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between p-6 pb-32 relative z-10"
      style={{ opacity: interpolate(entrance, [0, 1], [0, 1]) }}>
      {(title || badge) && (
        <div className="text-center mt-4">
          {badge && (
            <div className="inline-block px-4 py-1.5 rounded-full font-mono text-sm font-bold uppercase tracking-wider mb-4"
              style={{ background: t.pillBg, color: t.pillText }}>{badge}</div>
          )}
          {title && <h2 className="font-black tracking-tight text-4xl" style={{ color: t.text }}>{title}</h2>}
        </div>
      )}

      <div className={`w-full max-w-[940px] flex gap-4 my-auto ${vertical ? 'flex-col' : 'flex-row'}`}>
        {pane(leftPane, 0)}
        {rightPane && pane(rightPane, 1)}
      </div>

      {bottomText && (
        <div className="mt-4 text-center">
          <div className="font-black text-2xl md:text-3xl uppercase tracking-wide" style={{ color: t.text }}>{bottomText}</div>
          {bottomSubtext && <div className="text-xl mt-1 font-semibold" style={{ color: t.accent }}>{bottomSubtext}</div>}
        </div>
      )}
    </div>
  );
};

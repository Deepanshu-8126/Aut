import React from 'react';
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { useTheme } from '../ThemeContext';

// Teacher-style popup: pop-in (spring), yellow tip ya green "note". startFrame ke baad dikhta hai.
export const TeacherTip: React.FC<{ text: string; startFrame: number; kind?: 'tip' | 'note'; x?: string; y?: string; hideAfter?: number }> = ({
  text, startFrame, kind = 'tip', x = '50%', y = '18%', hideAfter,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = useTheme();
  const local = frame - startFrame;
  if (local < 0) return null;
  if (hideAfter !== undefined && local > hideAfter) return null;
  const s = spring({ frame: local, fps, config: { damping: 9, mass: 0.6 } });
  const isTip = kind === 'tip';
  return (
    <div className="absolute z-40 pointer-events-none" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${s})`, opacity: Math.min(1, s * 1.5) }}>
      <div className="px-6 py-4 rounded-2xl font-bold text-xl whitespace-nowrap flex items-center gap-3"
        style={{
          background: isTip ? t.tipBg : t.okBg,
          border: `2px solid ${isTip ? t.tipBorder : t.okText}`,
          color: isTip ? t.tipText : t.okText,
          boxShadow: '0 12px 30px rgba(15,23,42,0.18)',
        }}>
        <span className="px-2 py-0.5 rounded-md text-sm font-black tracking-wider" style={{ background: isTip ? t.tipBorder : t.okText, color: '#fff' }}>{isTip ? 'TIP' : 'NOTE'}</span>
        <span>{text}</span>
      </div>
    </div>
  );
};

import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { useTheme } from '../ThemeContext';

// Black terminal: `$ command` type hota hai, phir output ek-ek line aata hai.
export const TerminalRun: React.FC<{ command: string; output: string[]; startFrame?: number; typeFrames: number }> = ({
  command, output, startFrame = 0, typeFrames,
}) => {
  const frame = useCurrentFrame();
  const t = useTheme();
  const local = frame - startFrame;
  const cmdShown = Math.floor(interpolate(local, [0, typeFrames], [0, command.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const cmdDone = cmdShown >= command.length;
  const outStart = typeFrames + 10;
  const linesShown = cmdDone ? Math.min(output.length, Math.max(0, Math.floor((local - outStart) / 18) + 1)) : 0;
  return (
    <div className="w-full h-full flex items-center justify-center p-10 relative z-10">
      <div className="w-full max-w-6xl rounded-2xl overflow-hidden" style={{ background: t.termBg, boxShadow: '0 20px 50px rgba(15,23,42,0.25)' }}>
        <div className="px-4 py-2.5 flex items-center gap-2" style={{ background: '#1f2937' }}>
          <div className="w-3 h-3 rounded-full" style={{ background: '#ff5f57' }} />
          <div className="w-3 h-3 rounded-full" style={{ background: '#febc2e' }} />
          <div className="w-3 h-3 rounded-full" style={{ background: '#28c840' }} />
          <span className="font-mono text-lg ml-3" style={{ color: '#d1d5db' }}>terminal</span>
        </div>
        <div className="p-10 font-mono text-4xl leading-relaxed" style={{ color: t.termText, minHeight: 300 }}>
          <div><span style={{ color: '#f472b6' }}>$ </span><span style={{ color: '#67e8f9' }}>{command.slice(0, cmdShown)}</span></div>
          {output.slice(0, linesShown).map((l, i) => (
            <div key={i} style={{ color: '#e5e7eb' }}>{l}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

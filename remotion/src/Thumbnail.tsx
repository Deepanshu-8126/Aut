import React from 'react';

// Thumbnail still (1280x720). Props lesson se auto-aate hain (pipeline/make_thumbnail.py).
export interface ThumbProps {
  title: string;              // bada text, jaise "What Is Java?"
  highlight?: string;         // title ka ek word jo yellow highlight ho
  badge: string;              // top pill, jaise "DAY 1 • JAVA 100"
  subtitle?: string;          // neeche ki line
  code?: string;              // right side code card (max 6 lines)
  codeTitle?: string;         // code card ka filename
  codeHighlightLine?: number; // 1-based line jo highlight ho
  footer?: string;            // bottom left, jaise "Progress • Day 1 / 100"
  accent?: string;            // accent color
  motif?: 'none' | 'snake';   // series ka visual motif
}

const FONT = "'Inter', 'Helvetica Neue', Arial, 'Noto Sans', sans-serif";
const MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace";

const clean = (s: string) => s.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();

export const Thumbnail: React.FC<ThumbProps> = ({
  title, highlight, badge, subtitle, code, codeTitle, codeHighlightLine, footer, accent = '#2563eb', motif = 'none',
}) => {
  const words = title.split(' ');
  const hl = clean(highlight || '');
  const codeLines = code ? code.split('\n') : [];
  const hasCode = codeLines.length > 0;
  // Title length ke hisaab se font: lambi title overflow na ho
  const L = title.length;
  const titleSize = L <= 16 ? 124 : L <= 24 ? 104 : L <= 36 ? 84 : L <= 52 ? 66 : 54;

  return (
    <div style={{
      width: 1280, height: 720, position: 'relative', overflow: 'hidden', background: '#ffffff',
      backgroundImage: 'linear-gradient(#eef0f3 1px, transparent 1px), linear-gradient(90deg, #eef0f3 1px, transparent 1px)',
      backgroundSize: '60px 60px', fontFamily: FONT, color: '#0a0a0a',
    }}>
      {/* Badge pill */}
      <div style={{
        position: 'absolute', left: 72, top: 64, background: '#0a0a0a', color: '#ffffff',
        borderRadius: 999, padding: '12px 26px', fontSize: 26, fontWeight: 800, letterSpacing: 2,
        fontFamily: MONO,
      }}>{badge}</div>

      {/* Title block */}
      <div style={{ position: 'absolute', left: 72, top: 170, width: hasCode ? 540 : 1100 }}>
        <div style={{ fontSize: titleSize, fontWeight: 900, lineHeight: 1.08, letterSpacing: -2 }}>
          {words.map((w, i) => {
            const isHl = hl.length > 0 && clean(w) === hl;
            return (
              <span key={i} style={{
                display: 'inline-block', marginRight: 22, marginBottom: 6,
                background: isHl ? '#facc15' : 'transparent',
                padding: isHl ? '0 14px' : 0, borderRadius: 14,
              }}>{w}</span>
            );
          })}
        </div>
        {subtitle && (
          <div style={{ marginTop: 30, fontSize: 36, fontWeight: 500, color: '#4b5563', lineHeight: 1.3 }}>
            {subtitle}
          </div>
        )}
        <div style={{ marginTop: 34, width: 120, height: 8, background: accent, borderRadius: 4 }} />
      </div>

      {/* Code card */}
      {hasCode && (
        <div style={{
          position: 'absolute', right: 40, top: 170, width: 640, background: '#ffffff',
          borderRadius: 22, border: '1px solid #e5e7eb',
          boxShadow: '0 30px 60px -20px rgba(15,23,42,0.25), 0 8px 18px rgba(15,23,42,0.08)',
          overflow: 'hidden',
        }}>
          <div style={{ height: 56, background: '#f3f4f6', display: 'flex', alignItems: 'center', padding: '0 20px', gap: 10, borderBottom: '1px solid #e5e7eb' }}>
            <div style={{ width: 14, height: 14, borderRadius: 7, background: '#ef4444' }} />
            <div style={{ width: 14, height: 14, borderRadius: 7, background: '#f59e0b' }} />
            <div style={{ width: 14, height: 14, borderRadius: 7, background: '#22c55e' }} />
            <div style={{ marginLeft: 'auto', fontFamily: MONO, fontSize: 22, color: '#374151' }}>{codeTitle || 'main.py'}</div>
          </div>
          <div style={{ padding: '24px 0', fontFamily: MONO, fontSize: 21, lineHeight: 1.65 }}>
            {codeLines.map((line, i) => {
              const n = i + 1;
              const on = codeHighlightLine === n;
              return (
                <div key={i} style={{
                  display: 'flex', padding: '0 26px 0 22px', background: on ? '#fef9c3' : 'transparent',
                  borderLeft: on ? '6px solid #facc15' : '6px solid transparent',
                }}>
                  <span style={{ width: 36, color: '#9ca3af' }}>{n}</span>
                  <span style={{ whiteSpace: 'pre', color: '#111827', fontWeight: on ? 700 : 500 }}>{line}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Footer */}
      {/* Series motif: snake (Python) */}
      {motif === 'snake' && (
        <svg width="1280" height="720" style={{ position: 'absolute', left: 0, top: 0, pointerEvents: 'none' }}>
          <path d="M 640 690 C 700 600, 760 740, 820 668 S 940 590, 990 650 S 1100 700, 1130 628"
                fill="none" stroke={accent} strokeWidth="30" strokeLinecap="round" opacity="0.92" />
          <path d="M 640 690 C 700 600, 760 740, 820 668 S 940 590, 990 650 S 1100 700, 1130 628"
                fill="none" stroke="#86efac" strokeWidth="6" strokeLinecap="round" strokeDasharray="2 22" opacity="0.8" />
          <circle cx="1160" cy="612" r="34" fill={accent} />
          <circle cx="1172" cy="604" r="6" fill="#ffffff" />
          <circle cx="1174" cy="602" r="3" fill="#0a0a0a" />
          <path d="M 1190 620 L 1222 612 M 1222 612 L 1236 602 M 1222 612 L 1236 622" stroke="#dc2626" strokeWidth="4" fill="none" strokeLinecap="round" />
        </svg>
      )}

      {footer && (
        <div style={{ position: 'absolute', left: 72, bottom: 48, fontFamily: MONO, fontSize: 24, color: '#6b7280' }}>
          {footer}
        </div>
      )}
    </div>
  );
};

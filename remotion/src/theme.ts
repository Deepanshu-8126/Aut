// Do themes, ek hi project mein `theme` field se choose hoti hai.
//  - "light-grid": white grid, black pill, code window, terminal card, yellow tip (reference style)
//  - "dark-vdo":   vdo ka original dark cyan look
export type ThemeName = 'light-grid' | 'dark-vdo';

export interface Theme {
  name: ThemeName;
  bg: string;          // page background
  gridLine: string;    // grid line color (light-grid), empty for dark-vdo
  text: string;
  textMuted: string;
  accent: string;      // primary highlight
  accentSoft: string;  // soft accent fill
  card: string;        // card background
  cardBorder: string;
  pillBg: string;      // badge pill
  pillText: string;
  codeBg: string;      // code window body
  codeText: string;
  winBar: string;      // window title bar
  termBg: string;      // terminal card
  termText: string;
  tipBg: string;
  tipBorder: string;
  tipText: string;
  okBg: string;        // green badge
  okText: string;
  progress: string;
}

export const THEMES: Record<ThemeName, Theme> = {
  'light-grid': {
    name: 'light-grid',
    bg: '#ffffff',
    gridLine: '#eef0f3',
    text: '#0a0a0a',
    textMuted: '#6b7280',
    accent: '#2563eb',
    accentSoft: '#dbeafe',
    card: '#ffffff',
    cardBorder: '#e5e7eb',
    pillBg: '#0a0a0a',
    pillText: '#ffffff',
    codeBg: '#ffffff',
    codeText: '#111827',
    winBar: '#f3f4f6',
    termBg: '#0f1115',
    termText: '#e5e7eb',
    tipBg: '#fff6cc',
    tipBorder: '#f5e08a',
    tipText: '#3f3200',
    okBg: '#dcfce7',
    okText: '#15803d',
    progress: '#0a0a0a',
  },
  'dark-vdo': {
    name: 'dark-vdo',
    bg: '#090d16',
    gridLine: '',
    text: '#f8fafc',
    textMuted: '#94a3b8',
    accent: '#22d3ee',
    accentSoft: 'rgba(34,211,238,0.12)',
    card: 'rgba(15,23,42,0.6)',
    cardBorder: 'rgba(34,211,238,0.25)',
    pillBg: 'rgba(34,211,238,0.12)',
    pillText: '#67e8f9',
    codeBg: '#0b1220',
    codeText: '#e2e8f0',
    winBar: '#111827',
    termBg: '#05080f',
    termText: '#e2e8f0',
    tipBg: 'rgba(250,204,21,0.12)',
    tipBorder: 'rgba(250,204,21,0.4)',
    tipText: '#fde68a',
    okBg: 'rgba(34,197,94,0.15)',
    okText: '#86efac',
    progress: '#22d3ee',
  },
};

export const getTheme = (name?: string): Theme =>
  THEMES[(name as ThemeName) in THEMES ? (name as ThemeName) : 'light-grid'];

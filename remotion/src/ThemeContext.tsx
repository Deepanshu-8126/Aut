import React, { createContext, useContext } from 'react';
import { getTheme, Theme } from './theme';

const ThemeCtx = createContext<Theme>(getTheme('light-grid'));
export const ThemeProvider: React.FC<{ name?: string; children: React.ReactNode }> = ({ name, children }) => (
  <ThemeCtx.Provider value={getTheme(name)}>{children}</ThemeCtx.Provider>
);
export const useTheme = () => useContext(ThemeCtx);

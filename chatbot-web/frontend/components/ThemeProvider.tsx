'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode, useRef, MouseEvent } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: (e?: MouseEvent<HTMLButtonElement>) => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'light',
  toggleTheme: () => {},
});

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');
  const [mounted, setMounted] = useState(false);
  const lockRef = useRef(false);

  // Load saved theme once
  useEffect(() => {
    const saved = localStorage.getItem('theme') as Theme | null;
    if (saved === 'dark' || saved === 'light') {
      setTheme(saved);
    }
    setMounted(true);
  }, []);

  // Apply theme to HTML tag
  useEffect(() => {
    if (!mounted) return;
    const root = document.documentElement;
    const body = document.body;

    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    body.classList.remove('light', 'dark');
    body.classList.add(theme);
    root.setAttribute('data-theme', theme);
    body.setAttribute('data-theme', theme);

    localStorage.setItem('theme', theme);
  }, [theme, mounted]);

  const toggleTheme = useCallback((e?: MouseEvent<HTMLButtonElement>) => {
    if (e) {
      e.stopPropagation();
      e.preventDefault();
    }

    if (lockRef.current) return;

    lockRef.current = true;

    setTheme(prev => prev === 'light' ? 'dark' : 'light');

    setTimeout(() => {
      lockRef.current = false;
    }, 400);
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
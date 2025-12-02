'use client';

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
  useRef,
} from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'light',
  toggleTheme: () => {},
});

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');
  const [mounted, setMounted] = useState(false);

  // 🟩 1. Load theme from localStorage once (StrictMode safe)
  useEffect(() => {
    const saved = localStorage.getItem('theme') as Theme | null;
    if (saved === 'dark' || saved === 'light') {
      setTheme(saved);
    }
    setMounted(true);
  }, []);

  // 🟩 2. Apply theme to <html>
  useEffect(() => {
    if (!mounted) return;

    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);

    localStorage.setItem('theme', theme);
  }, [theme, mounted]);

  // 🟩 3. Prevent StrictMode from double-executing the handler
  const lockRef = useRef(false);

  const toggleTheme = useCallback(() => {
    if (lockRef.current) return;     // Block second call in same tick
    lockRef.current = true;

    // Release lock at end of microtask
    Promise.resolve().then(() => {
      lockRef.current = false;
    });

    setTheme(prev => {
      const next = prev === 'light' ? 'dark' : 'light';
      console.log(`🔄 Toggle: ${prev} → ${next}`);
      return next;
    });
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

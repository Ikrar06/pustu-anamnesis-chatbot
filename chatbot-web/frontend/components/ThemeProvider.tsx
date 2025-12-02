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
  const instanceIdRef = useRef(Math.random().toString(36).slice(2, 8));
  const lockRef = useRef(false);
  const toggleCountRef = useRef(0);

  // Load saved theme once
  useEffect(() => {
    const saved = localStorage.getItem('theme') as Theme | null;
    if (saved === 'dark' || saved === 'light') {
      setTheme(saved);
    }
    setMounted(true);
    console.log('ThemeProvider mounted, id=', instanceIdRef.current);
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
    
    console.log(`📦 [${instanceIdRef.current}] Applied theme:`, theme);

    localStorage.setItem('theme', theme);
  }, [theme, mounted]);

  const toggleTheme = useCallback((e?: MouseEvent<HTMLButtonElement>) => {
    // Stop event
    if (e) {
      e.stopPropagation();
      e.preventDefault();
    }
    
    // Check if locked
    if (lockRef.current) {
      console.log(`🔒 [${instanceIdRef.current}] toggle ignored (locked)`);
      return;
    }
    
    // Lock immediately
    lockRef.current = true;
    toggleCountRef.current++;
    const currentToggleId = toggleCountRef.current;
    
    console.log(`🔔 [${instanceIdRef.current}] Toggle #${currentToggleId} executing`);

    setTheme(prev => {
      const next = prev === 'light' ? 'dark' : 'light';
      console.log(`🔄 Theme toggled: ${prev} → ${next} (Toggle #${currentToggleId})`);
      return next;
    });
    
    // Unlock after delay
    setTimeout(() => {
      lockRef.current = false;
      console.log(`🔓 [${instanceIdRef.current}] Unlocked after toggle #${currentToggleId}`);
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
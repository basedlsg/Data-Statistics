import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Stanford-clean slate palette
        background: 'hsl(0, 0%, 100%)',
        foreground: 'hsl(240, 10%, 3.9%)',
        card: 'hsl(0, 0%, 100%)',
        'card-foreground': 'hsl(240, 10%, 3.9%)',
        primary: 'hsl(240, 5.9%, 10%)',
        'primary-foreground': 'hsl(0, 0%, 98%)',
        secondary: 'hsl(240, 4.8%, 95.9%)',
        'secondary-foreground': 'hsl(240, 5.9%, 10%)',
        muted: 'hsl(240, 4.8%, 95.9%)',
        'muted-foreground': 'hsl(240, 3.8%, 46.1%)',
        accent: 'hsl(240, 4.8%, 95.9%)',
        'accent-foreground': 'hsl(240, 5.9%, 10%)',
        // Ancient Egypt accent colors (subtle sand/gold)
        'accent-egypt': 'hsl(40, 40%, 65%)',
        'accent-egypt-light': 'hsl(40, 30%, 85%)',
        'accent-egypt-dark': 'hsl(40, 50%, 45%)',
        border: 'hsl(240, 5.9%, 90%)',
        input: 'hsl(240, 5.9%, 90%)',
        ring: 'hsl(240, 5.9%, 10%)',
      },
      borderRadius: {
        lg: '0.5rem',
        md: '0.375rem',
        sm: '0.25rem',
      },
      fontFamily: {
        sans: [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'ui-monospace',
          'SFMono-Regular',
          'Consolas',
          'Liberation Mono',
          'Menlo',
          'monospace',
        ],
      },
      transitionDuration: {
        DEFAULT: '150ms',
      },
    },
  },
  plugins: [],
};

export default config;

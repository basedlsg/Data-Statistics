import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'VC Hype Simulation Dashboard',
  description: 'Explore how market sentiment affects venture capital allocation across regional ecosystems',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background">
        <div className="flex min-h-screen flex-col">
          <header className="border-b border-border bg-card">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-2xl font-bold tracking-tight">VC Hype Simulation</h1>
                  <p className="text-sm text-muted-foreground">
                    Regional venture capital allocation under market sentiment
                  </p>
                </div>
                <nav className="flex gap-4 text-sm">
                  <a href="/" className="hover:text-accent-egypt transition-colors">
                    Overview
                  </a>
                  <a href="/regions" className="hover:text-accent-egypt transition-colors">
                    Regions
                  </a>
                  <a href="/traits" className="hover:text-accent-egypt transition-colors">
                    Traits
                  </a>
                  <a href="/hype" className="hover:text-accent-egypt transition-colors">
                    Hype
                  </a>
                  <a href="/founder" className="hover:text-accent-egypt transition-colors">
                    Founder
                  </a>
                  <a href="/sources" className="hover:text-accent-egypt transition-colors">
                    Sources
                  </a>
                </nav>
              </div>
            </div>
          </header>

          <main className="flex-1">{children}</main>

          <footer className="border-t border-border bg-card py-6">
            <div className="container mx-auto px-4">
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <div>
                  <span className="font-mono">Seed: Loading...</span>
                  {' • '}
                  <span className="font-mono">Hash: Loading...</span>
                </div>
                <div className="flex items-center gap-2">
                  <span>Powered by Claude Code</span>
                  <svg
                    className="h-4 w-4 text-accent-egypt"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M12 2L2 7v10c0 5.5 3.8 9.7 9 11 5.2-1.3 9-5.5 9-11V7l-10-5zm0 18c-3.9-1-7-4.5-7-8.5V8l7-3.5L19 8v3.5c0 4-3.1 7.5-7 8.5z" />
                  </svg>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}

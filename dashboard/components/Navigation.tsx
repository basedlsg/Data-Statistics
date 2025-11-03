'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Navigation() {
  const pathname = usePathname();

  const links = [
    { href: '/', label: 'Hype Cycles' },
    { href: '/pitch-theater', label: 'Pitch Theater' },
    { href: '/ai-scoring', label: 'AI Scoring Logic' },
  ];

  return (
    <nav className="glass-strong border-b border-white/20 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="text-heading-2 smooth-hover">
            VC Hype Simulation
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-1">
            {links.map(link => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all smooth-hover press-animation ${
                    isActive
                      ? 'glass-medium border border-white/30'
                      : 'glass-hover glass'
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}

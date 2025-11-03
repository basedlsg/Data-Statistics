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
        {children}
      </body>
    </html>
  );
}

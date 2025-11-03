export default function Page() {
  const titles = {
    traits: 'Feature Weights & Traits',
    hype: 'Hype State Analysis',
    founder: 'Founder Personas',
    sources: 'Data Sources & Provenance'
  };
  const pageName = '${page}';
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold section-title mb-4">{titles[pageName as keyof typeof titles] || 'Page'}</h1>
      <div className="bg-card border border-border rounded-lg p-12 text-center">
        <p className="text-lg text-muted-foreground">Coming soon...</p>
      </div>
    </div>
  );
}

# VC Hype Simulation Dashboard

Local-first Next.js dashboard for exploring VC Hype Simulation results with natural language queries, confidence intervals, and Ancient Egyptian-inspired design accents.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Create or edit `.env.local`:

```bash
# Path to simulation results directory (relative to dashboard/)
SIM_DATA_DIR=../results

# Use mock data for testing (1 = yes, 0 = no)
NEXT_PUBLIC_USE_MOCK=1
```

## Data Contract

The dashboard expects simulation outputs in the following format:

### Directory Structure

```
results/
├── run_42.json           # Individual run results
├── run_43.json
├── ...
├── aggregated_results.csv # Combined results (optional)
└── summary_stats.json    # Metadata about simulation
```

### run_*.json Format

Each file should contain an array or `{founders: [...]}` object with:

```typescript
{
  seed: number;
  run_id: number;
  t: number;              // Time step
  region: 'bay_area' | 'nyc' | 'boston' | 'la';
  stage: 'seed' | 'series_a' | 'series_b_plus';
  domain: 'ai' | 'bio' | 'consumer' | 'enterprise';
  founder_id: number;
  funded: boolean;
  lead: boolean;          // True if region led the round
  syndication: boolean;   // True if region co-invested
  dollars: number;        // Funding amount in millions
  score: number;          // Region's score for this founder
  prob?: number;          // Funding probability (optional)
  // Founder features (optional)
  revenue?: number;
  growth?: number;
  charisma?: number;
  vision?: number;
  traction_quality?: number;
  repeat_founder?: boolean;
  geo_flex?: number;
}
```

### summary_stats.json Format

```json
{
  "seed": 42,
  "n_founders": 200,
  "n_runs": 10,
  "git_hash": "abc123...",
  "timestamp": "2025-11-03T12:00:00Z"
}
```

## Features

### Natural Language Queries

Ask questions in plain English:

- **"Where is charisma most important?"** → Feature importance ranking
- **"Where am I most likely to get funded?"** → Funding likelihood with CIs
- **"Compare Champion vs RevenueFirst"** → Persona comparison
- **"Show domain/stage mix for NYC"** → Regional breakdown

### Pages

- **Overview** - KPIs, regional likelihood (with CIs), calibration chart
- **Regions** - Small multiples, lead vs syndication toggle, domain/stage stacks
- **Traits** - Hype slider, radar chart of effective weights
- **Hype** - State selector, likelihood shifts across regimes
- **Founder** - Champion vs Custom persona, probabilities, live narrative
- **Sources** - Provenance table, data files, timestamps

### Personas

- **Champion** - High charisma/vision, low revenue, AI focus
- **RevenueFirst** - High revenue/traction, enterprise focus
- **BioScience** - Boston-optimized, publication-heavy
- **ConsumerBrand** - LA-optimized, brand storyteller

### Design

- Stanford-clean base (white, slate/stone grays)
- Ancient Egyptian micro-accents (subtle gold sand underlines)
- 150-200ms transitions (Framer Motion)
- Accessible, keyboard-navigable, color-blind safe

## Development

### Mock Data Mode

Set `NEXT_PUBLIC_USE_MOCK=1` to use generated mock data for testing without simulation results.

### Project Structure

```
dashboard/
├── app/                   # Next.js App Router pages
│   ├── api/              # Server-side API routes
│   │   ├── meta/         # Simulation metadata
│   │   ├── runs/         # Founder runs (filterable)
│   │   └── summaries/    # Computed summaries with CIs
│   ├── regions/          # Regions page
│   ├── traits/           # Traits page
│   ├── hype/             # Hype page
│   ├── founder/          # Founder page
│   ├── sources/          # Sources page
│   └── layout.tsx        # Root layout
├── components/           # React components
├── lib/                  # Utilities
│   ├── data/            # Data loaders (JSON, mock, CI)
│   ├── nl/              # Natural language query parser
│   └── personas.ts      # Persona presets
└── public/              # Static assets
```

## Exporting Data from Simulation

To generate compatible data, run the Python simulation with:

```bash
python simulate.py --runs 10 --seed 42 --out results/
```

This will create `results/run_*.json` files readable by the dashboard.

## Tech Stack

- **Next.js 15** (App Router)
- **TypeScript 5**
- **Tailwind CSS 3**
- **Recharts 2** (charting)
- **Framer Motion 11** (animations)
- **parquetjs-lite** (Parquet support)

## License

MIT

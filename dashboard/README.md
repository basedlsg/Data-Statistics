# VC Hype Simulation Dashboard

**Beautiful, visual-first dashboard** for exploring venture capital allocation patterns across regional ecosystems.

![Dashboard Preview](https://via.placeholder.com/1200x600/F5F5F5/C9A96E?text=VC+Hype+Simulation+Dashboard)

## ✨ Features

### 📊 Visual Data Exploration
- **Funding Distribution** - See which regions get the most deals
- **Capital Deployment** - Track dollar flows across ecosystems
- **Feature Importance** - Understand what traits matter (charisma, vision, revenue, growth)
- **Domain Breakdown** - Analyze funding by sector (AI, Bio, Consumer, Enterprise)

### 💬 Natural Language Chatbot
Ask questions in plain English:
- "Where is charisma most important?"
- "Which region funds the most AI companies?"
- "Compare Champion vs RevenueFirst personas"

### 🎨 Beautiful Design
- Stanford-clean aesthetic with Ancient Egyptian gold accents
- Immediate visual clarity - understand data at a glance
- Responsive charts with Recharts
- Smooth animations and hover effects

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd dashboard
npm install
```

### 2. Run with Mock Data (No Simulation Required)

```bash
# Set mock mode in .env.local
echo "NEXT_PUBLIC_USE_MOCK=1" > .env.local

# Start dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) - you'll see the dashboard with generated mock data!

### 3. Run with Real Simulation Data

```bash
# First, run the simulation from parent directory
cd ..
python simulate.py --runs 10 --seed 42 --out results/

# Update .env.local to use real data
cd dashboard
echo "NEXT_PUBLIC_USE_MOCK=0" > .env.local
echo "SIM_DATA_DIR=../results" >> .env.local

# Start dev server
npm run dev
```

The dashboard will read from `../results/run_*.json` and `aggregated_results.csv`.

## 📁 Project Structure

```
dashboard/
├── app/
│   ├── page.tsx              # Main overview page (visual data explorer)
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles with Egypt accents
│   └── api/                  # Server-side data routes
│       ├── meta/route.ts     # Simulation metadata
│       ├── runs/route.ts     # Founder runs (filterable)
│       └── summaries/route.ts # Computed summaries
├── components/
│   ├── SimpleBarChart.tsx    # Clean bar chart component
│   ├── SimplePieChart.tsx    # Pie chart for domains
│   └── ChatBot.tsx           # Natural language query interface
└── lib/
    ├── data/                 # Data loaders and aggregators
    │   ├── loadMeta.ts       # Load simulation config
    │   ├── loadRuns.ts       # Load founder data
    │   ├── mock.ts           # Mock data generator
    │   └── ci.ts             # Confidence interval helpers
    ├── nl/                   # Natural language processing
    │   ├── parse.ts          # Intent parser
    │   └── answer.ts         # Response generator
    ├── personas.ts           # Founder persona presets
    └── types.ts              # TypeScript definitions
```

## 🎯 What You See on the Dashboard

### Top Section: Key Metrics (4 Cards)
1. **Total Deals** - Number of funded founders
2. **Funding Rate** - Percentage of founders who got funded
3. **Total Founders** - Founders across all simulation runs
4. **Regions** - Number of regional ecosystems

### Main Charts (2×2 Grid)
1. **Funding Distribution by Region** - Bar chart showing deal counts per region
2. **Capital Deployed by Region** - Bar chart showing dollars invested
3. **What Matters Most?** - Feature importance (average weights for charisma, vision, revenue, growth)
4. **Funding by Domain** - Pie chart of AI/Bio/Consumer/Enterprise breakdown

### Chatbot Section
- Interactive chat interface
- Ask natural language questions
- Get instant answers based on simulation data

### Regional Ecosystem Cards (Bottom)
- 4 detailed cards (Bay Area, NYC, Boston, LA)
- Shows deals, market share, capital, hype sensitivity
- Top 3 traits highlighted with badges
- Hover for visual feedback

## 🔧 Configuration

### Environment Variables

Create `.env.local`:

```bash
# Path to simulation results (relative to dashboard/)
SIM_DATA_DIR=../results

# Mock data mode (1 = use mock data, 0 = use real data)
NEXT_PUBLIC_USE_MOCK=0
```

### Data Contract

The dashboard expects these files in `SIM_DATA_DIR`:

#### `run_*.json` - Individual simulation runs
```json
{
  "founders": [
    {
      "seed": 42,
      "run_id": 0,
      "region": "bay_area",
      "stage": "seed",
      "domain": "ai",
      "founder_id": 0,
      "funded": true,
      "lead": true,
      "syndication": false,
      "dollars": 2.8,
      "score": 85.3
    }
  ]
}
```

#### `aggregated_results.csv` (optional, faster loading)
```csv
seed,run_id,region,stage,domain,founder_id,funded,lead,syndication,dollars,score
42,0,bay_area,seed,ai,0,True,True,False,2.8,85.3
```

#### `summary_stats.json` - Metadata
```json
{
  "seed": 42,
  "n_founders": 200,
  "n_runs": 10
}
```

## 🧪 Development

### Mock Data Mode
Perfect for development without running the full simulation:

```bash
NEXT_PUBLIC_USE_MOCK=1 npm run dev
```

Generates realistic mock data with:
- 1,000 founders across 5 runs
- 65% funding rate
- Regional and domain distributions
- Random feature values

### Real Data Mode
Use actual simulation results:

```bash
# Run simulation first
cd .. && python simulate.py --runs 10 --seed 42

# Start dashboard
cd dashboard
npm run dev
```

## 🎨 Design Philosophy

**Visual First, Simple Always**

1. **Immediate Understanding** - User sees key insights without scrolling
2. **Clean Charts** - Recharts with custom styling, no clutter
3. **Beautiful Gradients** - Subtle gold accents inspired by Ancient Egypt
4. **No Over-Engineering** - Simple components, clear data flow

## 🛠 Tech Stack

- **Next.js 15** - React framework with App Router
- **TypeScript 5** - Type safety
- **Tailwind CSS 3** - Utility-first styling
- **Recharts 2** - Declarative charting
- **Framer Motion 11** - Animations (future)

## 📊 Example Queries (Chatbot)

Try asking:
- "Where is charisma most important?"
- "Which region funds the most AI companies?"
- "What are my chances of getting funded?"
- "Compare Champion vs RevenueFirst"
- "Show domain mix for NYC"

## 🔮 Future Enhancements

- [ ] Hype cycle timeline visualization
- [ ] Interactive persona builder
- [ ] Confidence interval ribbons on charts
- [ ] Export charts as images
- [ ] Comparison mode (side-by-side regions)
- [ ] Mobile-optimized layouts

## 📝 License

MIT

---

**Built with Claude Code** | Powered by simulation data from `/simulate.py`

import { NextRequest, NextResponse } from 'next/server';
import { loadAggregatedRuns } from '@/lib/data/loadRuns';
import type { RunFilter } from '@/lib/data/loadRuns';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;

    // Build filter from query params
    const filter: RunFilter = {};

    const lead = searchParams.get('lead');
    if (lead !== null) {
      filter.lead = lead === 'true' || lead === '1';
    }

    const syndication = searchParams.get('syndication');
    if (syndication !== null) {
      filter.syndication = syndication === 'true' || syndication === '1';
    }

    const region = searchParams.get('region');
    if (region) {
      filter.region = region;
    }

    const domain = searchParams.get('domain');
    if (domain) {
      filter.domain = domain;
    }

    const stage = searchParams.get('stage');
    if (stage) {
      filter.stage = stage;
    }

    const funded = searchParams.get('funded');
    if (funded !== null) {
      filter.funded = funded === 'true' || funded === '1';
    }

    const runId = searchParams.get('run_id');
    if (runId) {
      filter.run_id = parseInt(runId, 10);
    }

    const runs = await loadAggregatedRuns(filter);

    return NextResponse.json({
      count: runs.length,
      data: runs,
    });
  } catch (error) {
    console.error('Error in /api/runs:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

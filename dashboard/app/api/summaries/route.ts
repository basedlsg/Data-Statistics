import { NextRequest, NextResponse } from 'next/server';
import { loadAggregatedRuns } from '@/lib/data/loadRuns';
import {
  groupByAndComputeCI,
  computeFundingLikelihoodByRegion,
  computeCalibration,
} from '@/lib/data/ci';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const metric = searchParams.get('metric');
    const groupBy = searchParams.get('group_by');

    const runs = await loadAggregatedRuns();

    if (metric === 'funding_likelihood') {
      const summaries = computeFundingLikelihoodByRegion(runs);
      return NextResponse.json({ summaries });
    }

    if (metric === 'calibration') {
      const calibration = computeCalibration(runs);
      return NextResponse.json({ calibration });
    }

    // Generic group by and CI computation
    if (metric && groupBy) {
      const summaries = groupByAndComputeCI(runs, groupBy as any, metric as any);
      return NextResponse.json({ summaries });
    }

    return NextResponse.json({ error: 'Missing metric or group_by parameter' }, { status: 400 });
  } catch (error) {
    console.error('Error in /api/summaries:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

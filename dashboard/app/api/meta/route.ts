import { NextResponse } from 'next/server';
import { loadMeta } from '@/lib/data/loadMeta';

export async function GET() {
  try {
    const meta = await loadMeta();

    if (!meta) {
      return NextResponse.json({ error: 'Could not load metadata' }, { status: 500 });
    }

    return NextResponse.json(meta);
  } catch (error) {
    console.error('Error in /api/meta:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

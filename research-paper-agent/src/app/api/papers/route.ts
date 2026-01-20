import { NextResponse } from 'next/server';
import prisma from '@/lib/db';

export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');

    try {
        const papers = await prisma.paper.findMany({
            where: category && category !== 'all' ? { category } : undefined,
            orderBy: { publishedAt: 'desc' },
            take: 10,
        });

        return NextResponse.json({ papers });
    } catch (error) {
        console.error('Failed to fetch papers:', error);
        return NextResponse.json({ error: 'Failed to fetch papers' }, { status: 500 });
    }
}

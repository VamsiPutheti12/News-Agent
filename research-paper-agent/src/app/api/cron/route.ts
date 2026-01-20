import { NextResponse } from 'next/server';
import prisma from '@/lib/db';
import { fetchArxivPapers, filterRecentPapers, getWeekStart } from '@/lib/arxiv';

// This endpoint is called by Vercel Cron every Saturday at 9 AM
export async function GET(request: Request) {
    // Verify cron secret for security (optional but recommended)
    const authHeader = request.headers.get('authorization');
    if (process.env.CRON_SECRET && authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    try {
        // Fetch papers from arXiv
        const allPapers = await fetchArxivPapers(100);

        // Filter to last 7 days
        const recentPapers = filterRecentPapers(allPapers, 7);

        // Take top 10
        const top10 = recentPapers.slice(0, 10);

        const weekOf = getWeekStart();

        // Store in database
        let savedCount = 0;
        for (const paper of top10) {
            try {
                await prisma.paper.upsert({
                    where: { arxivId: paper.arxivId },
                    update: {
                        title: paper.title,
                        authors: paper.authors,
                        abstract: paper.abstract,
                        category: paper.category,
                        pdfUrl: paper.pdfUrl,
                        publishedAt: paper.publishedAt,
                        weekOf,
                    },
                    create: {
                        arxivId: paper.arxivId,
                        title: paper.title,
                        authors: paper.authors,
                        abstract: paper.abstract,
                        category: paper.category,
                        pdfUrl: paper.pdfUrl,
                        publishedAt: paper.publishedAt,
                        weekOf,
                    },
                });
                savedCount++;
            } catch (err) {
                console.error(`Failed to save paper ${paper.arxivId}:`, err);
            }
        }

        return NextResponse.json({
            success: true,
            message: `Fetched and saved ${savedCount} papers`,
            weekOf: weekOf.toISOString(),
        });
    } catch (error) {
        console.error('Cron job failed:', error);
        return NextResponse.json({ error: 'Failed to fetch papers' }, { status: 500 });
    }
}

'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import PaperCard from '@/components/PaperCard';
import CategoryFilter from '@/components/CategoryFilter';

interface Paper {
  id: string;
  arxivId: string;
  title: string;
  authors: string[];
  abstract: string;
  category: string;
  pdfUrl: string;
  publishedAt: string;
}

export default function Home() {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('all');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPapers();
  }, [category]);

  const fetchPapers = async () => {
    setLoading(true);
    setError(null);

    try {
      const url = category === 'all'
        ? '/api/papers'
        : `/api/papers?category=${encodeURIComponent(category)}`;

      const res = await fetch(url);

      if (!res.ok) {
        throw new Error('Failed to fetch papers');
      }

      const data = await res.json();
      setPapers(data.papers || []);
    } catch (err) {
      console.error('Error fetching papers:', err);
      setError('Could not load papers. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      <Header />

      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* Filter */}
        <div className="mb-8">
          <CategoryFilter selected={category} onChange={setCategory} />
        </div>

        {/* Content */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-500 dark:text-red-400">{error}</p>
            <button
              onClick={fetchPapers}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        ) : papers.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">
              No papers found. Papers will be fetched every Saturday at 9 AM.
            </p>
            <button
              onClick={async () => {
                setLoading(true);
                await fetch('/api/cron');
                fetchPapers();
              }}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Fetch Papers Now
            </button>
          </div>
        ) : (
          <div className="grid gap-6">
            {papers.map((paper) => (
              <PaperCard key={paper.id} paper={paper} />
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-700 py-6 mt-12">
        <p className="text-center text-sm text-gray-500 dark:text-gray-400">
          Research Paper Agent — Aggregating top AI/ML papers from arXiv
        </p>
      </footer>
    </div>
  );
}

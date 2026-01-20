'use client';

import { useState } from 'react';

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

interface PaperCardProps {
    paper: Paper;
}

export default function PaperCard({ paper }: PaperCardProps) {
    const [expanded, setExpanded] = useState(false);

    const formattedDate = new Date(paper.publishedAt).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });

    const displayAbstract = expanded
        ? paper.abstract
        : paper.abstract.slice(0, 250) + (paper.abstract.length > 250 ? '...' : '');

    const categoryColors: Record<string, string> = {
        'Artificial Intelligence': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        'Machine Learning': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
        'Deep Learning': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
        'Computer Vision': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
        'NLP': 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200',
    };

    const categoryClass = categoryColors[paper.category] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';

    return (
        <article className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 shadow-sm hover:shadow-md transition-shadow">
            {/* Header */}
            <div className="flex items-start justify-between gap-4 mb-3">
                <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${categoryClass}`}>
                    {paper.category}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap">
                    {formattedDate}
                </span>
            </div>

            {/* Title */}
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 leading-tight">
                <a
                    href={`https://arxiv.org/abs/${paper.arxivId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                >
                    {paper.title}
                </a>
            </h2>

            {/* Authors */}
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {paper.authors.slice(0, 5).join(', ')}
                {paper.authors.length > 5 && ` +${paper.authors.length - 5} more`}
            </p>

            {/* Abstract */}
            <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                {displayAbstract}
                {paper.abstract.length > 250 && (
                    <button
                        onClick={() => setExpanded(!expanded)}
                        className="ml-1 text-blue-600 dark:text-blue-400 hover:underline font-medium"
                    >
                        {expanded ? 'Show less' : 'Read more'}
                    </button>
                )}
            </p>

            {/* Actions */}
            <div className="flex items-center gap-3">
                <a
                    href={paper.pdfUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors"
                >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    PDF
                </a>
                <a
                    href={`https://arxiv.org/abs/${paper.arxivId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                    arXiv
                </a>
            </div>
        </article>
    );
}

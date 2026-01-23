'use client';

interface CategoryFilterProps {
    selected: string;
    onChange: (category: string) => void;
}

const CATEGORIES = [
    { id: 'all', label: 'All' },
    { id: 'Artificial Intelligence', label: 'AI' },
    { id: 'Machine Learning', label: 'ML' },
    { id: 'Deep Learning', label: 'Deep Learning' },
    { id: 'Reinforcement Learning', label: 'RL' },
    { id: 'AI Safety', label: 'AI Safety' },
    { id: 'Computer Vision', label: 'Vision' },
    { id: 'NLP', label: 'NLP' },
];

export default function CategoryFilter({ selected, onChange }: CategoryFilterProps) {
    return (
        <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((cat) => (
                <button
                    key={cat.id}
                    onClick={() => onChange(cat.id)}
                    className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${selected === cat.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
                        }`}
                >
                    {cat.label}
                </button>
            ))}
        </div>
    );
}

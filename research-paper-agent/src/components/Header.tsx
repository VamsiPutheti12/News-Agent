import ThemeToggle from './ThemeToggle';

export default function Header() {
    return (
        <header className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
            <div className="max-w-5xl mx-auto px-4 py-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                            Research Paper Agent
                        </h1>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                            Top 10 AI/ML papers from arXiv this week
                        </p>
                    </div>
                    <ThemeToggle />
                </div>
            </div>
        </header>
    );
}

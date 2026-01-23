// arXiv API Client
// Fetches papers from arXiv API for AI/ML categories

export interface ArxivPaper {
    arxivId: string;
    title: string;
    authors: string[];
    abstract: string;
    category: string;
    pdfUrl: string;
    publishedAt: Date;
}

// arXiv category mappings
const ARXIV_CATEGORIES = {
    'Artificial Intelligence': 'cs.AI',
    'Machine Learning': 'cs.LG',
    'Neural Computing': 'cs.NE',
    'Statistical ML': 'stat.ML',
    'Reinforcement Learning': 'cs.LG', // RL papers are often under cs.LG
    'AI Safety': 'cs.AI', // AI Safety papers are often under cs.AI
};

const CATEGORY_QUERY = Object.values(ARXIV_CATEGORIES).map(cat => `cat:${cat}`).join('+OR+');

export async function fetchArxivPapers(maxResults: number = 50): Promise<ArxivPaper[]> {
    const apiUrl = `http://export.arxiv.org/api/query?search_query=${CATEGORY_QUERY}&sortBy=submittedDate&sortOrder=descending&max_results=${maxResults}`;

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`arXiv API error: ${response.status}`);
        }

        const xmlText = await response.text();
        return parseArxivResponse(xmlText);
    } catch (error) {
        console.error('Failed to fetch arXiv papers:', error);
        return [];
    }
}

function parseArxivResponse(xml: string): ArxivPaper[] {
    const papers: ArxivPaper[] = [];

    // Parse entries from XML
    const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
    let match;

    while ((match = entryRegex.exec(xml)) !== null) {
        const entry = match[1];

        // Extract fields
        const id = extractField(entry, 'id');
        const title = extractField(entry, 'title').replace(/\s+/g, ' ').trim();
        const abstract = extractField(entry, 'summary').replace(/\s+/g, ' ').trim();
        const published = extractField(entry, 'published');

        // Extract authors
        const authors: string[] = [];
        const authorRegex = /<author>\s*<name>([^<]+)<\/name>/g;
        let authorMatch;
        while ((authorMatch = authorRegex.exec(entry)) !== null) {
            authors.push(authorMatch[1].trim());
        }

        // Extract category - first check arXiv category, then use keyword detection
        const categoryMatch = entry.match(/<arxiv:primary_category[^>]*term="([^"]+)"/);
        let category = categoryMatch ? mapCategory(categoryMatch[1]) : 'Machine Learning';

        // Override category based on content analysis for RL and AI Safety
        if (detectRLPaper(title, abstract)) {
            category = 'Reinforcement Learning';
        } else if (detectSafetyPaper(title, abstract)) {
            category = 'AI Safety';
        }

        // Extract PDF link
        const pdfMatch = entry.match(/<link[^>]*title="pdf"[^>]*href="([^"]+)"/);
        const pdfUrl = pdfMatch ? pdfMatch[1] : id.replace('abs', 'pdf');

        // Extract arXiv ID from URL
        const arxivId = id.split('/abs/').pop() || id;

        if (title && abstract) {
            papers.push({
                arxivId,
                title,
                authors,
                abstract,
                category,
                pdfUrl,
                publishedAt: new Date(published),
            });
        }
    }

    return papers;
}

function extractField(entry: string, field: string): string {
    const regex = new RegExp(`<${field}[^>]*>([\\s\\S]*?)<\\/${field}>`);
    const match = entry.match(regex);
    return match ? match[1].trim() : '';
}

function mapCategory(arxivCategory: string): string {
    const mapping: Record<string, string> = {
        'cs.AI': 'Artificial Intelligence',
        'cs.LG': 'Machine Learning',
        'cs.NE': 'Deep Learning',
        'stat.ML': 'Machine Learning',
        'cs.CV': 'Computer Vision',
        'cs.CL': 'NLP',
        'cs.RO': 'Robotics',
        'cs.MA': 'Reinforcement Learning', // Multi-Agent Systems (often RL)
        'cs.GT': 'AI Safety', // Game Theory (often AI Safety related)
    };
    return mapping[arxivCategory] || 'Machine Learning';
}

// Check if paper title/abstract suggests Reinforcement Learning
export function detectRLPaper(title: string, abstract: string): boolean {
    const rlKeywords = [
        'reinforcement learning', 'rl agent', 'reward', 'policy gradient',
        'q-learning', 'actor-critic', 'markov decision', 'mdp',
        'deep q', 'dqn', 'ppo', 'a3c', 'sac', 'td3', 'rl-based',
        'multi-agent', 'reward shaping', 'exploration', 'exploitation'
    ];
    const text = (title + ' ' + abstract).toLowerCase();
    return rlKeywords.some(keyword => text.includes(keyword));
}

// Check if paper title/abstract suggests AI Safety
export function detectSafetyPaper(title: string, abstract: string): boolean {
    const safetyKeywords = [
        'ai safety', 'alignment', 'safe ai', 'adversarial', 'robustness',
        'interpretability', 'explainability', 'fairness', 'bias',
        'trustworthy', 'reliable', 'secure', 'privacy', 'ethical',
        'human feedback', 'rlhf', 'value alignment', 'unsafe', 'jailbreak',
        'red teaming', 'guardrails', 'constitutional ai'
    ];
    const text = (title + ' ' + abstract).toLowerCase();
    return safetyKeywords.some(keyword => text.includes(keyword));
}

// Filter papers from the past week
export function filterRecentPapers(papers: ArxivPaper[], days: number = 7): ArxivPaper[] {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);

    return papers.filter(paper => paper.publishedAt >= cutoff);
}

// Get start of the current week (Sunday)
export function getWeekStart(): Date {
    const now = new Date();
    const dayOfWeek = now.getDay();
    const diff = now.getDate() - dayOfWeek;
    return new Date(now.setDate(diff));
}

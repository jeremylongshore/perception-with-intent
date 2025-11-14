import { useEffect, useState } from 'react'

interface Article {
  id: string
  title: string
  summary: string
  source: string
  url: string
  ai_tags: string[]
  relevance_score: number
  date_found: string
}

export default function Dashboard() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // TODO: Connect to Firestore
    // For now, show placeholder
    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-zinc-500">Loading articles...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-primary">News Feed</h2>
          <p className="text-zinc-600 mt-1">Real-time intelligence from monitored sources</p>
        </div>
        <button className="btn-primary">
          Run Analysis
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="text-zinc-500 text-sm">Articles Today</div>
          <div className="text-3xl font-bold text-primary mt-2">0</div>
        </div>
        <div className="card">
          <div className="text-zinc-500 text-sm">Active Topics</div>
          <div className="text-3xl font-bold text-primary mt-2">0</div>
        </div>
        <div className="card">
          <div className="text-zinc-500 text-sm">Sources</div>
          <div className="text-3xl font-bold text-primary mt-2">3</div>
        </div>
        <div className="card">
          <div className="text-zinc-500 text-sm">Avg Relevance</div>
          <div className="text-3xl font-bold text-primary mt-2">-</div>
        </div>
      </div>

      {/* Articles */}
      <div className="space-y-4">
        {articles.length === 0 ? (
          <div className="card text-center py-12">
            <div className="text-zinc-400 text-lg">No articles yet</div>
            <p className="text-zinc-500 text-sm mt-2">
              Configure topics and run your first analysis
            </p>
          </div>
        ) : (
          articles.map((article) => (
            <div key={article.id} className="card hover:border-zinc-200">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-primary hover:underline">
                    <a href={article.url} target="_blank" rel="noopener noreferrer">
                      {article.title}
                    </a>
                  </h3>
                  <p className="text-zinc-600 mt-2">{article.summary}</p>
                  <div className="flex items-center gap-4 mt-4 text-sm">
                    <span className="text-zinc-500">{article.source}</span>
                    <span className="text-zinc-400">•</span>
                    <span className="text-zinc-500">Score: {article.relevance_score}</span>
                    <div className="flex gap-2 ml-auto">
                      {article.ai_tags.map((tag) => (
                        <span
                          key={tag}
                          className="bg-zinc-100 text-zinc-700 px-2 py-1 rounded text-xs"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

import { useState } from 'react'

interface DailySummary {
  id: string
  date: string
  article_count: number
  main_topics: string[]
  top_sources: Record<string, number>
  highlights: string[]
}

export default function DailyBriefs() {
  const [summaries, setSummaries] = useState<DailySummary[]>([])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-primary">Daily Intelligence Briefs</h2>
        <p className="text-zinc-600 mt-1">Executive summaries with strategic insights</p>
      </div>

      {/* Summaries */}
      <div className="space-y-6">
        {summaries.length === 0 ? (
          <div className="card text-center py-12">
            <div className="text-zinc-400 text-lg">No briefs generated yet</div>
            <p className="text-zinc-500 text-sm mt-2">
              Daily summaries will appear here after analysis runs
            </p>
          </div>
        ) : (
          summaries.map((summary) => (
            <div key={summary.id} className="card">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-primary">
                    {new Date(summary.date).toLocaleDateString('en-US', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </h3>
                  <p className="text-zinc-500 text-sm mt-1">
                    {summary.article_count} articles analyzed
                  </p>
                </div>
              </div>

              {/* Top Topics */}
              <div className="mb-4">
                <h4 className="text-sm font-medium text-zinc-700 mb-2">Main Topics</h4>
                <div className="flex gap-2">
                  {summary.main_topics.map((topic) => (
                    <span
                      key={topic}
                      className="bg-zinc-100 text-zinc-700 px-3 py-1 rounded-full text-sm"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              </div>

              {/* Highlights */}
              <div className="mb-4">
                <h4 className="text-sm font-medium text-zinc-700 mb-3">Strategic Highlights</h4>
                <ul className="space-y-2">
                  {summary.highlights.map((highlight, index) => (
                    <li key={index} className="text-zinc-600 flex">
                      <span className="text-zinc-400 mr-2">•</span>
                      <span>{highlight}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Top Sources */}
              <div>
                <h4 className="text-sm font-medium text-zinc-700 mb-2">Top Sources</h4>
                <div className="grid grid-cols-3 gap-3">
                  {Object.entries(summary.top_sources).map(([source, count]) => (
                    <div key={source} className="bg-zinc-50 px-3 py-2 rounded">
                      <div className="text-sm text-zinc-600">{source}</div>
                      <div className="text-lg font-semibold text-primary">{count}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

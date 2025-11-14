import { useEffect, useState } from 'react'
import { collection, query, orderBy, limit, getDocs } from 'firebase/firestore'
import { db } from '../firebase'

interface Brief {
  id: string
  date: string
  executiveSummary: string
  highlights: string[]
  metrics?: {
    articleCount: number
    topSources?: Record<string, number>
    mainTopics?: string[]
  }
}

export default function TodayBriefCard() {
  const [brief, setBrief] = useState<Brief | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchBrief = async () => {
      try {
        const briefsRef = collection(db, 'briefs')
        const q = query(briefsRef, orderBy('date', 'desc'), limit(1))
        const snapshot = await getDocs(q)

        if (!snapshot.empty) {
          const doc = snapshot.docs[0]
          setBrief({
            id: doc.id,
            ...doc.data()
          } as Brief)
        }
      } catch (err) {
        console.error('Error fetching brief:', err)
        setError(err instanceof Error ? err.message : 'Failed to load brief')
      } finally {
        setLoading(false)
      }
    }

    fetchBrief()
  }, [])

  if (loading) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">Today's Brief</h3>
        <div className="flex items-center justify-center py-8">
          <div className="text-zinc-500">Loading brief...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card border-red-200 bg-red-50">
        <h3 className="text-xl font-bold text-red-700 mb-4">Today's Brief</h3>
        <div className="text-red-600 text-sm">
          ⚠️ Error loading brief: {error}
        </div>
      </div>
    )
  }

  if (!brief) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">Today's Brief</h3>
        <div className="text-center py-8">
          <div className="text-zinc-400 text-lg">No brief available yet</div>
          <p className="text-zinc-500 text-sm mt-2">
            Daily briefs are generated during ingestion runs
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-bold text-primary">Today's Brief</h3>
        <span className="text-sm text-zinc-500">{brief.date}</span>
      </div>

      {/* Executive Summary */}
      <div className="mb-6">
        <h4 className="text-sm font-semibold text-zinc-700 mb-2">Executive Summary</h4>
        <p className="text-zinc-600 leading-relaxed">{brief.executiveSummary}</p>
      </div>

      {/* Highlights */}
      {brief.highlights && brief.highlights.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-zinc-700 mb-3">Key Highlights</h4>
          <ul className="space-y-2">
            {brief.highlights.map((highlight, index) => (
              <li key={index} className="flex items-start">
                <span className="text-primary font-bold mr-2">•</span>
                <span className="text-zinc-600 flex-1">{highlight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Metrics */}
      {brief.metrics && (
        <div className="border-t border-zinc-200 pt-4">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div>
              <div className="text-zinc-500 text-xs">Articles Analyzed</div>
              <div className="text-xl font-bold text-primary mt-1">
                {brief.metrics.articleCount}
              </div>
            </div>
            {brief.metrics.mainTopics && brief.metrics.mainTopics.length > 0 && (
              <div className="col-span-2">
                <div className="text-zinc-500 text-xs mb-2">Main Topics</div>
                <div className="flex flex-wrap gap-2">
                  {brief.metrics.mainTopics.map((topic) => (
                    <span
                      key={topic}
                      className="bg-zinc-100 text-zinc-700 px-2 py-1 rounded text-xs"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

import { useEffect, useState } from 'react'
import { collection, getDocs } from 'firebase/firestore'
import { db, auth } from '../firebase'

interface Topic {
  id: string
  name?: string
  keywords?: string[]
  category?: string
  active?: boolean
  lastUpdated?: { seconds: number }
}

export default function TopicWatchlistCard() {
  const [topics, setTopics] = useState<Topic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const user = auth.currentUser
        if (!user) {
          setError('Not authenticated')
          setLoading(false)
          return
        }

        const topicsRef = collection(db, 'users', user.uid, 'topics')
        const snapshot = await getDocs(topicsRef)

        const topicsList = snapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data()
        })) as Topic[]

        setTopics(topicsList)
      } catch (err) {
        console.error('Error fetching topics:', err)
        setError(err instanceof Error ? err.message : 'Failed to load topics')
      } finally {
        setLoading(false)
      }
    }

    fetchTopics()
  }, [])

  if (loading) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">Topic Watchlist</h3>
        <div className="flex items-center justify-center py-8">
          <div className="text-zinc-500">Loading topics...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card border-red-200 bg-red-50">
        <h3 className="text-xl font-bold text-red-700 mb-4">Topic Watchlist</h3>
        <div className="text-red-600 text-sm">
          ⚠️ Error loading topics: {error}
        </div>
      </div>
    )
  }

  if (topics.length === 0) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">Topic Watchlist</h3>
        <div className="text-center py-8">
          <div className="text-zinc-400 text-lg">No topics configured</div>
          <p className="text-zinc-500 text-sm mt-2">
            Add topics to start tracking relevant news
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-primary">Topic Watchlist</h3>
        <span className="text-sm text-zinc-500">{topics.length} active</span>
      </div>

      <div className="space-y-3">
        {topics.map((topic) => (
          <div
            key={topic.id}
            className="p-4 border border-zinc-200 rounded-lg hover:border-zinc-300 transition-colors"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h4 className="font-semibold text-zinc-800">
                  {topic.name || topic.id}
                </h4>
                {topic.keywords && topic.keywords.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {topic.keywords.map((keyword, index) => (
                      <span
                        key={index}
                        className="bg-zinc-100 text-zinc-600 px-2 py-0.5 rounded text-xs"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <div className="flex items-center gap-2">
                {topic.category && (
                  <span className="text-xs text-zinc-500 bg-zinc-100 px-2 py-1 rounded">
                    {topic.category}
                  </span>
                )}
                {topic.active !== undefined && (
                  <div
                    className={`h-2 w-2 rounded-full ${
                      topic.active ? 'bg-green-500' : 'bg-zinc-300'
                    }`}
                    title={topic.active ? 'Active' : 'Inactive'}
                  />
                )}
              </div>
            </div>
            {topic.lastUpdated && (
              <div className="text-xs text-zinc-400 mt-2">
                Last updated: {new Date(topic.lastUpdated.seconds * 1000).toLocaleDateString()}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

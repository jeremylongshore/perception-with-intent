import { useState } from 'react'

interface Topic {
  id: string
  keywords: string[]
  category: string
  active: boolean
}

export default function Topics() {
  const [topics, setTopics] = useState<Topic[]>([])
  const [showAddForm, setShowAddForm] = useState(false)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-primary">Monitored Topics</h2>
          <p className="text-zinc-600 mt-1">Manage keywords and categories for news tracking</p>
        </div>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn-primary"
        >
          + Add Topic
        </button>
      </div>

      {/* Add Topic Form */}
      {showAddForm && (
        <div className="card bg-zinc-50">
          <h3 className="text-lg font-semibold text-primary mb-4">New Topic</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-2">
                Keywords (comma-separated)
              </label>
              <input
                type="text"
                className="input w-full"
                placeholder="AI, machine learning, artificial intelligence"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-2">
                Category
              </label>
              <select className="input w-full">
                <option>Technology</option>
                <option>Business</option>
                <option>Politics</option>
                <option>Sports</option>
                <option>Science</option>
              </select>
            </div>
            <div className="flex gap-2">
              <button className="btn-primary">Save Topic</button>
              <button
                onClick={() => setShowAddForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Topics List */}
      <div className="space-y-4">
        {topics.length === 0 ? (
          <div className="card text-center py-12">
            <div className="text-zinc-400 text-lg">No topics configured</div>
            <p className="text-zinc-500 text-sm mt-2">
              Add your first topic to start monitoring news
            </p>
          </div>
        ) : (
          topics.map((topic) => (
            <div key={topic.id} className="card">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-semibold text-primary">{topic.category}</h3>
                    <span className={`px-2 py-1 rounded text-xs ${
                      topic.active
                        ? 'bg-green-100 text-green-700'
                        : 'bg-zinc-100 text-zinc-500'
                    }`}>
                      {topic.active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <div className="flex gap-2 mt-3">
                    {topic.keywords.map((keyword) => (
                      <span
                        key={keyword}
                        className="bg-zinc-100 text-zinc-700 px-3 py-1 rounded-full text-sm"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
                <button className="text-zinc-400 hover:text-zinc-600">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

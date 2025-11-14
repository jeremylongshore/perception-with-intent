export default function About() {
  return (
    <div className="max-w-4xl mx-auto space-y-12">
      {/* Hero */}
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold text-primary">
          Stop drowning in news.<br />Start seeing what matters.
        </h1>
        <p className="text-xl text-zinc-600 max-w-2xl mx-auto">
          Perception uses AI to cut through the noise and deliver the intelligence you actually need.
        </p>
      </div>

      {/* Value Props */}
      <div className="grid md:grid-cols-3 gap-8">
        <div className="card text-center">
          <div className="text-4xl mb-4">🎯</div>
          <h3 className="text-lg font-semibold text-primary mb-2">Source-Agnostic</h3>
          <p className="text-zinc-600 text-sm">
            Monitor any topic from any source. RSS feeds, APIs, custom connectors.
          </p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">🤖</div>
          <h3 className="text-lg font-semibold text-primary mb-2">AI-Powered</h3>
          <p className="text-zinc-600 text-sm">
            Gemini 2.0 generates summaries, tags, and strategic insights automatically.
          </p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-lg font-semibold text-primary mb-2">Executive Dashboard</h3>
          <p className="text-zinc-600 text-sm">
            Real-time intelligence delivered via clean, professional interface.
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="card">
        <h2 className="text-2xl font-bold text-primary mb-6">How Perception Works</h2>
        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-semibold">
              1
            </div>
            <div>
              <h3 className="font-semibold text-primary">Configure Topics</h3>
              <p className="text-zinc-600 text-sm">
                Define keywords and categories you want to monitor.
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-semibold">
              2
            </div>
            <div>
              <h3 className="font-semibold text-primary">Automated Collection</h3>
              <p className="text-zinc-600 text-sm">
                8 AI agents work together to collect, filter, and analyze news from multiple sources.
              </p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-semibold">
              3
            </div>
            <div>
              <h3 className="font-semibold text-primary">Strategic Insights</h3>
              <p className="text-zinc-600 text-sm">
                Daily executive briefs highlight patterns, trends, and strategic implications.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="card bg-zinc-50">
        <h2 className="text-2xl font-bold text-primary mb-6">Built on Enterprise-Grade Technology</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-primary mb-2">Backend</h3>
            <ul className="text-zinc-600 text-sm space-y-1">
              <li>• Google ADK (Agent Development Kit)</li>
              <li>• Vertex AI Agent Engine</li>
              <li>• A2A Protocol (Agent-to-Agent)</li>
              <li>• Gemini 2.0 Flash</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-primary mb-2">Infrastructure</h3>
            <ul className="text-zinc-600 text-sm space-y-1">
              <li>• Firebase (Hosting + Firestore)</li>
              <li>• Cloud Run (serverless scale-to-zero)</li>
              <li>• Terraform (Infrastructure as Code)</li>
              <li>• GitHub Actions (CI/CD)</li>
            </ul>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="card text-center bg-primary text-white">
        <h2 className="text-2xl font-bold mb-4">Want this for your team?</h2>
        <p className="text-white/90 mb-6 max-w-xl mx-auto">
          We're in private beta right now. Reach out if you'd like early access for your organization.
        </p>
        <button className="bg-white text-primary px-8 py-3 rounded-lg font-semibold hover:bg-zinc-100 transition-colors">
          Get Early Access
        </button>
      </div>

      {/* Footer */}
      <div className="text-center text-zinc-500 text-sm pt-8 border-t border-zinc-100">
        <p>Powered by Google Cloud • Built with ADK + Vertex AI Agent Engine</p>
        <p className="mt-2">© 2025 Perception. All rights reserved.</p>
      </div>
    </div>
  )
}

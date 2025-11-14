import { auth } from '../firebase'

export default function FooterBranding() {
  const user = auth.currentUser

  return (
    <footer className="mt-12 py-8 border-t border-zinc-200">
      <div className="text-center">
        <h3 className="text-lg font-bold text-primary">
          Perception With Intent
        </h3>
        <p className="text-zinc-600 text-sm mt-2">
          Created by{' '}
          <a
            href="https://intentsolutions.io"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary hover:underline font-medium"
          >
            intent solutions io
          </a>
        </p>
        {user && (
          <p className="text-zinc-400 text-xs mt-3">
            Logged in as: {user.email}
          </p>
        )}
      </div>
    </footer>
  )
}

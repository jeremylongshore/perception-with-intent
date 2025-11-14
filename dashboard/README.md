# Perception Dashboard

React + TypeScript dashboard with HustleStats.io inspired design.

## Color Scheme

Clean, minimalist zinc/gray palette:
- **Primary:** `#18181b` (zinc-900) - Dark, professional
- **Backgrounds:** White + `#f4f4f5` (zinc-50)
- **Text:** Zinc shades (900 → 300)
- **Accents:** Minimal, focused on typography

See `../COLOR_SCHEME.md` for complete palette.

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# → http://localhost:3000

# Build for production
npm run build

# Preview production build
npm run preview
```

## Pages

- **Dashboard** (`/`) - Real-time article feed
- **Topics** (`/topics`) - Manage monitoring keywords
- **Daily Briefs** (`/briefs`) - Executive summaries

## Firebase Integration

TODO: Add Firestore connection

```typescript
// lib/firebase.ts
import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  // Add config from Firebase Console
}

const app = initializeApp(firebaseConfig)
export const db = getFirestore(app)
```

## Components

All styled with HustleStats colors:
- Clean card design with subtle borders
- Minimal hover effects
- Typography-focused layout
- Professional zinc/gray palette

## Deploy to Firebase Hosting

```bash
npm run build
firebase deploy --only hosting
```

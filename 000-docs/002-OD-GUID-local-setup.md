# Local Development Setup - Perception With Intent

**Project:** perception-with-intent
**Created:** 2025-11-14
**Version:** 1.0

---

## Prerequisites

### Required
- **Node.js** 18+ (for dashboard and seed scripts)
- **Python** 3.11+ (for agents and tools)
- **Google Cloud Project** with Firestore Native Mode enabled
- **Firebase CLI** installed (`npm install -g firebase-tools`)

### GCP Setup

**Project ID:** `perception-with-intent`

**Required APIs:**
```bash
gcloud services enable firestore.googleapis.com
gcloud services enable identitytoolkit.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

**Firestore Native Mode:**
- ⚠️ **MUST be enabled manually in console**
- Go to: https://console.firebase.google.com/project/perception-with-intent/firestore
- Click "Create database"
- Select "Start in production mode"
- Choose location: `us-central1`
- Click "Enable"

---

## Environment Setup

### 1. Set Project ID

```bash
# Set as environment variable
export GOOGLE_CLOUD_PROJECT=perception-with-intent

# Or via gcloud
gcloud config set project perception-with-intent
```

### 2. Authenticate

```bash
# Application Default Credentials
gcloud auth application-default login

# Set quota project
gcloud auth application-default set-quota-project perception-with-intent
```

---

## Seeding Firestore

### Initial Feeds CSV

Sources are loaded from **`data/initial_feeds.csv`**

This CSV is the source of truth for initial `/sources` documents.

**Format:**
```csv
source_id,name,type,url,category,enabled
techcrunch_ai,TechCrunch AI,rss,https://techcrunch.com/feed/,tech,true
```

### Running the Seed Script

**Method 1: Node.js Script** (Recommended)

```bash
# Install dependencies
npm install

# Run seed script
node scripts/seed-firestore.js
```

**Method 2: Python Script**

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install firebase-admin

# Run seed script
python scripts/load-initial-feeds.py
```

### What Gets Seeded

The seed script creates:

1. **Sources** (`/sources/{sourceId}`)
   - Loaded from `data/initial_feeds.csv`
   - 10 tech/AI news sources

2. **Sample Articles** (`/articles/{articleId}`)
   - 3 realistic sample articles
   - AI-generated summaries
   - Relevance scores

3. **Sample Brief** (`/briefs/{briefId}`)
   - Daily brief for today's date
   - Executive summary + highlights
   - Metrics

4. **Sample Ingestion Run** (`/ingestion_runs/{runId}`)
   - Recent completed run
   - Stats (sources checked, articles ingested, etc.)

### Idempotency

The seed script is **safe to run multiple times**:
- Checks if documents exist before creating
- Skips existing sources
- Won't duplicate data

---

## Verifying the Seed

### Check Firestore Console

https://console.firebase.google.com/project/perception-with-intent/firestore

You should see:
- `/sources` - 10 documents
- `/articles` - 3 documents
- `/briefs` - 1 document
- `/ingestion_runs` - 1 document

### Query from CLI

```bash
# List sources
firebase firestore:get sources --project perception-with-intent

# Count articles
firebase firestore:count articles --project perception-with-intent
```

---

## Running the Dashboard

### Install Dependencies

```bash
cd dashboard
npm install
```

### Environment Configuration

The dashboard uses environment variables for Firebase configuration. While default values are provided for the perception-with-intent project, you can override them with a `.env.local` file.

**Create `.env.local` (optional):**

```bash
cd dashboard
cp .env.example .env.local
```

**Environment Variables:**
- `VITE_FIREBASE_API_KEY` - Firebase API key
- `VITE_FIREBASE_AUTH_DOMAIN` - Firebase auth domain
- `VITE_FIREBASE_PROJECT_ID` - Firebase project ID
- `VITE_FIREBASE_STORAGE_BUCKET` - Firebase storage bucket
- `VITE_FIREBASE_MESSAGING_SENDER_ID` - Firebase messaging sender ID
- `VITE_FIREBASE_APP_ID` - Firebase app ID

**Note:** These values are public and safe for client-side use. The default values in the code are for the perception-with-intent project.

### Start Dev Server

```bash
npm run dev

# Dashboard available at:
# http://localhost:5173
```

### Dashboard Features

Once logged in, you'll see:

1. **Today's Brief** - Most recent daily intelligence summary
2. **Topic Watchlist** - Your monitored topics (requires user-specific data)
3. **Source Health & Coverage** - Status of all news sources
4. **Alerts & Thresholds** - Your configured alerts (requires user-specific data)
5. **System Activity** - Recent ingestion runs and statistics

**Note:** Topic Watchlist and Alerts are user-specific and will be empty until you configure them. Today's Brief, Source Health, and System Activity read from global collections populated by the seed script.

### Build for Production

```bash
npm run build

# Test production build
npm run preview
```

---

## Firebase Authentication

### Enable Email/Password Provider

Go to: https://console.firebase.google.com/project/perception-with-intent/authentication/providers

1. Click "Email/Password"
2. Toggle "Enable" to ON
3. Click "Save"

### Create Test Account

```bash
# Via dashboard at http://localhost:5173/login
# Click "Sign up" and create account
```

---

## Security Rules

### Deploy Rules

```bash
firebase deploy --only firestore:rules --project perception-with-intent
```

### Test Rules

```bash
firebase emulators:start --only firestore

# In another terminal, run tests
npm run test:rules
```

---

## Common Issues

### "Firestore in Datastore Mode" Error

**Problem:** Firestore Native Mode not enabled

**Solution:**
1. Go to https://console.firebase.google.com/project/perception-with-intent/firestore
2. Enable Native Mode (see "GCP Setup" section above)

### "Permission Denied" Errors

**Problem:** Not authenticated or missing quota project

**Solution:**
```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project perception-with-intent
```

### Seed Script Fails

**Problem:** Missing dependencies

**Solution:**
```bash
# For Node.js script
npm install

# For Python script
pip install firebase-admin
```

---

## Project Structure

```
perception-with-intent/
├── data/
│   └── initial_feeds.csv          # Source of truth for feeds
├── scripts/
│   ├── seed-firestore.js          # Node.js seed script
│   └── load-initial-feeds.py      # Python seed script
├── dashboard/
│   ├── src/                       # React app source
│   └── dist/                      # Built files
├── app/
│   └── perception_agent/          # Agent Engine app
│       ├── agents/                # 8 agent YAML configs
│       ├── tools/                 # Agent tools (Python)
│       └── prompts/               # Agent prompts
├── firestore.rules                # Security rules
└── firebase.json                  # Firebase config
```

---

## Next Steps

After seeding Firestore:

1. **Test Dashboard**
   - Login with test account
   - View seeded data
   - Verify all sections render

2. **Deploy Agents** (Phase 3+)
   - Configure Agent Engine
   - Deploy individual agents
   - Test A2A communication

3. **Deploy MCP Tools** (Phase 4+)
   - Build Cloud Run services
   - Implement fetch_rss_feed
   - Connect to agents

---

## Resources

- **Project Console:** https://console.firebase.google.com/project/perception-with-intent
- **Firestore Console:** https://console.firebase.google.com/project/perception-with-intent/firestore
- **Firebase Hosting:** https://perception-with-intent.web.app
- **GitHub Repo:** https://github.com/jeremylongshore/perception-with-intent

---

**Last Updated:** 2025-11-14
**Phase:** 1 (Firestore Foundation)
**Status:** Ready for seeding

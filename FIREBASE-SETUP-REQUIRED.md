# Firebase Hosting Setup Required

## Current Status

✅ Dashboard built successfully (`dashboard/dist/`)
✅ Firebase configuration files created (`firebase.json`, `.firebaserc`)
✅ Firestore rules and indexes configured
✅ GitHub Action for auto-deployment created
❌ Firebase Hosting not yet enabled in Firebase Console

## The Issue

When you visit https://perception-with-intent.web.app you see "Site Not Found" because:

1. **Firebase Hosting needs to be enabled through the Firebase Console**
2. The hosting site hasn't been created yet
3. No deployment has been made

## How to Fix (5 minutes)

### Step 1: Enable Firebase Hosting

1. Go to **[Firebase Console](https://console.firebase.google.com/)**
2. Select project: **perception-with-intent**
3. Click **"Hosting"** in the left sidebar
4. Click **"Get Started"** button
5. Follow the wizard (just click Next/Continue - we already have config files)

### Step 2: Deploy Dashboard

Once Firebase Hosting is enabled, deploy using either method:

**Option A: Deploy from local machine**
```bash
cd /home/jeremy/000-projects/perception
firebase deploy --only hosting --project perception-with-intent
```

**Option B: Deploy via GitHub Actions**
```bash
# Push any change to dashboard/ folder
git add .
git commit -m "chore: trigger dashboard deployment"
git push origin main
```

### Step 3: Verify

Visit https://perception-with-intent.web.app - you should see the dashboard!

## What's Already Done

### Firebase Configuration (`firebase.json`)
```json
{
  "hosting": {
    "public": "dashboard/dist",
    "rewrites": [{ "source": "**", "destination": "/index.html" }]
  },
  "firestore": {
    "rules": "firestore.rules",
    "indexes": "firestore.indexes.json"
  }
}
```

### Firestore Security Rules (`firestore.rules`)
- Read-only access to articles, topics, summaries
- Write access restricted to backend agents only

### Dashboard Build
```bash
cd dashboard
npm install  # ✅ Done
npm run build  # ✅ Done - output in dist/
```

### GitHub Action (`.github/workflows/deploy-firebase-dashboard.yml`)
Automatically deploys dashboard on every push to `main` that touches `dashboard/**`

## Files Created

1. **`firebase.json`** - Firebase project configuration
2. **`.firebaserc`** - Project aliases
3. **`firestore.rules`** - Database security rules
4. **`firestore.indexes.json`** - Database indexes
5. **`dashboard/tsconfig.node.json`** - TypeScript config for Vite
6. **`.github/workflows/deploy-firebase-dashboard.yml`** - Auto-deployment

## Why This Couldn't Be Done Automatically

Firebase Hosting initialization requires:
- Web UI interaction (Firebase Console)
- Or service account with `firebase.management.serviceAccounts.create` permission
- Cannot be done via CLI without the hosting site existing first

## Next Steps

1. ✅ Enable Firebase Hosting in Console (Step 1 above)
2. ✅ Deploy dashboard (Step 2 above)
3. ✅ Verify site is live (Step 3 above)
4. 🔄 Then agents can start writing data to Firestore
5. 🔄 Dashboard will show real-time intelligence

---

**TL;DR:** Go to [Firebase Console → perception-with-intent → Hosting → Get Started](https://console.firebase.google.com/project/perception-with-intent/hosting), then run `firebase deploy --only hosting --project perception-with-intent`

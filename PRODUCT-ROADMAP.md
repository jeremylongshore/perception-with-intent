# Perception Product Roadmap

## Phase 1: Public Showcase (Current)
**Purpose:** Demonstrate platform capabilities, promote company

### Features:
- ✅ Public dashboard (no authentication)
- ✅ Real-time news intelligence display
- ✅ Example topics showing platform power
- ✅ Professional HustleStats-inspired design
- 🔄 Live demo of AI analysis
- 🔄 Company branding and portfolio showcase

### Use Cases:
- Marketing website / landing page
- Portfolio demonstration
- Lead generation
- Proof of concept for investors/clients

---

## Phase 2: Client SaaS Platform (Future)
**Purpose:** Multi-tenant news intelligence for paying clients

### Features:
- 🔜 Firebase Authentication (email/password, Google SSO)
- 🔜 Multi-tenant architecture (client isolation)
- 🔜 Custom topics per client account
- 🔜 Private RSS feed configuration
- 🔜 Usage analytics and reporting
- 🔜 Subscription tiers (basic/pro/enterprise)
- 🔜 API access for enterprise clients
- 🔜 White-label options

### Technical Requirements:
- Firestore security rules (row-level security)
- User management dashboard (admin)
- Stripe/billing integration
- Email notifications
- Data export features
- SLA monitoring

---

## Dashboard Evolution

### Current (Phase 1):
```
Perception Dashboard (Public)
├── Homepage: Live intelligence feed
├── Topics: Example monitoring categories
├── Daily Briefs: Strategic summaries
└── About: Company info, contact
```

### Future (Phase 2):
```
Perception SaaS (Authenticated)
├── Login/Signup
├── Dashboard: User's custom feed
├── My Topics: User-configured keywords
├── Daily Briefs: Personalized summaries
├── Settings: Account, billing, API keys
└── Admin Panel: (for us) User management
```

---

## Immediate Focus

**Phase 1 Goals:**
1. ✅ Deploy public showcase dashboard
2. 🔄 Add company branding/about section
3. 🔄 Configure example topics (AI, tech, business)
4. 🔄 Set up WIF CICD for automated deployments
5. 🔄 Custom domain (e.g., perception.yourcompany.com)
6. 🔄 Analytics (Google Analytics, Plausible)

**Marketing Copy:**
- "Track what matters. See what's coming."
- "AI-powered news intelligence for executives"
- "Never miss strategic insights from the noise"

---

## Technical Architecture Notes

### Phase 1 (Simple):
- Single Firestore database (public read access)
- No user accounts
- No billing
- Showcase-quality data

### Phase 2 (Multi-tenant):
- User collection with Firebase Auth UIDs
- Topics scoped to `user_id`
- Articles scoped to `user_id`
- Firestore security rules enforce isolation
- Subscription tracking in Firestore
- Stripe webhooks for billing events

---

## Timeline Estimate

**Phase 1 MVP:** 1 week
- Infrastructure: ✅ Done
- Dashboard: ✅ Done
- Agents: 3-4 days
- WIF CICD: 1 day
- Polish: 1 day

**Phase 2 (SaaS):** 3-4 weeks after Phase 1 launch
- Authentication: 3 days
- Multi-tenant refactor: 5 days
- Billing integration: 5 days
- Admin panel: 3 days
- Testing: 4 days

---

**Status:** Phase 1 in progress - Public showcase dashboard
**Next:** Complete agent implementation, then WIF CICD deployment

# IAM Multi-Agent Architecture Brainstorming

**Created**: 2025-11-09
**Status**: Brainstorming / Pre-Implementation
**Purpose**: Explore different hierarchical architectures for real-world use cases

---

## Research: Caldwell Wenzel & Asthana, PC

### Firm Profile
- **Location**: Mobile, Pensacola, Birmingham, Foley (Alabama/Florida Gulf Coast)
- **Practice Focus**: Personal Injury, Wrongful Death, Estate/Trust Litigation, Auto Accidents
- **Years in Practice**: 20+ years
- **Structure**: Regional multi-office firm

### Key Partners/Attorneys
- **Deepti Asthana** - Managing Partner (joined 2013, partner 2019)
- **C. Randall Caldwell, Jr.** - Founding Partner
- **Drew Wenzel** - Partner (Mobile Bay Magazine Top 40 under 40)
- **Ruben V. Nichols, III** - Attorney
- **Andrew Duncan** - Attorney

### How They Handle Referrals
Per their website (cwalawfirm.com/referring-attorneys/):
- **Referral In**: Accept cases from other attorneys who don't handle personal injury
- **Referral Out**: Send cases outside their niche (e.g., criminal, family law, business law)
- **Referral Network**: Maintain relationships with specialized attorneys across practice areas
- **Fee Sharing**: Standard referral fee arrangements (typically 25-33%)

---

## Legal Referral System Research

### How Attorney Referrals Work

**Types of Referrals**:
1. **Bar Association Referral Services** - Certified networks maintained by state/local bars
2. **Attorney-to-Attorney Referrals** - Direct relationships between complementary practices
3. **Client Referrals** - Past clients recommending to new clients
4. **Professional Referral Networks** - Groups like BNI, legal-specific networks

**Referral Process**:
1. **Intake**: Potential client contacts firm
2. **Screening**: Determine if case fits firm's practice area
3. **If No Match**: Search referral network for appropriate specialist
4. **Connect**: Introduce client to referred attorney
5. **Fee Arrangement**: Referral fee agreement (if applicable)
6. **Follow-up**: Track case outcome for quality assurance

**Key Decision Factors**:
- Practice area match
- Case value/complexity
- Geographic jurisdiction
- Attorney specialization level
- Referral network relationship strength

---

## Architecture Model 1: Multi-Partner Shared IAM1 (Caldwell Wenzel Example)

### Concept
Multiple partners (5+ attorneys) share ONE central IAM1 that orchestrates all firm operations.

```
┌──────────────────────────────────────────────────────────────┐
│                  PARTNER ACCESS LAYER                         │
│  👤 Deepti Asthana  👤 Drew Wenzel  👤 Randall Caldwell      │
│  👤 Ruben Nichols   👤 Andrew Duncan                          │
│           (All access same IAM1 via Slack/Web UI)             │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│        IAM1: Firm Operations Manager (Shared Resource)       │
│   - Client Intake & Qualification                            │
│   - Case Assignment to Partners                              │
│   - Referral Network Routing                                 │
│   - Multi-Office Coordination (Mobile, Pensacola, etc.)      │
│   - Firm-wide Knowledge Base Access                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌─────▼─────┐     ┌────▼─────┐
   │  IAM2   │      │   IAM2    │     │   IAM2   │
   │Personal │      │  Estate   │     │ Referral │
   │ Injury  │      │ Litigation│     │ Network  │
   │Practice │      │  Practice │     │ Manager  │
   └────┬────┘      └─────┬─────┘     └────┬─────┘
        │                 │                 │
  ┌─────┼────┐      ┌─────┼────┐     ┌─────┼────┐
  │     │    │      │     │    │     │     │    │
┌─▼─┐ ┌▼─┐ ┌▼─┐  ┌─▼─┐ ┌▼─┐ ┌▼─┐  ┌─▼─┐ ┌▼─┐ ┌▼─┐
│IA3│ │IA3│ │IA3│ │IA3│ │IA3│ │IA3│ │IA3│ │IA3│ │IA3│
│Mob│ │Pen│ │Bir│ │Mob│ │Pen│ │Bir│ │Crim│ │Fam│ │Bus│
│ile│ │sa │ │min│ │ile│ │sa │ │min│ │inal│ │ily│ │ines│
└─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘
  │     │     │     │     │     │     │     │     │
(4 IAM4 teams per office)  (4 IAM4 teams)  (External referrals)
```

### Key Features

**Shared Access**:
- All 5 partners query same IAM1 via Slack/web interface
- IAM1 maintains context per partner (separate conversation threads)
- Partner-specific permissions (e.g., only Managing Partner sees firm financials)

**Case Routing**:
- IAM1 determines: "Is this our practice area?"
  - **YES** → Route to appropriate IAM2 practice leader
  - **NO** → Route to IAM2 Referral Network Manager

**Referral Network Manager (IAM2)**:
- Maintains directory of 9 IAM3 referral partners:
  - IAM3-Criminal-Defense (for criminal cases)
  - IAM3-Family-Law (for divorce, custody)
  - IAM3-Business-Law (for contracts, corp law)
  - IAM3-Immigration (for visa, citizenship)
  - IAM3-Employment (for workplace disputes)
  - IAM3-Tax-Law (for IRS issues)
  - IAM3-Bankruptcy (for debt relief)
  - IAM3-IP-Law (for patents, trademarks)
  - IAM3-Real-Estate (for property transactions)

Each referral IAM3 has 4 IAM4 teams:
1. **Qualification Team** - Verify case fits specialty
2. **Attorney Matcher** - Match to best attorney in network
3. **Introduction Coordinator** - Warm handoff to client
4. **Follow-up Tracker** - Monitor referral outcomes

---

## Architecture Model 2: Partner-Specific IAM1s (Enterprise Scale)

### Concept
Each senior partner has their OWN IAM1 for their practice group.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│👤 Partner A │    │👤 Partner B │    │👤 Partner C │
│  IAM1-A     │    │  IAM1-B     │    │  IAM1-C     │
│ Personal    │    │  Estate     │    │ Auto Injury │
│  Injury     │    │ Litigation  │    │   Cases     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
  (3 IAM2s)          (3 IAM2s)          (3 IAM2s)
       │                  │                  │
  (9 IAM3s)          (9 IAM3s)          (9 IAM3s)
       │                  │                  │
 (36 IAM4s)         (36 IAM4s)         (36 IAM4s)

       └──────────────────┼──────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Firm-Wide IAM0       │
              │  (Managing Partner    │
              │   Strategic Overview) │
              └───────────────────────┘
```

**When to Use**:
- Large firms (50+ attorneys)
- Independent practice groups
- Separate P&Ls per partner
- High autonomy model

---

## Architecture Model 3: Regional Auto Dealer Group (Alternative Industry)

### Example: "Gulf Coast Auto Group"
**Brands**: Ford, Chevrolet, Toyota, Honda, Nissan
**Locations**: Mobile, Pensacola, Panama City

```
┌──────────────────────────────────────────────────────────┐
│     IAM1: Gulf Coast Auto Group - DSM (Dealer Sales      │
│            Manager / General Manager Level)               │
│  - Multi-brand inventory management                       │
│  - Cross-dealership coordination                          │
│  - Regional marketing campaigns                           │
│  - Customer referrals between brands                      │
└─────────────────────────┬────────────────────────────────┘
                          │
      ┌───────────────────┼───────────────────┐
      │                   │                   │
┌─────▼─────┐      ┌──────▼──────┐     ┌──────▼──────┐
│   IAM2    │      │    IAM2     │     │    IAM2     │
│  New Car  │      │   Used Car  │     │   Service   │
│   Sales   │      │    Sales    │     │  & Parts    │
└─────┬─────┘      └──────┬──────┘     └──────┬──────┘
      │                   │                   │
 ┌────┼────┐         ┌────┼────┐        ┌────┼────┐
 │    │    │         │    │    │        │    │    │
┌▼┐  ┌▼┐  ┌▼┐       ┌▼┐  ┌▼┐  ┌▼┐      ┌▼┐  ┌▼┐  ┌▼┐
│F │  │C │  │T │     │M │  │P │  │P │    │M │  │P │  │P │
│o │  │h │  │o │     │o │  │e │  │a │    │o │  │e │  │a │
│r │  │e │  │y │     │b │  │n │  │n │    │b │  │n │  │n │
│d │  │v │  │o │     │i │  │s │  │a │    │i │  │s │  │a │
│  │  │y │  │t │     │l │  │a │  │m │    │l │  │a │  │m │
│  │  │  │  │a │     │e │  │c │  │a │    │e │  │c │  │a │
│IA3│ │IA3│ │IA3│   │IA3│ │IA3│ │IA3│  │IA3│ │IA3│ │IA3│
└─┬┘  └─┬┘  └─┬┘    └─┬┘  └─┬┘  └─┬┘   └─┬┘  └─┬┘  └─┬┘
  │     │     │       │     │     │      │     │     │
(4 IAM4 teams)     (4 IAM4 teams)     (4 IAM4 teams)
```

### IAM4 Teams for Auto Dealer

**New Car Sales IAM4s**:
1. **Lead Qualification** - Score incoming leads, prioritize hot prospects
2. **Inventory Matcher** - Match customer needs to available inventory
3. **Finance Pre-Approval** - Credit check, loan options, payment calculator
4. **Trade-In Appraiser** - Vehicle valuation, market comparisons

**Used Car Sales IAM4s**:
1. **Vehicle History Reporter** - Carfax, AutoCheck, service records
2. **Pricing Optimizer** - Market analysis, competitive pricing
3. **Cross-Brand Matcher** - "Customer wants Honda but we only have Toyota? Find equivalent"
4. **Warranty Package Builder** - Extended warranty options, protection plans

**Service & Parts IAM4s**:
1. **Appointment Scheduler** - Service bay optimization, technician allocation
2. **Diagnostic Assistant** - Symptom analysis, recommended services
3. **Parts Sourcing** - Inventory check, cross-location transfer, supplier orders
4. **Recall & Maintenance Reminder** - Proactive customer outreach

### Auto Dealer Workflows

**Example 1: Cross-Brand Referral**
- Customer: "I want a reliable SUV under $30K"
- IAM1 analyzes: Budget-conscious, family vehicle
- IAM2-NewCar routes to:
  - IAM3-Toyota (RAV4)
  - IAM3-Honda (CR-V)
  - IAM3-Chevy (Equinox)
- Each IAM3 returns: Inventory, pricing, incentives
- IAM1 synthesizes: "We have 3 options across our brands..."

**Example 2: Service Coordination**
- Customer: "My Ford F-150 needs transmission work"
- IAM1 routes to IAM2-Service
- IAM2-Service routes to IAM3-Ford-Mobile
- IAM3 delegates to IAM4s:
  - Diagnostic Assistant: "Transmission flush or rebuild?"
  - Parts Sourcing: Check part availability
  - Appointment Scheduler: First available bay
- IAM1 response: "Diagnostic on Tuesday, parts in stock, estimated $1,200"

---

## Referral Routing Architecture Deep Dive

### Intelligent Case Qualification System

```
User Query: "I need a lawyer for my divorce"
        │
        ▼
┌─────────────────────────────────────────┐
│ IAM1: Intake & Qualification            │
│ - Analyzes: "Divorce = Family Law"      │
│ - Checks: Firm Practice Areas           │
│ - Decision: NOT our practice (we do PI) │
└────────────┬────────────────────────────┘
             │
             ▼ (Route to Referral Manager)
┌─────────────────────────────────────────┐
│ IAM2: Referral Network Manager          │
│ - Identifies: Family Law needed         │
│ - Checks: Geographic location           │
│ - Selects: IAM3-Family-Law-Mobile       │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ IAM3: Family Law Referral Partner       │
│ - Attorney: Smith & Associates          │
│ - Specialty: Divorce, Custody           │
│ - Location: Mobile, AL                  │
│ - Rating: 4.8/5 (50 referrals)          │
└────────────┬────────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
┌───▼──┐  ┌──▼──┐  ┌──▼──┐
│ IAM4 │  │ IAM4 │  │ IAM4 │
│Qualify│ │Match │ │Intro│
└──────┘  └─────┘  └─────┘

IAM4-Qualification: "Divorce case, married 5 years, no kids, $200K assets"
IAM4-Match: "Best fit: Sarah Johnson, specializes in no-fault divorce"
IAM4-Introduction: "Here's Sarah's contact, I've sent her your case summary"
```

### Referral Network Database (IAM3 Level)

Each IAM3 referral partner stores:
```json
{
  "attorney_name": "Sarah Johnson, Esq.",
  "firm": "Johnson Family Law, PC",
  "practice_areas": ["Divorce", "Child Custody", "Adoption"],
  "location": "Mobile, AL",
  "years_experience": 15,
  "referral_history": {
    "total_referrals": 50,
    "successful_outcomes": 42,
    "client_satisfaction": 4.8,
    "avg_time_to_resolution": "6 months"
  },
  "referral_fee": "25% of attorney fees",
  "contact": {
    "phone": "251-555-0123",
    "email": "sarah@johnsonfamilylaw.com",
    "website": "https://johnsonfamilylaw.com"
  },
  "specializations": [
    "High-net-worth divorce",
    "Military divorce",
    "Collaborative divorce"
  ],
  "availability": "Accepting new clients",
  "communication_preference": "Email intro with case summary"
}
```

---

## Comparison: Architecture Models

### Model 1: Shared IAM1 (Caldwell Wenzel)

**Pros**:
- ✅ Single knowledge base for entire firm
- ✅ Unified client experience
- ✅ Cost-effective (one IAM1 deployment)
- ✅ Centralized case management
- ✅ Easy cross-office coordination

**Cons**:
- ❌ Single point of failure
- ❌ Scaling limits (all partners share resources)
- ❌ Less autonomy per partner
- ❌ Complex access control

**Best For**:
- Small to mid-size firms (5-50 attorneys)
- Single practice area focus
- Strong central management
- Cost-conscious deployments

**Pricing**:
- 1x IAM1: $500/month
- 3x IAM2 (practices): $600/month ($200 each)
- 9x IAM3 (offices/referrals): $1,800/month ($200 each)
- 36x IAM4 (teams): **Included in IAM3 pricing**
- **Total**: ~$2,900/month for 49-agent system

---

### Model 2: Partner-Specific IAM1s

**Pros**:
- ✅ Complete autonomy per practice group
- ✅ Horizontal scaling (add partners independently)
- ✅ Fault isolation (one partner's IAM1 down ≠ firm down)
- ✅ Custom workflows per partner

**Cons**:
- ❌ Higher cost (multiple IAM1 deployments)
- ❌ Knowledge silos between partners
- ❌ Complex inter-partner coordination
- ❌ Duplicate infrastructure

**Best For**:
- Large firms (100+ attorneys)
- Independent practice groups with separate P&Ls
- High-growth firms adding new partners frequently
- Distributed/remote teams

**Pricing**:
- 3x IAM1 (partners): $1,500/month ($500 each)
- 9x IAM2: $1,800/month
- 27x IAM3: $5,400/month
- 108x IAM4: **Included**
- 1x IAM0 (strategic): $500/month
- **Total**: ~$9,200/month for 148-agent system

---

### Model 3: Auto Dealer Group

**Pros**:
- ✅ Multi-brand inventory visibility
- ✅ Customer referrals between brands
- ✅ Unified customer experience across brands
- ✅ Cross-location coordination

**Cons**:
- ❌ Complexity managing multiple inventories
- ❌ Brand-specific rules and incentives
- ❌ Manufacturer compliance requirements

**Best For**:
- Regional auto dealer groups
- Multi-brand retail operations
- Service-heavy businesses
- Customer lifecycle management

**Pricing**: Same as Model 1 (~$2,900/month)

---

## Decision Matrix: Which Architecture?

| Factor | Shared IAM1 | Partner IAM1s | Auto Dealer |
|--------|-------------|---------------|-------------|
| **Team Size** | 5-50 people | 100+ people | 5-50 people |
| **Practice Areas** | 1-3 areas | 5+ areas | 3-5 brands |
| **Autonomy Needs** | Low-Medium | High | Medium |
| **Budget** | $3K/month | $9K/month | $3K/month |
| **Complexity** | Low | High | Medium |
| **Scalability** | Medium | High | Medium |
| **Fault Tolerance** | Low | High | Medium |

---

## Key Questions for Implementation

### For Caldwell Wenzel Pitch:

1. **Access Pattern**:
   - Do all 5 partners need 24/7 access?
   - Or is there a "managing partner" who primarily uses it?

2. **Practice Area Split**:
   - Should Personal Injury and Estate Litigation be separate IAM2s?
   - Or one unified "Civil Litigation" IAM2?

3. **Office Coordination**:
   - Do Mobile/Pensacola/Birmingham offices work independently?
   - Or frequently collaborate on cases?

4. **Referral Network**:
   - How many referral partners do they currently have?
   - Do they track referral outcomes?

5. **Integration Needs**:
   - What case management software? (Clio, MyCase, PracticePanther?)
   - CRM system? (Salesforce, HubSpot?)
   - Document management? (NetDocuments, iManage?)

---

## Recommended Architecture: Caldwell Wenzel & Asthana

Based on research, I recommend **Model 1: Shared IAM1** with these specifics:

```
Caldwell Wenzel & Asthana, PC
├── IAM1: Firm Operations Manager
│   ├── IAM2: Personal Injury Practice
│   │   ├── IAM3: Mobile Office (Auto accidents, slip-fall)
│   │   ├── IAM3: Pensacola Office
│   │   └── IAM3: Birmingham Office
│   ├── IAM2: Estate Litigation Practice
│   │   ├── IAM3: Mobile Office (Probate, will contests)
│   │   ├── IAM3: Pensacola Office
│   │   └── IAM3: Birmingham Office (NOTE: Birmingham = Foley?)
│   └── IAM2: Referral Network Manager
│       ├── IAM3: Criminal Defense Referrals
│       ├── IAM3: Family Law Referrals
│       ├── IAM3: Business Law Referrals
│       └── IAM3: Immigration Law Referrals
```

**Total Agents**: 1 IAM1 + 3 IAM2 + 10 IAM3 + 40 IAM4 = **54 agents**

**Monthly Cost**: ~$3,200/month

**ROI Calculation**:
- Automates: Case intake, qualification, routing, referral management
- Time Saved: ~20 hours/week (partner + staff time)
- Cost Savings: ~$2,000/week in labor ($8K/month)
- **Payback Period**: < 2 weeks

---

## Next Steps (User Decision Required)

Before implementing diagrams, please decide:

1. **Which architecture model?**
   - Shared IAM1 (Model 1)
   - Partner-specific IAM1s (Model 2)
   - Both (show comparison)

2. **Industry focus?**
   - Law firm (Caldwell Wenzel)
   - Auto dealer
   - Both as examples

3. **Diagram detail level?**
   - Show all 36-40 IAM4 teams
   - Or represent symbolically with "4x IAM4 per office"

4. **LLM model differentiation?**
   - IAM1: Gemini 2.0 Flash Thinking
   - IAM2: Gemini 2.0 Flash
   - IAM3: Gemini 1.5 Flash
   - IAM4: Gemini 1.5 Flash 8B

5. **Visual style?**
   - Professional/corporate
   - Tech/modern gradient
   - Industry-specific branding

Let me know your preferences and I'll create the Mermaid diagrams!

---

**Status**: Awaiting user direction before implementation
**Recommendation**: Start with Shared IAM1 model for Caldwell Wenzel pitch

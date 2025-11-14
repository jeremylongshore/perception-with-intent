# Agent Deployment Architecture on Vertex AI Engine

## The Reality: One Container, Multiple Agents

On Vertex AI Agent Engine with ADK, here's how it actually works:

### Architecture Pattern

```
Vertex AI Agent Engine (Single Deployment)
├── agent_engine_app.py (Entry Point)
├── Agent 0: Root Orchestrator (Main)
│   ├── Controls sub-agents via A2A Protocol
│   └── Has references to all sub-agents
│
└── Sub-Agents (Referenced by Agent 0)
    ├── Agent 1: Source Ingestion
    ├── Agent 2: Topic Manager
    ├── Agent 3: Relevance Filter
    ├── Agent 4: Article Analyst
    ├── Agent 5: Daily Synthesizer
    ├── Agent 6: Validator
    └── Agent 7: Delivery
```

**Key Point:** All agents deploy as ONE unit to Agent Engine, but they operate independently via A2A protocol.

## Deployment Models

### Option 1: Monolithic Deployment (Simpler, What We'll Start With)

All agents in one Agent Engine deployment:

```python
# agent_engine_app.py
from google.adk.apps import App
from google.adk.agents import Agent

app = App()

# Load root orchestrator with all sub-agents
root_agent = Agent.from_config_file("agents/agent_0_orchestrator.yaml")
app.register_agent(root_agent)

# Root agent references all sub-agents internally
```

**Pros:**
- Simpler deployment
- Lower latency between agents
- Shared memory/session
- Single telemetry stream

**Cons:**
- All agents scale together
- Updates affect entire system

### Option 2: Distributed Deployment (Production Goal)

Each agent gets its own Agent Engine deployment:

```
Agent Engine Instance 1: Root Orchestrator
    ↓ (A2A Protocol)
Agent Engine Instance 2: Source Ingestion
Agent Engine Instance 3: Topic Manager
Agent Engine Instance 4: Article Analyst
... etc
```

**Pros:**
- Independent scaling
- Isolated failures
- Granular updates
- Better resource allocation

**Cons:**
- More complex
- Network latency between agents
- Higher cost

## File Structure for Specialized Agents

Yes, each agent gets its own specialized files:

```
app/
└── perception_agent/
    ├── agents/
    │   ├── agent_0_orchestrator.yaml
    │   ├── agent_1_source_ingestion.yaml
    │   ├── agent_2_topic_manager.yaml
    │   ├── agent_3_relevance_filter.yaml
    │   ├── agent_4_article_analyst.yaml
    │   ├── agent_5_daily_synthesizer.yaml
    │   ├── agent_6_validator.yaml
    │   └── agent_7_delivery.yaml
    │
    ├── tools/
    │   ├── agent_0_tools.py  # Orchestration tools
    │   ├── agent_1_tools.py  # RSS fetching tools
    │   ├── agent_2_tools.py  # Topic management
    │   ├── agent_3_tools.py  # Scoring algorithms
    │   ├── agent_4_tools.py  # LLM analysis
    │   ├── agent_5_tools.py  # Synthesis tools
    │   ├── agent_6_tools.py  # Validation logic
    │   └── agent_7_tools.py  # Delivery methods
    │
    └── prompts/
        ├── agent_0_prompts.py
        ├── agent_1_prompts.py
        └── ... etc
```

## Individual Agent Example

### Agent 0: Root Orchestrator

**File:** `agents/agent_0_orchestrator.yaml`
```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/google/adk-python/refs/heads/main/src/google/adk/agents/config_schemas/AgentConfig.json
name: perception_orchestrator
agent_class: Agent
model: gemini-2.0-flash
description: Root orchestrator for news intelligence workflow
instruction: |
  You are the Editor-in-Chief orchestrating daily news intelligence.

  Workflow:
  1. Dispatch source collection (parallel)
  2. Filter by relevance
  3. Analyze top articles
  4. Synthesize daily brief
  5. Deliver to stakeholders

tools:
  - name: agent_0_tools

sub_agents:
  - config_path: ./agents/agent_1_source_ingestion.yaml
  - config_path: ./agents/agent_2_topic_manager.yaml
  - config_path: ./agents/agent_3_relevance_filter.yaml
  - config_path: ./agents/agent_4_article_analyst.yaml
  - config_path: ./agents/agent_5_daily_synthesizer.yaml
  - config_path: ./agents/agent_6_validator.yaml
  - config_path: ./agents/agent_7_delivery.yaml
```

### Agent 4: Article Analyst (Specialized)

**File:** `agents/agent_4_article_analyst.yaml`
```yaml
name: article_analyst
agent_class: Agent
model: gemini-2.0-flash
description: Analyze articles for summaries and insights
instruction: |
  You are an expert news analyst. Your job:

  1. Generate 3-5 sentence summaries
  2. Extract 4 relevant tags
  3. Identify strategic implications
  4. Score importance (1-10)

  Output strict JSON format.

tools:
  - name: agent_4_tools

# No sub-agents (leaf agent)
```

**File:** `tools/agent_4_tools.py`
```python
from typing import Dict, List, Any
import httpx

async def analyze_with_llm(article_text: str) -> Dict[str, Any]:
    """Call LLMToolsMCP for analysis."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://llm-tools-mcp:8080/mcp/tools/summarize",
            json={"text": article_text, "options": {"max_sentences": 5}}
        )
        return response.json()

async def generate_tags(article_text: str, topics: List[str]) -> List[str]:
    """Generate relevant tags via LLMToolsMCP."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://llm-tools-mcp:8080/mcp/tools/generate_tags",
            json={"text": article_text, "topics": topics, "max_tags": 4}
        )
        return response.json()["tags"]

async def score_importance(article: Dict[str, Any]) -> float:
    """Score article importance (1-10)."""
    # Custom scoring logic
    score = 5.0

    # Boost for keywords in title
    if any(kw in article["title"].lower() for kw in ["breaking", "exclusive", "urgent"]):
        score += 2.0

    # Boost for multiple topic matches
    if len(article.get("matched_topics", [])) > 2:
        score += 1.5

    return min(score, 10.0)
```

## Observability & Telemetry

### Built-in ADK Telemetry

Each agent automatically gets:

```python
# In agent_engine_app.py or agent config
from google.adk import telemetry

# Enable Cloud Trace
telemetry.enable_cloud_trace(
    project_id="perception-with-intent",
    service_name="perception-agents",
    service_version="1.0.0"
)

# Enable Cloud Monitoring
telemetry.enable_cloud_monitoring(
    project_id="perception-with-intent",
    metrics_prefix="perception"
)

# Enable structured logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        telemetry.CloudLoggingHandler()
    ]
)
```

### Per-Agent Telemetry

Each agent gets tagged telemetry:

```python
# In each agent's tools file
import opentelemetry.trace as trace
from opentelemetry import metrics

tracer = trace.get_tracer("perception.agent_4.article_analyst")
meter = metrics.get_meter("perception.agent_4.article_analyst")

article_counter = meter.create_counter(
    "articles_analyzed",
    description="Number of articles analyzed",
    unit="1"
)

async def analyze_with_llm(article_text: str) -> Dict[str, Any]:
    with tracer.start_as_current_span("analyze_article") as span:
        span.set_attribute("agent.name", "article_analyst")
        span.set_attribute("agent.id", "agent_4")
        span.set_attribute("article.length", len(article_text))

        # Do analysis
        result = await _call_llm_mcp(article_text)

        # Record metrics
        article_counter.add(1, {"agent": "article_analyst"})

        return result
```

### Cloud Monitoring Dashboard

You'll see in Cloud Monitoring:

```
perception-agents/
├── agent_0_orchestrator/
│   ├── requests_per_minute: 60
│   ├── latency_p95: 2.3s
│   └── error_rate: 0.1%
├── agent_1_source_ingestion/
│   ├── feeds_fetched: 15
│   ├── articles_collected: 847
│   └── fetch_latency: 1.2s
├── agent_4_article_analyst/
│   ├── articles_analyzed: 150
│   ├── summaries_generated: 150
│   ├── llm_tokens_used: 45,000
│   └── analysis_latency: 0.8s
```

## Container Deployment Details

### For Monolithic (Starting Point)

One container with all agents:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install ADK and dependencies
COPY requirements.txt .
RUN pip install google-adk==1.17.0 -r requirements.txt

# Copy all agent code
COPY app/ ./app/

# Entry point that loads all agents
COPY agent_engine_app.py .

# Run the Agent Engine app
CMD ["python", "agent_engine_app.py"]
```

Deploy command:
```bash
adk deploy agent_engine \
  --project=perception-with-intent \
  --region=us-central1 \
  --staging_bucket=gs://perception-staging \
  --display_name="Perception Intelligence System" \
  agent_engine_app.py \
  --trace_to_cloud \
  --cpu=4 \
  --memory=8Gi \
  --min_instances=1 \
  --max_instances=10
```

### For Distributed (Future)

Each agent gets its own deployment:

```bash
# Deploy Agent 0 (Orchestrator)
adk deploy agent_engine \
  --project=perception-with-intent \
  --region=us-central1 \
  --display_name="Perception Orchestrator" \
  app/deployments/orchestrator/agent_engine_app.py \
  --cpu=2 --memory=4Gi

# Deploy Agent 4 (Article Analyst) separately
adk deploy agent_engine \
  --project=perception-with-intent \
  --region=us-central1 \
  --display_name="Article Analyst" \
  app/deployments/article_analyst/agent_engine_app.py \
  --cpu=1 --memory=2Gi
```

## A2A Communication Between Agents

Agents talk via A2A protocol:

```python
# Agent 0 calling Agent 4
async def analyze_articles(articles: List[Dict]):
    """Orchestrator calling Article Analyst agent."""

    # A2A call to Article Analyst
    response = await a2a_client.send_task(
        agent_url="https://agent-4-article-analyst.agent-engine.googleapis.com",
        task={
            "action": "analyze_batch",
            "articles": articles,
            "options": {
                "summary_length": 5,
                "generate_tags": True
            }
        }
    )

    # Track telemetry
    with tracer.start_as_current_span("a2a_call") as span:
        span.set_attribute("source_agent", "orchestrator")
        span.set_attribute("target_agent", "article_analyst")
        span.set_attribute("articles_count", len(articles))

    return response
```

## Why This Architecture?

1. **Start Simple** - Monolithic deployment to get running
2. **Specialize Agents** - Each has its own prompt, tools, config
3. **Observable** - Full telemetry per agent
4. **Scalable** - Can split into distributed later
5. **Clean Separation** - Agents → MCPs (tools) → Data

## Next Steps

1. Create all 8 agent YAML files
2. Implement specialized tool files
3. Set up telemetry
4. Deploy monolithic first
5. Monitor and optimize
6. Split to distributed if needed

The key is: **Agents are smart (they think), MCPs are dumb (they do), Firebase is for humans.**

Ready to build the specialized agents?
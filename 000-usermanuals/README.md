# User Manuals & Examples Directory

**Purpose:** Template and example user manuals for agent systems

**Created:** 2025-11-11
**Status:** Active collection

---

## Contents

### 1. Agent-to-Agent (A2A) Protocol

#### `tutorial_a2a_on_agent_engine.ipynb`
**Source:** Google Cloud Platform generative-ai repository
**Size:** 59KB
**Type:** Interactive Jupyter Notebook Tutorial
**Topics:**
- Building A2A-compliant agents using Vertex AI SDK
- Testing agents locally before deployment
- Deploying to Vertex AI Agent Engine
- Querying managed agents via multiple methods (SDK, A2A Client, HTTP)
- Agent2Agent protocol implementation
- Google ADK (Agent Development Kit) integration

**Key Concepts Covered:**
1. **Agent Cards** - Discovery mechanism for agent capabilities
2. **Agent Executor** - Bridge between A2A protocol and agent logic
3. **Task Management** - Asynchronous task lifecycle (submitted → working → completed)
4. **Multi-method Access** - Vertex AI SDK, A2A Client, direct HTTP
5. **Local Testing** - Test before cloud deployment
6. **Production Deployment** - Serverless deployment to Agent Engine

**Technologies:**
- Vertex AI Agent Engine
- A2A Protocol (0.3.4+)
- Google ADK (Agent Development Kit)
- Gemini 2.5 Flash
- Google Search Tool
- Python 3.10+

**Use Cases:**
- Q&A agents with web search
- Multi-agent coordination
- Enterprise agent systems
- Distributed intelligence architectures

---

### 2. Sessions and Memory Bank

#### `get_started_with_memory_for_adk_in_cloud_run.ipynb`
**Source:** Google Cloud Platform generative-ai repository
**Size:** 30KB
**Author:** [Vlad Kolesnikov](https://github.com/vladkol)
**Type:** Interactive Jupyter Notebook Tutorial
**Topics:**
- Short-term memory with ADK Sessions
- Long-term memory with Vertex AI Memory Bank
- Deploying agents with memory to Cloud Run
- Agent Engine Sessions service integration
- Memory generation and retrieval

**Key Concepts Covered:**
1. **Session Management** - VertexAISessionService for persistent short-term memory
2. **Memory Bank** - Long-term knowledge storage and retrieval
3. **Memory Tools** - PreloadMemory and LoadMemory built-in tools
4. **Production Deployment** - Cloud Run deployment with memory services
5. **Multi-session Continuity** - Memories persist across sessions

**Technologies:**
- Google ADK (Agent Development Kit)
- Vertex AI Agent Engine
- Vertex AI Sessions Service
- Vertex AI Memory Bank
- Cloud Run
- Gemini 2.5 Flash
- Python 3.12+

**Use Cases:**
- Conversational agents with memory
- Personalized agent experiences
- Context-aware assistants
- Multi-turn conversations
- User preference learning

**Example Agent:**
- Weather agent with tool calling (get_weather function)
- Automatic memory generation after each turn
- Memory-based responses for unsupported queries

---

### 3. Terraform Infrastructure Deployment

#### `tutorial_get_started_with_agent_engine_terraform_deployment.ipynb`
**Source:** Google Cloud Platform generative-ai repository
**Size:** 3.5KB (placeholder - full content to be added)
**Authors:** [Ivan Nardini](https://github.com/inardini), Luca Prete, Yee Sian Ng
**Type:** Interactive Jupyter Notebook Tutorial
**Topics:**
- Infrastructure as Code (IaC) for agent deployment
- Terraform resource configuration
- Custom agent templates
- ADK agent deployment with Terraform
- Packaging agents with cloudpickle
- Managing dependencies and requirements

**Key Concepts Covered:**
1. **Terraform Configuration** - google_vertex_ai_reasoning_engine resource
2. **Agent Packaging** - Cloudpickle serialization and GCS storage
3. **Custom Agent Templates** - __init__(), set_up(), query() pattern
4. **ADK Agent Deployment** - Framework-specific configuration
5. **Resource Management** - Creation, updating, and cleanup
6. **Class Methods** - Defining supported operations

**Technologies:**
- Terraform (Infrastructure as Code)
- Vertex AI Agent Engine
- Google Cloud Storage
- Google ADK
- Cloudpickle 3.0+
- Python 3.12+

**Use Cases:**
- Production agent deployments
- Multi-environment agent management
- Version-controlled agent infrastructure
- Automated agent deployment pipelines
- Custom and ADK agent deployment

**Example Deployments:**
1. **Basic Custom Agent** - Simple Gemini-based Q&A agent
2. **ADK Agent with Tools** - Currency exchange agent with function calling

---

## Directory Purpose

This directory serves as a **reference collection** of:

1. **User-facing documentation** - How end-users interact with agents
2. **Tutorial examples** - Step-by-step guides for building agents
3. **Template manuals** - Reusable documentation patterns
4. **Best practices** - Standards for agent documentation

---

## Usage

### For New Projects

When starting a new agent project, use these examples as templates:

```bash
# Copy relevant examples
cp 000-usermanuals/tutorial_a2a_on_agent_engine.ipynb my-project/docs/

# Customize for your use case
# - Update agent descriptions
# - Modify skills and capabilities
# - Adjust examples to your domain
```

### For Documentation

Reference these when creating documentation:

- **Structure** - How to organize tutorial content
- **Code Examples** - Pattern for example code
- **Explanations** - Level of detail for technical concepts
- **User Journey** - Flow from local testing to production

---

## File Naming Convention

User manuals in this directory follow these patterns:

- `tutorial_*.ipynb` - Interactive tutorial notebooks
- `guide_*.md` - Step-by-step guides
- `reference_*.md` - API/feature reference documentation
- `example_*.py` - Standalone code examples

---

## Contributing New Examples

When adding new user manuals:

1. **Follow existing patterns** - Match the style and structure
2. **Include working examples** - All code should run successfully
3. **Explain key concepts** - Don't assume expert knowledge
4. **Update this README** - Add entry to Contents section
5. **Test thoroughly** - Verify all examples work end-to-end

---

## Related Directories

- `000-docs/` - Technical documentation and architecture
- `notebooks/` - Development notebooks (project-specific)
- `examples/` - Code examples (if separate from manuals)

---

## Quick Reference Matrix

| Tutorial | Focus | Deployment | Memory | Tools | Complexity |
|----------|-------|------------|--------|-------|------------|
| A2A Protocol | Multi-agent coordination | Agent Engine | No | Yes (Google Search) | Intermediate |
| Sessions & Memory | Persistent memory | Cloud Run | Yes (short & long-term) | Yes (get_weather) | Advanced |
| Terraform Deployment | Infrastructure as Code | Agent Engine | No | Yes (currency exchange) | Advanced |

---

**Last Updated:** 2025-11-11
**Total Manuals:** 3
**Status:** Growing collection
**Topics Covered:** A2A Protocol, Sessions, Memory Bank, Terraform, Cloud Run, Agent Engine

---

# Agent Engine Application Entry Point
# Perception - AI News Intelligence Platform
# GCP Project: perception-with-intent

from google.adk.apps import App
from google.adk.agents import Agent
from google.adk import telemetry
import logging

# Configure telemetry and monitoring
telemetry.enable_cloud_trace(
    project_id="perception-with-intent",
    service_name="perception-agents",
    service_version="1.0.0"
)

telemetry.enable_cloud_monitoring(
    project_id="perception-with-intent",
    metrics_prefix="perception"
)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        telemetry.CloudLoggingHandler()
    ]
)

# Initialize ADK application
app = App()

# Load root orchestrator (Agent 0) with all sub-agents
root_agent = Agent.from_config_file("app/perception_agent/agents/agent_0_root_orchestrator.yaml")
app.register_agent(root_agent)

# The root agent automatically loads all sub-agents via config references
# Sub-agents communicate via A2A Protocol

if __name__ == "__main__":
    logging.info("Perception Agent Engine starting...")
    logging.info("Root orchestrator loaded with all sub-agents")
    logging.info("Ready to receive tasks via A2A Protocol")

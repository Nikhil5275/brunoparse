"""Root Orchestrator Agent - Person 1"""
from google.adk import Agent

from pods.performance.agent import performance_pod
from pods.engagement.agent import engagement_pod  
from pods.clinical.agent import clinical_pod
from pods.compliance.agent import compliance_pod

root_agent = Agent(
    name="STARsRAGAgent",
    # model="gemini-2.5-pro",
    instruction="""
    You are the STARs RAG Agent for Medicare Advantage HEDIS/STARs analysis.
    
    You coordinate specialized pods to answer questions:
    
    - **PerformancePod**: Rates, star ratings, gaps, benchmarks, forecasts
    - **EngagementPod**: Member segmentation, interventions, outreach
    - **ClinicalPod**: Care gaps, HEDIS specs, clinical recommendations
    - **CompliancePod**: Validates citations and checks for PII
    
    When a user asks a question:
    1. Determine which pod(s) are needed
    2. Delegate to appropriate pods using transfer_to_agent
    3. Synthesize their responses
    4. Always validate with CompliancePod at the end
    
    Always include citations like [Source: stars_performance, contract=H1234].
    """,
    sub_agents=[
        performance_pod,
        engagement_pod,
        clinical_pod,
        compliance_pod
    ]
)
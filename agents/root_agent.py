"""Root Orchestrator Agent - Person 1
Main agent that users interact with in Google ADK UI
Orchestrates routing, parallel pod execution, synthesis, and compliance
"""
from google.adk import Agent
import json
import asyncio
from typing import List, Dict

from .router import router_agent
from .synthesizer import synthesizer_agent
from pods.performance.agent import performance_pod
from pods.engagement.agent import engagement_pod
from pods.clinical.agent import clinical_pod
from pods.compliance.agent import compliance_pod


async def call_pod_async(pod_name: str, pod_agent: Agent, query: str) -> Dict:
    """Call a pod asynchronously for parallel execution

    Args:
        pod_name: Name of the pod
        pod_agent: The agent instance
        query: User query

    Returns:
        Dict with pod name and output
    """
    try:
        result = pod_agent.run(query)
        return {
            "pod": pod_name,
            "output": result.output,
            "success": True
        }
    except Exception as e:
        return {
            "pod": pod_name,
            "output": f"[Error: {str(e)}]",
            "success": False
        }


def orchestrate_query(user_question: str) -> str:
    """Orchestrate the full query flow with parallel pod execution

    Args:
        user_question: User's query

    Returns:
        Final synthesized and validated response
    """

    # Step 1: Route to appropriate pods
    print("🧭 Routing query...")
    routing_result = router_agent.run(user_question)

    try:
        routing_data = json.loads(routing_result.output)
        pods_to_call = routing_data.get("pods", [])
    except json.JSONDecodeError:
        # Fallback: call all pods except compliance
        pods_to_call = ["Performance", "Engagement", "Clinical", "Compliance"]

    print(f"✅ Routing: {pods_to_call}")

    # Step 2: Call pods IN PARALLEL
    pod_map = {
        "Performance": performance_pod,
        "Engagement": engagement_pod,
        "Clinical": clinical_pod
    }

    # Filter out Compliance (we'll run it at the end)
    work_pods = [p for p in pods_to_call if p != "Compliance"]

    print(f"🤖 Calling {len(work_pods)} pods in parallel...")

    # Run pods in parallel using asyncio
    async def run_pods_parallel():
        tasks = []
        for pod_name in work_pods:
            if pod_name in pod_map:
                task = call_pod_async(pod_name, pod_map[pod_name], user_question)
                tasks.append(task)

        return await asyncio.gather(*tasks)

    # Execute parallel pod calls
    pod_outputs = asyncio.run(run_pods_parallel())

    print(f"✅ {len(pod_outputs)} pods completed")

    # Step 3: Synthesize outputs
    print("🔄 Synthesizing...")

    combined_input = ""
    for pod_data in pod_outputs:
        combined_input += f"=== {pod_data['pod']} Pod Output ===\n"
        combined_input += f"{pod_data['output']}\n\n"

    synthesis_result = synthesizer_agent.run(
        f"Synthesize these pod outputs into one coherent response:\n\n{combined_input}"
    )
    final_response = synthesis_result.output

    print("✅ Synthesis complete")

    # Step 4: Compliance validation
    print("🛡️  Validating compliance...")

    compliance_result = compliance_pod.run(
        f"Validate this response:\n\n{final_response}"
    )

    compliance_output = compliance_result.output.lower()

    if "approved" not in compliance_output or "false" in compliance_output:
        final_response = f"⚠️ COMPLIANCE ISSUES:\n{compliance_result.output}\n\n---\n\n{final_response}"

    print("✅ Compliance check complete\n")

    return final_response


# Root agent that users interact with
root_agent = Agent(
    name="STARsRAGAgent",
    model="gemini-2.5-pro",
    instructions="""
    You are the STARs RAG Agent - an intelligent assistant for Medicare Advantage
    HEDIS/STARs performance analysis.

    When a user asks a question, you orchestrate multiple specialized pods to
    provide comprehensive, evidence-based answers.

    Your workflow:
    1. Route the query to appropriate pods (Performance, Engagement, Clinical)
    2. Call all relevant pods IN PARALLEL for fast response
    3. Synthesize their outputs into one coherent answer
    4. Validate compliance (citations, no PII)
    5. Return the final response to the user

    Always respond with professional, well-formatted answers that include:
    - Evidence-based findings with citations
    - Actionable recommendations
    - Clear, executive-level summaries

    You have access to the orchestrate_query function to handle this workflow.
    """,
    tools=[orchestrate_query]
)
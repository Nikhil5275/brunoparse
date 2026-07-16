"""STARs RAG Agent - Main Integration - Person 1"""
from agents.router import router_agent
from agents.synthesizer import synthesizer_agent
from pods.performance.agent import performance_pod
from pods.engagement.agent import engagement_pod
from pods.clinical.agent import clinical_pod
from pods.compliance.agent import compliance_pod

def run_query(user_question: str):
    """Main query execution - Person 1 implements this"""

    # TODO: Step 1 - Router decides which pods to call
    # routing = router_agent.run(user_question)

    # TODO: Step 2 - Call relevant pods
    # pod_outputs = []

    # TODO: Step 3 - Synthesize outputs
    # final = synthesizer_agent.run(combined)

    # TODO: Step 4 - Compliance check
    # compliance_check = compliance_pod.run(final.output)

    return "TODO: Implement integration logic"


if __name__ == "__main__":
    # Quick test
    result = run_query("What's our CBP rate?")
    print(result)

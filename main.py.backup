"""STARs RAG Agent - Main Integration - Person 1"""
import json
from agents.router import router_agent
from agents.synthesizer import synthesizer_agent
from pods.performance.agent import performance_pod
from pods.engagement.agent import engagement_pod
from pods.clinical.agent import clinical_pod
from pods.compliance.agent import compliance_pod


def run_query(user_question: str):
    """Main query execution - orchestrates routing, pod calls, synthesis, and validation

    Args:
        user_question: The user's query

    Returns:
        Final synthesized and validated response
    """

    print(f"\n{'='*60}")
    print(f"Query: {user_question}")
    print(f"{'='*60}\n")

    # =========================================================================
    # STEP 1: Router decides which pods to call
    # =========================================================================
    print("🧭 Step 1: Routing query to appropriate pods...")

    routing_result = router_agent.run(user_question)
    print(f"Router output:\n{routing_result.output}\n")

    # Parse the JSON response from router
    try:
        routing_data = json.loads(routing_result.output)
        pods_to_call = routing_data.get("pods", [])
        routing_reasoning = routing_data.get("reasoning", "No reasoning provided")

        print(f"✅ Routing decision: {pods_to_call}")
        print(f"   Reasoning: {routing_reasoning}\n")

    except json.JSONDecodeError as e:
        print(f"⚠️  Failed to parse router output as JSON: {e}")
        print(f"   Falling back to all pods...")
        # Fallback: call all pods if routing fails
        pods_to_call = ["Performance", "Engagement", "Clinical", "Compliance"]


    # =========================================================================
    # STEP 2: Call relevant pods
    # =========================================================================
    print("🤖 Step 2: Calling selected pods...\n")

    pod_outputs = []
    pod_map = {
        "Performance": performance_pod,
        "Engagement": engagement_pod,
        "Clinical": clinical_pod,
        "Compliance": compliance_pod
    }

    # Call each pod (except Compliance - we'll handle that separately)
    for pod_name in pods_to_call:
        if pod_name == "Compliance":
            continue  # Skip compliance for now, we'll validate at the end

        if pod_name in pod_map:
            print(f"   Calling {pod_name} Pod...")
            try:
                pod_agent = pod_map[pod_name]
                result = pod_agent.run(user_question)

                pod_outputs.append({
                    "pod": pod_name,
                    "output": result.output
                })

                print(f"   ✅ {pod_name} Pod completed\n")

            except Exception as e:
                print(f"   ❌ {pod_name} Pod failed: {e}\n")
                pod_outputs.append({
                    "pod": pod_name,
                    "output": f"[Error: {pod_name} Pod encountered an error]"
                })
        else:
            print(f"   ⚠️  Unknown pod: {pod_name}\n")


    # =========================================================================
    # STEP 3: Synthesize outputs
    # =========================================================================
    print("🔄 Step 3: Synthesizing pod outputs...\n")

    if not pod_outputs:
        return "❌ No pod outputs to synthesize. Check pod routing and execution."

    # Combine pod outputs into a format for the synthesizer
    combined_input = ""
    for pod_data in pod_outputs:
        combined_input += f"=== {pod_data['pod']} Pod Output ===\n"
        combined_input += f"{pod_data['output']}\n\n"

    print(f"Combined pod outputs:\n{combined_input}\n")

    # Synthesize into final response
    print("   Synthesizing final response...")
    try:
        synthesis_result = synthesizer_agent.run(
            f"Synthesize these pod outputs into one coherent response:\n\n{combined_input}"
        )
        final_response = synthesis_result.output
        print(f"   ✅ Synthesis completed\n")

    except Exception as e:
        print(f"   ❌ Synthesis failed: {e}\n")
        # Fallback: just concatenate outputs
        final_response = combined_input


    # =========================================================================
    # STEP 4: Compliance validation
    # =========================================================================
    print("🛡️  Step 4: Running compliance validation...\n")

    try:
        compliance_result = compliance_pod.run(
            f"Validate this response for citations and PII:\n\n{final_response}"
        )

        compliance_output = compliance_result.output.lower()

        print(f"Compliance check:\n{compliance_result.output}\n")

        # Check if compliance approved
        if "approved" in compliance_output and "false" not in compliance_output:
            print("✅ Compliance check PASSED\n")
        else:
            print("⚠️  Compliance check FAILED - Review response\n")
            final_response = f"⚠️ COMPLIANCE ISSUES DETECTED:\n{compliance_result.output}\n\n---\n\n{final_response}"

    except Exception as e:
        print(f"⚠️  Compliance check failed to run: {e}\n")


    # =========================================================================
    # Return final response
    # =========================================================================
    print(f"{'='*60}")
    print("✅ Query processing complete!")
    print(f"{'='*60}\n")

    return final_response


if __name__ == "__main__":
    # Quick test
    print("\n🚀 STARs RAG Agent - Test Mode\n")

    test_queries = [
        "What's our CBP rate?",
        # "Which member segments have the lowest diabetes control rates?",
        # "What's our gap to achieving 4 stars for blood pressure control?"
    ]

    for query in test_queries:
        result = run_query(query)
        print("\n" + "="*60)
        print("FINAL RESPONSE:")
        print("="*60)
        print(result)
        print("\n" + "="*60 + "\n")

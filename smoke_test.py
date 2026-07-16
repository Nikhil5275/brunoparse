#!/usr/bin/env python3
"""
Pod Smoke Testing Script
Quick integration tests for all pods

Usage:
    python smoke_test.py performance "What's our CBP rate?"
    python smoke_test.py engagement "Which age groups need outreach?"
    python smoke_test.py clinical "Show open care gaps for diabetes"
    python smoke_test.py compliance "Check this text: [Source: test]"
"""

import sys
from dotenv import load_dotenv

load_dotenv()


def test_performance_pod(query: str):
    """Test Performance Pod - Person 2"""
    from pods.performance.agent import performance_pod

    print(f"🧪 Testing Performance Pod...")
    print(f"Query: {query}\n")

    result = performance_pod.run(query)
    print(f"✅ Result:\n{result.output}\n")
    return result


def test_engagement_pod(query: str):
    """Test Engagement Pod - Person 3"""
    from pods.engagement.agent import engagement_pod

    print(f"🧪 Testing Engagement Pod...")
    print(f"Query: {query}\n")

    result = engagement_pod.run(query)
    print(f"✅ Result:\n{result.output}\n")
    return result


def test_clinical_pod(query: str):
    """Test Clinical Pod - Person 4"""
    from pods.clinical.agent import clinical_pod

    print(f"🧪 Testing Clinical Pod...")
    print(f"Query: {query}\n")

    result = clinical_pod.run(query)
    print(f"✅ Result:\n{result.output}\n")
    return result


def test_compliance_pod(query: str):
    """Test Compliance Pod - Person 5"""
    from pods.compliance.agent import compliance_pod

    print(f"🧪 Testing Compliance Pod...")
    print(f"Query: {query}\n")

    result = compliance_pod.run(query)
    print(f"✅ Result:\n{result.output}\n")
    return result


def test_tool_directly():
    """Test individual tools without the agent"""
    print("🔧 Testing tools directly...\n")

    # Example: Test Performance Pod tools
    from pods.performance.tools import query_stars_performance, compute_star_gap

    print("Testing query_stars_performance...")
    result = query_stars_performance(measure="CBP", contract="H1234", year=2025)
    print(f"Result: {result}\n")

    print("Testing compute_star_gap...")
    gap = compute_star_gap(current_rate=0.65, measure="CBP", target_star=4)
    print(f"Gap Analysis: {gap}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python smoke_test.py <pod_name> [query]")
        print("\nAvailable pods:")
        print("  performance  - Person 2")
        print("  engagement   - Person 3")
        print("  clinical     - Person 4")
        print("  compliance   - Person 5")
        print("  tools        - Test tools directly")
        print("\nExample:")
        print('  python smoke_test.py performance "What is our CBP rate?"')
        sys.exit(1)

    pod_name = sys.argv[1].lower()
    query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Test query"

    try:
        if pod_name == "performance":
            test_performance_pod(query)
        elif pod_name == "engagement":
            test_engagement_pod(query)
        elif pod_name == "clinical":
            test_clinical_pod(query)
        elif pod_name == "compliance":
            test_compliance_pod(query)
        elif pod_name == "tools":
            test_tool_directly()
        else:
            print(f"❌ Unknown pod: {pod_name}")
            print("Choose: performance, engagement, clinical, compliance, or tools")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
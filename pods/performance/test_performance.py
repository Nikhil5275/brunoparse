#!/usr/bin/env python3
"""
Performance Pod Unit Tests - Person 2
Create your own detailed tests here

Run: python pods/performance/test_performance.py
"""

from dotenv import load_dotenv
load_dotenv()

from pods.performance.tools import query_stars_performance, compute_star_gap


def test_query_stars_performance():
    """Test querying BigQuery for performance data"""
    print("🧪 Testing query_stars_performance...")

    # Test 1: Valid query
    result = query_stars_performance(
        measure="CBP",
        contract="H1234",
        year=2025
    )
    print(f"✅ Result: {result}\n")

    # Test 2: Different measure
    result2 = query_stars_performance(
        measure="CDC",
        contract="H1234",
        year=2025
    )
    print(f"✅ Diabetes result: {result2}\n")

    # Test 3: Invalid measure (should return error)
    result3 = query_stars_performance(
        measure="INVALID",
        contract="H1234",
        year=2025
    )
    print(f"✅ Error handling: {result3}\n")


def test_compute_star_gap():
    """Test star gap calculations"""
    print("🧪 Testing compute_star_gap...")

    # Test 1: Currently at 3 stars, want 4 stars
    result = compute_star_gap(
        current_rate=0.65,
        measure="CBP",
        target_star=4
    )
    print(f"✅ Gap to 4 stars: {result}\n")
    assert result["current_star"] == 3
    assert result["target_star"] == 4

    # Test 2: Already at 5 stars
    result2 = compute_star_gap(
        current_rate=0.80,
        measure="CBP",
        target_star=5
    )
    print(f"✅ Already at 5 stars: {result2}\n")

    # Test 3: Low performance
    result3 = compute_star_gap(
        current_rate=0.50,
        measure="CBP",
        target_star=3
    )
    print(f"✅ Low performance: {result3}\n")


def test_agent_integration():
    """Test the full agent with tools"""
    print("🧪 Testing full Performance Pod agent...")

    from pods.performance.agent import performance_pod

    # Test query
    result = performance_pod.run(
        "What is our current CBP rate and how far are we from 4 stars?"
    )
    print(f"✅ Agent response:\n{result.output}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Performance Pod Tests - Person 2")
    print("=" * 60 + "\n")

    try:
        # Test tools individually
        test_query_stars_performance()
        test_compute_star_gap()

        # Test full agent (comment out if agent not ready)
        # test_agent_integration()

        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
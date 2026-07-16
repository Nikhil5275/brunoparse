#!/usr/bin/env python3
"""
Engagement Pod Unit Tests - Person 3
Run: python pods/engagement/test_engagement.py
"""

from dotenv import load_dotenv
load_dotenv()

from pods.engagement.tools import query_member_segments, search_intervention_history


def test_query_member_segments():
    """Test member segmentation queries"""
    print("🧪 Testing query_member_segments...")

    # Test different dimension combinations
    result = query_member_segments(
        measure="CBP",
        dimensions=["age_group", "geography"],
        contract="H1234"
    )
    print(f"✅ Segmentation result: {result}\n")


def test_search_intervention_history():
    """Test intervention history retrieval"""
    print("🧪 Testing search_intervention_history...")

    result = search_intervention_history(
        measure="CBP",
        year=2024
    )
    print(f"✅ Past interventions: {result}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Engagement Pod Tests - Person 3")
    print("=" * 60 + "\n")

    try:
        test_query_member_segments()
        test_search_intervention_history()

        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
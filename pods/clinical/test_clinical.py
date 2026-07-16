#!/usr/bin/env python3
"""
Clinical Pod Unit Tests - Person 4
Run: python pods/clinical/test_clinical.py
"""

from dotenv import load_dotenv
load_dotenv()

from pods.clinical.tools import query_care_gaps


def test_query_care_gaps():
    """Test care gap queries"""
    print("🧪 Testing query_care_gaps...")

    result = query_care_gaps(
        measure="CBP",
        contract="H1234",
        limit=100
    )
    print(f"✅ Care gaps result: {result}\n")
    print(f"   Total gaps: {result['total_open_gaps']}")
    print(f"   Top priority members: {len(result['top_priority_members'])}")


if __name__ == "__main__":
    print("=" * 60)
    print("Clinical Pod Tests - Person 4")
    print("=" * 60 + "\n")

    try:
        test_query_care_gaps()

        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
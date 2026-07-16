#!/usr/bin/env python3
"""
Compliance Pod Unit Tests - Person 5
Run: python pods/compliance/test_compliance.py
"""

from dotenv import load_dotenv
load_dotenv()

from pods.compliance.tools import cross_check_citations, scan_for_pii


def test_cross_check_citations():
    """Test citation validation"""
    print("🧪 Testing cross_check_citations...")

    # Test 1: Good response with citations
    good_text = """
    Our CBP rate is 65% [Source: stars_performance, contract=H1234].
    We need to improve by 8.2 percentage points [Source: cms_thresholds].
    """
    result = cross_check_citations(good_text)
    print(f"✅ Good citations: {result}\n")
    assert result["approved"] == True

    # Test 2: Bad response - numbers without citations
    bad_text = """
    Our CBP rate is 65% and we need to improve by 8.2 percentage points.
    """
    result2 = cross_check_citations(bad_text)
    print(f"✅ Missing citations caught: {result2}\n")
    assert result2["approved"] == False


def test_scan_for_pii():
    """Test PII detection"""
    print("🧪 Testing scan_for_pii...")

    # Test 1: Clean text
    clean_text = "Our overall performance is strong."
    result = scan_for_pii(clean_text)
    print(f"✅ No PII: {result}\n")
    assert result["pii_detected"] == False

    # Test 2: Text with member ID
    pii_text = "Member M1234567 needs outreach."
    result2 = scan_for_pii(pii_text)
    print(f"✅ PII detected: {result2}\n")
    assert result2["pii_detected"] == True


if __name__ == "__main__":
    print("=" * 60)
    print("Compliance Pod Tests - Person 5")
    print("=" * 60 + "\n")

    try:
        test_cross_check_citations()
        test_scan_for_pii()

        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
"""Compliance Pod Tools - Person 5"""
import re

def cross_check_citations(response_text: str):
    """Check if response has citations

    Args:
        response_text: Text to validate

    Returns:
        dict with approved status and issues
    """
    # Simple regex to find [Source: ...] patterns
    citations = re.findall(r'\[Source:.*?\]', response_text)

    # Find numbers (rates, percentages)
    numbers = re.findall(r'\d+\.?\d*%', response_text)

    if len(numbers) > 0 and len(citations) == 0:
        return {
            "approved": False,
            "issues": [f"Found {len(numbers)} numerical claims but no citations"]
        }

    return {
        "approved": True,
        "citations_found": len(citations)
    }


def scan_for_pii(text: str):
    """Simple PII detection (optional)

    Args:
        text: Text to scan

    Returns:
        dict with pii_detected status
    """
    # Check for member IDs (pattern: M + 7 digits)
    member_ids = re.findall(r'M\d{7}', text)

    if member_ids:
        return {
            "pii_detected": True,
            "issues": [f"Found member IDs: {member_ids}"]
        }

    return {"pii_detected": False}

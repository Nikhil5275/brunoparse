"""Compliance Pod Tools - Person 5."""


import math

import re

from typing import Any

import os
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-43ecffa89f51") 
BQ_DATASET = "humana_hackathon"




# -------------------------------------------------------------------

# Reusable patterns

# -------------------------------------------------------------------


CITATION_PATTERN = re.compile(

    r"\[(?:Source|Sources):\s*[^\]]+\]",

    flags=re.IGNORECASE,

)


QUANTITATIVE_PATTERN = re.compile(

    r"""

    \b\d+(?:\.\d+)?\s*%                       

    |

    \b\d+(?:\.\d+)?\s*

    (?:pp|percentage\s+points?)\b              

    |

    \b\d+\s+(?:additional\s+)?

    (?:members?|gaps?|closures?)\b             

    |

    \b\d+(?:\.\d+)?[-\s]?stars?\b             

    """,

    flags=re.IGNORECASE | re.VERBOSE,

)


MEMBER_ID_PATTERN = re.compile(

    r"\bM\d{7}\b",

    flags=re.IGNORECASE,

)


EMAIL_PATTERN = re.compile(

    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",

    flags=re.IGNORECASE,

)


PHONE_PATTERN = re.compile(

    r"\b(?:\+?1[-.\s]?)?"

    r"(?:\(?\d{3}\)?[-.\s]?)"

    r"\d{3}[-.\s]?\d{4}\b"

)




# -------------------------------------------------------------------

# Citation validation

# -------------------------------------------------------------------


def cross_check_citations(

    response_text: str,

) -> dict[str, Any]:

    """Check whether quantitative responses include citations.


    Expected format:

        [Source: stars_performance | measure_id=MRP | year=2026]


    This checks citation presence only. It does not prove that every

    citation supports every claim.


    Args:

        response_text: Proposed response to validate.


    Returns:

        Structured validation result.

    """


    citations = CITATION_PATTERN.findall(response_text)

    quantitative_claims = QUANTITATIVE_PATTERN.findall(

        response_text

    )


    issues: list[str] = []


    if quantitative_claims and not citations:

        issues.append(

            "Quantitative claims were found, but no source "

            "citation was included."

        )


    return {

        "check": "citation_presence",

        "approved": len(issues) == 0,

        "citation_count": len(citations),

        "quantitative_claim_count": len(

            quantitative_claims

        ),

        "issues": issues,

        "limitations": [

            "This validates citation presence, not whether each "

            "citation supports its associated claim."

        ],

    }




# -------------------------------------------------------------------

# Identifier scanning

# -------------------------------------------------------------------


def scan_for_pii(

    text: str,

) -> dict[str, Any]:

    """Perform lightweight pattern-based identifier detection.


    This is not a complete regulatory or privacy compliance review.


    Args:

        text: Proposed response to scan.


    Returns:

        Structured validation result without repeating identifiers.

    """


    finding_counts = {

        "member_id": len(

            MEMBER_ID_PATTERN.findall(text)

        ),

        "email": len(

            EMAIL_PATTERN.findall(text)

        ),

        "phone": len(

            PHONE_PATTERN.findall(text)

        ),

    }


    total_findings = sum(finding_counts.values())


    issues: list[str] = []


    if total_findings:

        issues.append(

            "Potential direct identifiers were detected. "

            "Redact or aggregate the response before display."

        )


    return {

        "check": "pii_pattern_scan",

        "approved": total_findings == 0,

        "pii_detected": total_findings > 0,

        "finding_count": total_findings,

        "finding_types": finding_counts,

        "issues": issues,

        "limitations": [

            "Pattern matching cannot detect every form of "

            "protected or personally identifiable information.",

            "The absence of a finding does not establish full "

            "privacy or regulatory compliance.",

        ],

    }




# -------------------------------------------------------------------

# STAR arithmetic validation

# -------------------------------------------------------------------


def validate_star_arithmetic(

    members_eligible: int,

    members_compliant: int,

    reported_rate_pct: float,

    reported_gap_count: int,

    target_threshold_pct: float | None = None,

    reported_additional_members: int | None = None,

    tolerance_pp: float = 0.05,

) -> dict[str, Any]:

    """Validate rate, open-gap, and threshold calculations.


    Args:

        members_eligible: Number of eligible members.

        members_compliant: Number of compliant members.

        reported_rate_pct: Rate shown in the proposed answer.

        reported_gap_count: Open gaps shown in the answer.

        target_threshold_pct: Target threshold from 0 to 100.

        reported_additional_members: Claimed number of additional

            compliant members needed.

        tolerance_pp: Allowed rate difference due to rounding.


    Returns:

        Structured validation result.


    Threshold calculations assume that the denominator remains fixed.

    """


    issues: list[str] = []


    if members_eligible <= 0:

        return {

            "check": "star_arithmetic",

            "approved": False,

            "issues": [

                "Members eligible must be greater than zero."

            ],

        }


    if members_compliant < 0:

        issues.append(

            "Members compliant cannot be negative."

        )


    if members_compliant > members_eligible:

        issues.append(

            "Members compliant cannot exceed members eligible."

        )


    calculated_rate_pct = round(

        members_compliant

        / members_eligible

        * 100,

        2,

    )


    calculated_gap_count = (

        members_eligible - members_compliant

    )


    if (

        abs(calculated_rate_pct - reported_rate_pct)

        > tolerance_pp

    ):

        issues.append(

            f"Reported rate is incorrect. Expected "

            f"{calculated_rate_pct}% from "

            f"{members_compliant}/{members_eligible}."

        )


    if calculated_gap_count != reported_gap_count:

        issues.append(

            f"Reported gap count is incorrect. Expected "

            f"{calculated_gap_count} open gaps."

        )


    calculated_additional_members = None


    if target_threshold_pct is not None:

        if target_threshold_pct < 0 or target_threshold_pct > 100:

            issues.append(

                "Target threshold must be between 0 and 100."

            )


        elif 0 < target_threshold_pct <= 1:

            issues.append(

                "Target threshold appears to use a 0-to-1 "

                "decimal scale. The project standard is a "

                "0-to-100 percentage scale."

            )


        else:

            required_compliant = math.ceil(

                target_threshold_pct

                / 100

                * members_eligible

            )


            calculated_additional_members = max(

                0,

                required_compliant - members_compliant,

            )


            if (

                reported_additional_members is not None

                and reported_additional_members

                != calculated_additional_members

            ):

                issues.append(

                    "Reported additional-member estimate is "

                    f"incorrect. Expected approximately "

                    f"{calculated_additional_members}."

                )


    return {

        "check": "star_arithmetic",

        "approved": len(issues) == 0,

        "calculated_rate_pct": calculated_rate_pct,

        "calculated_gap_count": calculated_gap_count,

        "calculated_additional_members": (

            calculated_additional_members

        ),

        "issues": issues,

        "assumptions": [

            "The eligible-member denominator remains unchanged.",

            "The supplied threshold applies to the requested year.",

            "The calculation does not account for future "

            "eligibility changes, exclusions, or data lag.",

        ],

    }




# -------------------------------------------------------------------

# Threshold validation

# -------------------------------------------------------------------


def validate_threshold(

    performance_year: int,

    threshold_year: int,

    measure_id: str,

    target_star: int,

    threshold_pct: float,

    threshold_source: str,

    performance_table_threshold_pct: float | None = None,

    tolerance_pp: float = 0.001,

) -> dict[str, Any]:

    """Validate a threshold's year, units, source, and value.


    Args:

        performance_year: Year associated with performance data.

        threshold_year: Year associated with the threshold.

        measure_id: Measure identifier such as CBP or MRP.

        target_star: Target star level from 2 through 5.

        threshold_pct: Proposed threshold from 0 to 100.

        threshold_source: Source of the threshold.

        performance_table_threshold_pct: Corresponding benchmark

            from stars_performance, when available.

        tolerance_pp: Allowed threshold difference.


    Returns:

        Structured validation result.

    """


    issues: list[str] = []


    normalized_measure_id = measure_id.strip().upper()


    if not normalized_measure_id:

        issues.append(

            "Measure ID is required."

        )


    if performance_year != threshold_year:

        issues.append(

            f"Threshold year mismatch: performance data is "

            f"for {performance_year}, but the threshold is "

            f"from {threshold_year}."

        )


    if target_star not in {2, 3, 4, 5}:

        issues.append(

            "Target star must be 2, 3, 4, or 5."

        )


    if threshold_pct < 0 or threshold_pct > 100:

        issues.append(

            "Threshold must be between 0 and 100."

        )


    elif 0 < threshold_pct <= 1:

        issues.append(

            "Threshold appears to use a 0-to-1 decimal scale. "

            "The project standard is a 0-to-100 percentage scale."

        )


    if not threshold_source.strip():

        issues.append(

            "Threshold source is missing."

        )


    if (

        performance_table_threshold_pct is not None

        and abs(

            threshold_pct

            - performance_table_threshold_pct

        ) > tolerance_pp

    ):

        issues.append(

            f"Threshold conflict for {normalized_measure_id}: "

            f"the proposed threshold is {threshold_pct}%, but "

            f"stars_performance contains "

            f"{performance_table_threshold_pct}% for the "

            f"{target_star}-star benchmark."

        )


    return {

        "check": "threshold_validation",

        "approved": len(issues) == 0,

        "measure_id": normalized_measure_id,

        "performance_year": performance_year,

        "threshold_year": threshold_year,

        "target_star": target_star,

        "threshold_pct": threshold_pct,

        "threshold_source": threshold_source,

        "issues": issues,

    }




# -------------------------------------------------------------------

# Combined validation

# -------------------------------------------------------------------


def validate_response(

    response_text: str,

    arithmetic_input: dict[str, Any] | None = None,

    threshold_input: dict[str, Any] | None = None,

) -> dict[str, Any]:

    """Run all applicable Compliance Pod checks.


    Args:

        response_text: Proposed answer.

        arithmetic_input: Optional arguments for

            validate_star_arithmetic.

        threshold_input: Optional arguments for validate_threshold.


    Returns:

        Final APPROVED or REJECTED_WITH_ISSUES result.

    """


    checks: list[dict[str, Any]] = [

        cross_check_citations(response_text),

        scan_for_pii(response_text),

    ]


    if arithmetic_input is not None:

        checks.append(

            validate_star_arithmetic(**arithmetic_input)

        )


    if threshold_input is not None:

        checks.append(

            validate_threshold(**threshold_input)

        )


    failed_checks = [

        check

        for check in checks

        if not check.get("approved", False)

    ]


    issues = [

        issue

        for check in failed_checks

        for issue in check.get("issues", [])

    ]


    approved = len(failed_checks) == 0


    return {

        "status": (

            "APPROVED"

            if approved

            else "REJECTED_WITH_ISSUES"

        ),

        "approved": approved,

        "checks": checks,

        "issue_count": len(issues),

        "issues": issues,

        "required_action": (

            "Response may proceed to the user."

            if approved

            else "Correct the listed issues and validate again."

        ),

    }
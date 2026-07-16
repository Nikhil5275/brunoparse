#!/bin/bash

# STARs RAG Agent - Pod Structure Setup
# Run this AFTER setup.sh to create pod-based organization

set -e

echo "🏗️  Creating Pod Structure..."
echo "================================"

# Create pods directory structure
echo "✓ Creating pod directories..."
mkdir -p pods/performance
mkdir -p pods/engagement
mkdir -p pods/clinical
mkdir -p pods/compliance

# Create __init__.py files
echo "✓ Creating Python package files..."
touch pods/__init__.py
touch pods/performance/__init__.py
touch pods/engagement/__init__.py
touch pods/clinical/__init__.py
touch pods/compliance/__init__.py

# Create placeholder files for each pod
echo "✓ Creating placeholder files..."

# Performance Pod (Person 2)
cat > pods/performance/agent.py << 'EOF'
"""Performance Intelligence Pod - Person 2"""
from google.adk import Agent
from .tools import query_stars_performance, compute_star_gap

performance_pod = Agent(
    name="PerformancePod",
    model="gemini-2.0-flash",
    instructions="""
    You are the Performance Intelligence Pod.

    Your job:
    - Query current HEDIS/STARs rates
    - Calculate gaps to star thresholds
    - Compare to benchmarks
    - Forecast trends

    CRITICAL: Always cite sources like [Source: stars_performance, contract=H1234]
    """,
    tools=[query_stars_performance, compute_star_gap]
)
EOF

cat > pods/performance/tools.py << 'EOF'
"""Performance Pod Tools - Person 2"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

def query_stars_performance(measure: str, contract: str, year: int = 2025):
    """Query current performance from BigQuery

    Args:
        measure: Measure code (e.g., 'CBP', 'CDC')
        contract: Contract ID (e.g., 'H1234')
        year: Year (default: 2025)

    Returns:
        dict with rate, star_rating, numerator, denominator
    """
    query = f"""
    SELECT measure_code, rate, star_rating, numerator, denominator
    FROM `{PROJECT_ID}.{BQ_DATASET}.stars_performance`
    WHERE measure_code = '{measure}'
      AND contract_id = '{contract}'
      AND year = {year}
    """

    result = client.query(query).to_dataframe()

    if result.empty:
        return {"error": f"No data for {measure}"}

    return result.to_dict('records')[0]


def compute_star_gap(current_rate: float, measure: str, target_star: int):
    """Calculate gap to target star threshold

    Args:
        current_rate: Current rate (0-1)
        measure: Measure code
        target_star: Target star level (2-5)

    Returns:
        dict with gap analysis
    """
    from config.cms_thresholds import STAR_THRESHOLDS

    target_threshold = STAR_THRESHOLDS[measure][target_star]
    gap = target_threshold - current_rate

    # Find current star
    current_star = 2
    for star in sorted(STAR_THRESHOLDS[measure].keys()):
        if current_rate >= STAR_THRESHOLDS[measure][star]:
            current_star = star

    return {
        "measure": measure,
        "current_rate": current_rate,
        "current_star": current_star,
        "target_star": target_star,
        "gap_percentage_points": round(gap, 3)
    }
EOF

# Engagement Pod (Person 3)
cat > pods/engagement/agent.py << 'EOF'
"""Engagement Intelligence Pod - Person 3"""
from google.adk import Agent
from .tools import query_member_segments, search_intervention_history

engagement_pod = Agent(
    name="EngagementPod",
    model="gemini-2.5-pro",
    instructions="""
    You are the Engagement Intelligence Pod.

    Your job:
    - Segment member populations
    - Analyze intervention effectiveness
    - Recommend outreach strategies

    Always cite sources: [Source: segment_performance, dimensions=age+geography]
    """,
    tools=[query_member_segments, search_intervention_history]
)
EOF

cat > pods/engagement/tools.py << 'EOF'
"""Engagement Pod Tools - Person 3"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

def query_member_segments(measure: str, dimensions: list, contract: str = "H1234"):
    """Query member segments with GROUP BY

    Args:
        measure: Measure code
        dimensions: List of columns to segment by (e.g., ['age_group', 'geography'])
        contract: Contract ID

    Returns:
        List of segment breakdowns
    """
    dimension_cols = ", ".join(dimensions)

    query = f"""
    SELECT
        {dimension_cols},
        COUNT(*) as member_count,
        AVG(compliant) as compliance_rate
    FROM `{PROJECT_ID}.{BQ_DATASET}.segment_performance`
    WHERE measure_code = '{measure}'
      AND contract_id = '{contract}'
    GROUP BY {dimension_cols}
    ORDER BY compliance_rate ASC
    LIMIT 10
    """

    result = client.query(query).to_dataframe()
    return result.to_dict('records')


def search_intervention_history(measure: str, year: int = 2024):
    """Get past intervention results

    Args:
        measure: Measure code
        year: Year to look at

    Returns:
        List of past interventions
    """
    query = f"""
    SELECT
        intervention_name,
        outcome_delta,
        population_size,
        cost_per_member,
        description
    FROM `{PROJECT_ID}.{BQ_DATASET}.historical_interventions`
    WHERE measure_code = '{measure}'
      AND year = {year}
    ORDER BY outcome_delta DESC
    LIMIT 5
    """

    result = client.query(query).to_dataframe()
    return result.to_dict('records')
EOF

# Clinical Pod (Person 4)
cat > pods/clinical/agent.py << 'EOF'
"""Clinical Operations Pod - Person 4"""
from google.adk import Agent
from .tools import query_care_gaps

clinical_pod = Agent(
    name="ClinicalPod",
    model="gemini-2.5-pro",
    instructions="""
    You are the Clinical Operations Pod.

    Your job:
    - Identify open care gaps
    - Interpret HEDIS specifications
    - Recommend clinical interventions

    Always cite: [Source: care_gaps, measure=CBP]
    """,
    tools=[query_care_gaps]
)
EOF

cat > pods/clinical/tools.py << 'EOF'
"""Clinical Pod Tools - Person 4"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

def query_care_gaps(measure: str, contract: str = "H1234", limit: int = 100):
    """Query open care gaps

    Args:
        measure: Measure code
        contract: Contract ID
        limit: Max gaps to return

    Returns:
        dict with total_open_gaps and top_priority_members
    """
    query = f"""
    SELECT
        member_id,
        measure_code,
        gap_status,
        days_open,
        closure_likelihood_score
    FROM `{PROJECT_ID}.{BQ_DATASET}.care_gaps`
    WHERE measure_code = '{measure}'
      AND gap_status = 'open'
      AND contract_id = '{contract}'
    ORDER BY closure_likelihood_score DESC
    LIMIT {limit}
    """

    result = client.query(query).to_dataframe()

    return {
        "total_open_gaps": len(result),
        "top_priority_members": result.head(10).to_dict('records')
    }
EOF

# Compliance Pod (Person 5)
cat > pods/compliance/agent.py << 'EOF'
"""Compliance & Evidence Pod - Person 5"""
from google.adk import Agent
from .tools import cross_check_citations

compliance_pod = Agent(
    name="CompliancePod",
    model="gemini-2.0-flash",
    instructions="""
    You are the Compliance & Evidence Pod.

    Your job:
    - Verify all numerical claims have citations
    - Check for PII leaks (member names, IDs)
    - Validate star rating thresholds

    Output: APPROVED or list of issues
    """,
    tools=[cross_check_citations]
)
EOF

cat > pods/compliance/tools.py << 'EOF'
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
EOF

# Create CMS Thresholds (Person 5 will update, but we create template)
echo "✓ Creating CMS thresholds template..."
cat > config/cms_thresholds.py << 'EOF'
"""CMS 2025 Star Rating Thresholds - Person 5 Update This"""

STAR_THRESHOLDS = {
    "CBP": {  # Controlling Blood Pressure
        2: 0.55,
        3: 0.60,
        4: 0.732,
        5: 0.782
    },
    "CDC": {  # Comprehensive Diabetes Care
        2: 0.70,
        3: 0.75,
        4: 0.83,
        5: 0.87
    },
    "HbA1c": {  # HbA1c Control (<8%)
        2: 0.60,
        3: 0.65,
        4: 0.72,
        5: 0.78
    },
    "COL": {  # Colorectal Cancer Screening
        2: 0.55,
        3: 0.60,
        4: 0.68,
        5: 0.74
    },
    "BCS": {  # Breast Cancer Screening
        2: 0.65,
        3: 0.70,
        4: 0.75,
        5: 0.80
    }
}
EOF

# Create Router agent (Person 1)
echo "✓ Creating Router agent..."
cat > agents/router.py << 'EOF'
"""Pod Router Agent - Person 1"""
from google.adk import Agent

router_agent = Agent(
    name="PodRouter",
    model="gemini-2.0-flash",
    instructions="""
    You are the Pod Router. Analyze the query and route to relevant pods.

    Routing rules:
    - Performance metrics (rates, trends, benchmarks) → Performance Pod
    - Segmentation, interventions → Engagement Pod
    - Care gaps, HEDIS questions → Clinical Pod
    - Always route to Compliance Pod last for validation

    For complex queries, route to multiple pods.

    Output format: List which pods to call.
    """,
    tools=[]  # Will add transfer_to_agent later
)
EOF

# Create Synthesizer agent (Person 1)
echo "✓ Creating Synthesizer agent..."
cat > agents/synthesizer.py << 'EOF'
"""Synthesizer Agent - Person 1"""
from google.adk import Agent

synthesizer_agent = Agent(
    name="Synthesizer",
    model="gemini-2.5-pro",
    instructions="""
    You are the Synthesizer. Merge outputs from multiple pods into one coherent response.

    Rules:
    - Keep all citations from pods
    - Create smooth narrative flow
    - Highlight key insights
    - Format with markdown

    Always end with: [Sources: pod1, pod2, ...]
    """,
    tools=[]
)
EOF

# Create main.py template (Person 1)
echo "✓ Creating main.py template..."
cat > main.py << 'EOF'
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
EOF

# Create team assignment doc
echo "✓ Creating team assignments..."
cat > TEAM_ASSIGNMENTS.md << 'EOF'
# Team Assignments - Who Does What

## Person 1 (YOU - Coordinator)
**Your Files:**
- `agents/router.py` - Route queries to pods
- `agents/synthesizer.py` - Merge pod outputs
- `main.py` - Integration logic

**Your Tasks:**
1. Build router logic (1 hour)
2. Build synthesizer logic (1 hour)
3. Wire all pods together in main.py (1-2 hours)
4. Integration testing (1 hour)

---

## Person 2 (Performance Pod)
**Your Folder:** `pods/performance/`
- `agent.py` - Performance pod agent (already created)
- `tools.py` - Add your tools here

**Your Tasks:**
1. Explore BigQuery tables (30 min)
2. Test `query_stars_performance()` (1 hour)
3. Test `compute_star_gap()` (1 hour)
4. Add optional tools if time (benchmarks, forecasts)

---

## Person 3 (Engagement Pod)
**Your Folder:** `pods/engagement/`
- `agent.py` - Engagement pod agent (already created)
- `tools.py` - Add your tools here

**Your Tasks:**
1. Explore BigQuery tables (30 min)
2. Test `query_member_segments()` (1 hour)
3. Test `search_intervention_history()` (1 hour)
4. Add optional tools if time

---

## Person 4 (Clinical Pod)
**Your Folder:** `pods/clinical/`
- `agent.py` - Clinical pod agent (already created)
- `tools.py` - Add your tools here

**Your Tasks:**
1. Explore BigQuery tables (30 min)
2. Test `query_care_gaps()` (1 hour)
3. Optional: HEDIS search (skip if < 4 hours left)

---

## Person 5 (Compliance Pod + Demo)
**Your Folder:** `pods/compliance/`
- `agent.py` - Compliance pod agent (already created)
- `tools.py` - Add your tools here
- `config/cms_thresholds.py` - UPDATE THIS FILE

**Your Tasks:**
1. Update CMS thresholds in `config/cms_thresholds.py` (30 min)
2. Test `cross_check_citations()` (1 hour)
3. Set up demo environment (1 hour)
4. Help with testing & bug fixes

---

## Communication
- Post updates every 30 minutes in your channel
- Report blockers in #bugs
- Person 1 coordinates integration at hours 2, 3, 4
EOF

echo ""
echo "================================"
echo "✅ Pod Structure Complete!"
echo ""
echo "📁 Created:"
echo "   pods/performance/ (Person 2)"
echo "   pods/engagement/  (Person 3)"
echo "   pods/clinical/    (Person 4)"
echo "   pods/compliance/  (Person 5)"
echo "   agents/router.py  (Person 1)"
echo "   agents/synthesizer.py (Person 1)"
echo "   main.py (Person 1)"
echo "   config/cms_thresholds.py (Person 5)"
echo ""
echo "📋 Read TEAM_ASSIGNMENTS.md for next steps"
echo "================================"

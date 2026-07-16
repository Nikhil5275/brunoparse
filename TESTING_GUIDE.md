# Testing Guide - Working in Parallel

## 🎯 Two-Tier Testing Strategy

We have **two types of tests** so you can work efficiently:

1. **Quick Smoke Tests** (`test_pod.py`) - Fast integration testing
2. **Detailed Unit Tests** (in each pod folder) - Thorough tool testing

### When to Use Which?

| Scenario | Use This |
|----------|----------|
| "Does my pod work at all?" | Quick smoke test (`smoke_test.py`) |
| "Is my tool returning correct data?" | Detailed unit test (in your pod folder) |
| "Testing after integration" | Quick smoke test |
| "Debugging a specific function" | Detailed unit test |
| "Person 1 checking all pods" | Quick smoke test |

---

## 🧪 Method 1: Quick Smoke Tests (Everyone)

### Fast Pod Testing with `smoke_test.py`

**Test any pod quickly WITHOUT waiting for Person 1's integration:**

```bash
# Activate environment
source venv/bin/activate

# Test a pod
python smoke_test.py <pod_name> "your test query"
```

### Examples by Person:

**Person 2 (Performance):**
```bash
python smoke_test.py performance "What is our CBP rate for contract H1234?"
python smoke_test.py performance "Calculate gap to 4 stars for diabetes"
```

**Person 3 (Engagement):**
```bash
python smoke_test.py engagement "Which age groups have lowest compliance?"
python smoke_test.py engagement "Show me past intervention results for CBP"
```

**Person 4 (Clinical):**
```bash
python smoke_test.py clinical "How many open care gaps for diabetes?"
python smoke_test.py clinical "Show priority members for CBP"
```

**Person 5 (Compliance):**
```bash
python smoke_test.py compliance "Check this: Our rate is 65% [Source: stars_performance]"
python smoke_test.py compliance "Validate this: Member M1234567 needs outreach"
```

---

## 🔬 Method 2: Detailed Unit Tests (Per Person)

### Test Your Tools Individually (Recommended for Development)

Each pod has its own test file for **detailed debugging**:

**Person 2 (Performance Pod):**
```bash
python pods/performance/test_performance.py
```
- Tests `query_stars_performance()` with multiple measures
- Tests `compute_star_gap()` with different scenarios
- Tests edge cases (invalid data, missing tables, etc.)

**Person 3 (Engagement Pod):**
```bash
python pods/engagement/test_engagement.py
```
- Tests `query_member_segments()` with different dimensions
- Tests `search_intervention_history()` for past campaigns
- Validates segmentation logic

**Person 4 (Clinical Pod):**
```bash
python pods/clinical/test_clinical.py
```
- Tests `query_care_gaps()` with different measures
- Validates gap prioritization logic
- Tests member filtering

**Person 5 (Compliance Pod):**
```bash
python pods/compliance/test_compliance.py
```
- Tests `cross_check_citations()` with good/bad examples
- Tests `scan_for_pii()` detection
- Validates compliance rules

### Benefits of Detailed Tests:
✅ **Test tools in isolation** - No agent overhead  
✅ **Better error messages** - See exactly which tool fails  
✅ **Test edge cases** - Invalid data, missing tables, etc.  
✅ **Faster debugging** - No need to run full agent  
✅ **No merge conflicts** - You own your test file

### Customize Your Tests

Edit your pod's test file to add more cases:

```python
# Example: Add to pods/performance/test_performance.py
def test_multiple_contracts():
    """Test querying different contracts"""
    for contract in ["H1234", "H5678", "H9999"]:
        result = query_stars_performance("CBP", contract, 2025)
        print(f"Contract {contract}: {result}")
```

---

## 🚀 Full System Testing (After Integration)

### Once Person 1 Completes Integration

**Start the full system with web UI:**

```bash
# Make executable (one time)
chmod +x start.sh

# Launch the system
./start.sh
```

**Or run directly:**
```bash
source venv/bin/activate
adk web main.py
```

This opens: `http://localhost:8000`

### Test End-to-End Queries

Try these 5 hero queries in the web UI:

1. **"What's our current CBP rate?"**  
   → Routes to Performance Pod

2. **"Which member segments have the lowest diabetes control rates?"**  
   → Routes to Engagement Pod

3. **"How many open care gaps do we have for colorectal cancer screening?"**  
   → Routes to Clinical Pod

4. **"What's our gap to achieving 4 stars for blood pressure control?"**  
   → Routes to Performance Pod + Compliance validation

5. **"Show me past intervention results for breast cancer screening and segment the at-risk population by age"**  
   → Routes to Engagement Pod (multiple tools)

---

## 🐛 Debugging Tips

### My Pod Test Fails

**Check:**
1. Is BigQuery connection working? `python test_connection.py`
2. Do your tables exist? Run SQL queries in BigQuery console
3. Are table/column names correct? `SELECT * FROM table LIMIT 1`
4. Any typos in `PROJECT_ID` or `BQ_DATASET` in `.env`?

### Import Errors

```bash
# Missing package?
pip install google-adk google-cloud-bigquery

# Can't find your pod?
# Make sure __init__.py exists:
touch pods/performance/__init__.py
```

### SQL Errors

**Common issues:**
- Column name wrong → Check with `DESCRIBE table`
- Table not found → Verify `BQ_DATASET` in `.env`
- Syntax error → Test query in BigQuery console first

### Agent Not Calling Tools

**Check:**
- Are tools imported in `agent.py`?
- Are tools added to `tools=[]` list?
- Does tool function have proper docstring?

---

## ⏱️ Testing Checkpoints

### Hour 1: Environment Setup
- [ ] All team members: `setup.sh` and `setup_pods.sh` run successfully
- [ ] `python test_connection.py` passes
- [ ] Can see BigQuery tables
- [ ] `.env` configured with correct project ID and dataset

### Hour 2: Individual Pod Tests (Detailed Unit Tests)
- [ ] Person 2: `python pods/performance/test_performance.py` passes
- [ ] Person 3: `python pods/engagement/test_engagement.py` passes
- [ ] Person 4: `python pods/clinical/test_clinical.py` passes
- [ ] Person 5: `python pods/compliance/test_compliance.py` passes

### Hour 3: Pod Integration Tests (Quick Smoke Tests)
- [ ] Person 1: Router can route queries to pods
- [ ] All pods pass: `python smoke_test.py <pod_name> "test query"`
- [ ] At least 1 end-to-end query works
- [ ] Citations appear in output

### Hour 4: Full System Test
- [ ] `./start.sh` launches successfully
- [ ] All 5 hero queries work in web UI
- [ ] No errors in logs
- [ ] Compliance validation running

### Hour 5: Demo Prep
- [ ] Team rehearses demo script
- [ ] Screenshots taken (optional)
- [ ] Known bugs documented
- [ ] Celebration time! 🎉

---

## 📊 Quick Schema Exploration

**Run these in BigQuery Console or Python:**

```python
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

# List all tables
tables = client.list_tables(BQ_DATASET)
for table in tables:
    print(table.table_id)

# Get schema for a table
table = client.get_table(f"{PROJECT_ID}.{BQ_DATASET}.stars_performance")
for field in table.schema:
    print(f"{field.name}: {field.field_type}")

# Sample data
query = f"SELECT * FROM `{PROJECT_ID}.{BQ_DATASET}.stars_performance` LIMIT 5"
df = client.query(query).to_dataframe()
print(df)
```

---

## 🆘 Get Help

**In your team channel, post:**
- What command you ran
- Full error message
- What you expected vs what happened

**Common fixes:**
- `ModuleNotFoundError` → `pip install <package>`
- `PermissionDenied` → Check GCP permissions
- `TableNotFound` → Verify `BQ_DATASET` in `.env`
- `SyntaxError in SQL` → Test query in BigQuery console first
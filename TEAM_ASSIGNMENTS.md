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

# STARs RAG Agent - Architecture

## Google ADK Architecture

### Agent Hierarchy

```
User (ADK UI)
    ↓
ROOT AGENT (STARsRAGAgent)
    ↓
    ├─→ Router Agent (routes query)
    ↓
    ├─→ PARALLEL POD EXECUTION
    │   ├─→ Performance Pod
    │   ├─→ Engagement Pod  
    │   └─→ Clinical Pod
    ↓
    ├─→ Synthesizer Agent (merges outputs)
    ↓
    └─→ Compliance Pod (validates)
```

## Files Overview

### Entry Points

- **`app.py`** - ADK entry point, exports root_agent
- **`start.sh`** - Launch script for ADK web UI

### Agents (Person 1)

- **`agents/root_agent.py`** - Main orchestrator agent (users chat with this)
  - Manages entire workflow
  - Calls pods in PARALLEL
  - Has `orchestrate_query()` tool

- **`agents/router.py`** - Routes queries to appropriate pods
  - Model: gemini-2.0-flash (fast classification)
  - Returns JSON with pod list

- **`agents/synthesizer.py`** - Merges pod outputs
  - Model: gemini-2.5-pro (complex reasoning)
  - Creates coherent narrative with citations

### Pods (Person 2, 3, 4, 5)

- **`pods/performance/`** - Performance metrics (Person 2)
- **`pods/engagement/`** - Member segmentation (Person 3)
- **`pods/clinical/`** - Care gaps (Person 4)
- **`pods/compliance/`** - Validation (Person 5)

## How It Works

### 1. User asks question in ADK UI
```
User: "What's our CBP rate and which age groups need outreach?"
```

### 2. Root Agent orchestrates
- Calls Router Agent
- Router returns: `["Performance", "Engagement", "Compliance"]`

### 3. Pods run IN PARALLEL
```python
# All pods execute simultaneously
asyncio.gather(
    performance_pod.run(query),
    engagement_pod.run(query)
)
```

**Why parallel?**
- ✅ Faster response (3 pods in ~5 sec instead of 15 sec sequential)
- ✅ Better user experience
- ✅ More efficient resource usage

### 4. Synthesizer merges outputs
```
Input:
  - Performance: "CBP rate is 65.2% [Source: ...]"
  - Engagement: "Age 65-74 lowest at 58% [Source: ...]"

Output:
  "Our CBP rate of 65.2% is 8.0 points below 4-star threshold.
   Members aged 65-74 show lowest compliance and should be targeted..."
```

### 5. Compliance validates
- Checks for citations
- Scans for PII
- Returns APPROVED or flags issues

### 6. User gets final response

## Running the Agent

### Launch ADK Web UI
```bash
./start.sh
# Opens http://localhost:8000
```

### In ADK UI
1. Select "STARsRAGAgent" from dropdown
2. Ask questions in chat
3. Root agent orchestrates everything automatically

### CLI Testing
```bash
python -c "from agents.root_agent import root_agent; \
result = root_agent.run('What is our CBP rate?'); \
print(result.output)"
```

## Key Design Decisions

### Why Root Agent + Orchestrator Pattern?
- ADK requires an agent to select in UI
- Root agent manages complexity, user just asks questions
- Clean separation: routing, execution, synthesis, validation

### Why Parallel Pod Execution?
- **Sequential (OLD):** 3 pods × 5 sec each = 15 sec total
- **Parallel (NEW):** 3 pods in parallel = ~5 sec total
- 3x faster response time!

### Why Different Models?
- **Router (Flash):** Simple classification, cheap, fast
- **Synthesizer (Pro):** Complex reasoning, quality matters
- **Root (Pro):** Main user-facing agent, quality matters
- Optimizes cost while maintaining quality

## Testing

See `TESTING_GUIDE.md` for:
- Individual pod testing
- Integration testing
- End-to-end testing

## Team Coordination

- **Person 1 (You):** Root agent, router, synthesizer, orchestration
- **Person 2-4:** Build pods independently
- **Person 5:** Compliance + demo setup

Everyone works in parallel, no merge conflicts!
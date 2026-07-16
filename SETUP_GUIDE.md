# STARs RAG Agent - Setup Guide

## ✅ Setup Complete!

You now have:
- ✓ Project structure created
- ✓ Python dependencies installed
- ✓ Configuration templates ready

## 🔧 Next Steps (REQUIRED)

### 1. Configure GCP Credentials

Edit `.env` file:
```bash
GOOGLE_CLOUD_PROJECT=your-actual-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
BQ_DATASET=your_dataset_name
```

### 2. Verify Connection

```bash
# Activate venv (if not already active)
source venv/bin/activate

# Test BigQuery connection
python test_connection.py
```

You should see: `✅ BigQuery connection successful!`

### 3. Find Your Tables

Run this to discover your BigQuery tables:

```bash
python << 'PYEOF'
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

client = bigquery.Client(project=PROJECT_ID)

tables = client.list_tables(BQ_DATASET)
print(f"\n📊 Tables in {BQ_DATASET}:")
for table in tables:
    print(f"  - {table.table_id}")
PYEOF
```

## 📋 Team Role Checkpoints

### Person 1 (Router/Synthesizer)
- [ ] All setup steps above ✓
- [ ] Can import `from google.adk import Agent`
- [ ] Ready to build orchestration layer

### Person 2 (Performance Pod)
- [ ] All setup steps above ✓
- [ ] Run: `SELECT * FROM stars_performance LIMIT 5` in BigQuery
- [ ] Document table schema in `config/schemas.md`

### Person 3 (Engagement Pod)
- [ ] All setup steps above ✓
- [ ] Run: `SELECT * FROM segment_performance LIMIT 5`
- [ ] Run: `SELECT * FROM historical_interventions LIMIT 5`

### Person 4 (Clinical Pod)
- [ ] All setup steps above ✓
- [ ] Run: `SELECT * FROM care_gaps LIMIT 5`

### Person 5 (Compliance/Demo)
- [ ] All setup steps above ✓
- [ ] Create CMS thresholds (see TEAM_TASK_SPLIT.md)

## 🆘 Troubleshooting

### "Module not found: google.adk"
```bash
pip install --upgrade google-adk
```

### "Permission denied" errors
Make sure your service account has:
- BigQuery Data Viewer
- BigQuery Job User

### "Table not found"
Check that `BQ_DATASET` in `.env` matches your actual dataset name.

## 🎯 Ready to Start?

1. ✅ `test_connection.py` passes
2. ✅ You can see your BigQuery tables
3. ✅ You know your role (Person 1-5)

→ Go to `TEAM_TASK_SPLIT.md` and find your section!

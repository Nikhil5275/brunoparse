#!/bin/bash

# STARs RAG Agent - Team Setup Script
# Run this ONCE before starting your individual work

set -e  # Exit on error

echo "🚀 STARs RAG Agent - Team Setup"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"

# Create project structure
echo ""
echo "✓ Creating project structure..."
mkdir -p agents
mkdir -p tools
mkdir -p config
mkdir -p features
mkdir -p tests
mkdir -p .adk
echo "  ✓ agents/"
echo "  ✓ tools/"
echo "  ✓ config/"
echo "  ✓ features/"
echo "  ✓ tests/"

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Created venv/"
else
    echo "  venv/ already exists, skipping"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "✓ Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env template
echo ""
echo "✓ Creating .env template..."
cat > .env.template << 'EOF'
# GCP Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# BigQuery Dataset
BQ_DATASET=your_dataset_name

# Optional: Anthropic API key
ANTHROPIC_API_KEY=your-key-here
EOF

if [ ! -f ".env" ]; then
    cp .env.template .env
    echo "  Created .env (UPDATE THIS WITH YOUR VALUES!)"
else
    echo "  .env already exists, skipping"
fi

# Create empty __init__.py files
echo ""
echo "✓ Creating Python package files..."
touch agents/__init__.py
touch tools/__init__.py
touch config/__init__.py
touch features/__init__.py
touch tests/__init__.py

# Create basic config file
echo ""
echo "✓ Creating config/settings.py..."
cat > config/settings.py << 'EOF'
"""Global configuration for STARs RAG Agent"""
import os
from dotenv import load_dotenv

load_dotenv()

# GCP Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
BQ_DATASET = os.getenv("BQ_DATASET", "stars_data")

# Contract defaults
DEFAULT_CONTRACT = "H1234"
DEFAULT_YEAR = 2025

# Model configuration
ROUTER_MODEL = "gemini-2.0-flash"
POD_MODEL = "gemini-2.5-pro"
SYNTHESIZER_MODEL = "gemini-2.5-pro"
EOF

# Create test query script
echo ""
echo "✓ Creating test_connection.py..."
cat > test_connection.py << 'EOF'
"""Quick test to verify GCP/BigQuery connection"""
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET

def test_connection():
    """Test BigQuery connection"""
    try:
        client = bigquery.Client(project=PROJECT_ID)

        # Try a simple query
        query = "SELECT 1 as test"
        result = client.query(query).result()

        print("✅ BigQuery connection successful!")
        print(f"   Project: {PROJECT_ID}")
        return True

    except Exception as e:
        print(f"❌ BigQuery connection failed: {e}")
        print("\nCheck:")
        print("1. GOOGLE_APPLICATION_CREDENTIALS is set correctly")
        print("2. GOOGLE_CLOUD_PROJECT matches your GCP project")
        print("3. Service account has BigQuery permissions")
        return False

if __name__ == "__main__":
    test_connection()
EOF

# Create README for team
echo ""
echo "✓ Creating SETUP_GUIDE.md..."
cat > SETUP_GUIDE.md << 'EOF'
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
EOF

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo ""
echo "📝 NEXT STEPS:"
echo "   1. Edit .env with your GCP credentials"
echo "   2. Run: source venv/bin/activate"
echo "   3. Run: python test_connection.py"
echo "   4. Read: SETUP_GUIDE.md"
echo ""
echo "👥 Share this with your team:"
echo "   Everyone runs: bash setup_team.sh"
echo ""
echo "================================"

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

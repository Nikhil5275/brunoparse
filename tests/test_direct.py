"""Direct test of the orchestration - bypasses ADK UI"""
from agents.agent import orchestrate_query

# Test query
query = "What's our CBP rate for 2026?"

print("\n" + "="*60)
print("TESTING STARs RAG AGENT")
print("="*60)
print(f"Query: {query}\n")

try:
    result = orchestrate_query(query)
    
    print("\n" + "="*60)
    print("SUCCESS! FINAL RESPONSE:")
    print("="*60)
    print(result)
    print("\n" + "="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

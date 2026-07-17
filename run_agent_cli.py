"""Interactive CLI for STARs RAG Agent - Shows agent execution in real-time"""
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.agent import root_agent
import os

# Ensure Vertex AI is used
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'qwiklabs-gcp-00-43ecffa89f51'

print("\n" + "="*70)
print("🏥 STARs RAG Agent - Interactive CLI")
print("="*70)
print("\nMulti-Pod Agentic System for HEDIS/STARs Analysis")
print("\nAvailable Pods:")
print("  • PerformancePod - Rates, star ratings, gaps, benchmarks")
print("  • EngagementPod - Member segmentation, interventions")
print("  • ClinicalPod - Care gaps, HEDIS specs")
print("  • CompliancePod - Citation validation, PII checks")
print("\n" + "="*70)

# Initialize runner
print("\nInitializing agent runner...")
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="agents",
    session_service=session_service,
    auto_create_session=True
)
print("✅ Ready!\n")

# Main loop
session_counter = 0

while True:
    print("\n" + "-"*70)
    query = input("\n💬 Your question (or 'quit' to exit): ").strip()
    
    if query.lower() in ['quit', 'exit', 'q']:
        print("\n👋 Goodbye!\n")
        break
    
    if not query:
        print("⚠️  Please enter a question.")
        continue
    
    print("\n" + "="*70)
    print(f"Query: {query}")
    print("="*70)
    
    try:
        # Create message
        message = types.Content(role="user", parts=[types.Part(text=query)])
        
        # Run agent
        print("\n🤖 Starting agent workflow...\n")
        
        events = runner.run(
            user_id="cli_user",
            session_id=f"session_{session_counter}",
            new_message=message
        )
        
        session_counter += 1
        
        # Process events in real-time
        current_agent = None
        response_text = ""
        
        for event in events:
            # Track which agent is running
            if hasattr(event, 'author') and event.author:
                if event.author != current_agent:
                    current_agent = event.author
                    print(f"➜ Agent active: {current_agent}")
            
            # Show function calls (tool executions)
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        func_call = part.function_call
                        print(f"  🔧 Calling tool: {func_call.name}({func_call.args})")
                    
                    if hasattr(part, 'function_response') and part.function_response:
                        func_resp = part.function_response
                        if func_resp.name:
                            print(f"  ✅ Tool completed: {func_resp.name}")
                    
                    # Capture final text response
                    if hasattr(part, 'text') and part.text:
                        response_text = part.text
        
        # Display final response
        print("\n" + "="*70)
        print("📋 FINAL RESPONSE:")
        print("="*70)
        print()
        print(response_text if response_text else "No response generated")
        print()
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry a simpler query like: 'What is our CBP rate?'")

print()

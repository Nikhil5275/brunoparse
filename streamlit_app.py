"""Simple Streamlit UI for STARs RAG Agent"""
import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.agent import root_agent
import os
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'qwiklabs-gcp-00-43ecffa89f51'

st.set_page_config(page_title="STARs RAG Agent", page_icon="🏥")

@st.cache_resource
def get_runner():
    session_service = InMemorySessionService()
    return Runner(
        agent=root_agent,
        app_name="agents",
        session_service=session_service,
        auto_create_session=True
    )
runner = get_runner()

st.title("🏥 STARs RAG Agent")
st.write("Ask questions about HEDIS/STARs performance")

query = st.text_area("Your question:", height=100)

if st.button("Ask Agent"):
    if query.strip():
        with st.spinner("Agent is working..."):
            try:
                message = types.Content(role="user", parts=[types.Part(text=query)])
                events = runner.run(
                    user_id="user",
                    session_id=f"session_{hash(query) % 1000}",
                    new_message=message
                )
                
                response = ""
                for event in events:
                    if hasattr(event, 'content') and event.content:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response = part.text
                
                if response:
                    st.success("Response:")
                    st.write(response)
                else:
                    st.warning("No response generated")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question")

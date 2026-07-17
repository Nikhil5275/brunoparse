"""Simple Flask Web UI for STARs RAG Agent"""
from flask import Flask, render_template, request, jsonify
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.agent import root_agent
import os

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'qwiklabs-gcp-00-43ecffa89f51'

app = Flask(__name__)

# Initialize runner
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="agents",
    session_service=session_service,
    auto_create_session=True
)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bruno STARs RAG Agent</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background: #5BA908;
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        .header {
            background: #00843D;
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { 
            font-size: 2.2em; 
            margin-bottom: 10px; 
            font-weight: 700;
        }
        .header p { 
            opacity: 0.95; 
            font-size: 1.15em; 
            font-weight: 400;
        }
        .content { padding: 40px; }
        textarea { 
            width: 100%; 
            padding: 16px; 
            border: 2px solid #d0d0d0;
            border-radius: 6px;
            font-size: 17px;
            font-family: inherit;
            resize: vertical;
            min-height: 130px;
            color: #1a1a1a;
            line-height: 1.5;
        }
        textarea:focus {
            outline: none;
            border-color: #00843D;
            box-shadow: 0 0 0 3px rgba(0, 132, 61, 0.1);
        }
        button {
            width: 100%;
            padding: 16px;
            margin-top: 20px;
            background: #00843D;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #006b32; }
        button:disabled { 
            opacity: 0.6; 
            cursor: not-allowed;
        }
        .examples {
            margin-top: 25px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }
        .examples h3 { 
            margin-bottom: 15px; 
            color: #1a1a1a;
            font-size: 1.1em;
            font-weight: 700;
        }
        .example {
            padding: 12px 16px;
            margin: 10px 0;
            background: white;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            color: #1a1a1a;
            font-size: 15px;
            line-height: 1.4;
        }
        .example:hover {
            background: #00843D;
            color: white;
            border-color: #00843D;
        }
        .response-area {
            margin-top: 30px;
            display: none;
        }
        .response-header {
            padding: 16px 20px;
            background: #00843D;
            color: white;
            font-weight: 700;
            font-size: 1.1em;
        }
        .response-content {
            padding: 25px;
            background: white;
            border: 1px solid #d0d0d0;
            min-height: 100px;
            line-height: 1.7;
            white-space: pre-wrap;
            color: #1a1a1a;
            font-size: 16px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #333;
            font-size: 16px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #00843D;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .agent-flow {
            padding: 12px 16px;
            margin-bottom: 15px;
            background: #e8f5e9;
            border-left: 4px solid #00843D;
            font-family: monospace;
            font-size: 15px;
            color: #1a1a1a;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Bruno STARs RAG Agent</h1>
            <p>Multi-Pod Agentic System for HEDIS/STARs Performance Analysis</p>
        </div>
        
        <div class="content">
            <textarea id="query" placeholder="Ask about performance rates, member segments, interventions, or care gaps..."></textarea>
            <button onclick="askAgent()" id="askBtn">Ask Agent</button>
            
            <div class="examples">
                <h3>Example Questions:</h3>
                <div class="example" onclick="setQuery(this.innerText)">What is our CBP rate for 2026?</div>
                <div class="example" onclick="setQuery(this.innerText)">Which member segments have the lowest blood pressure compliance?</div>
                <div class="example" onclick="setQuery(this.innerText)">What are our care gaps for blood pressure and how can we resolve them?</div>
                <div class="example" onclick="setQuery(this.innerText)">What interventions worked best for blood pressure last year?</div>
            </div>
            
            <div class="response-area" id="responseArea">
                <div class="response-header">Agent Response</div>
                <div class="response-content" id="responseContent"></div>
            </div>
        </div>
    </div>
    
    <script>
        function setQuery(text) {
            document.getElementById('query').value = text;
        }
        
        function askAgent() {
            const query = document.getElementById('query').value.trim();
            const btn = document.getElementById('askBtn');
            const responseArea = document.getElementById('responseArea');
            const responseContent = document.getElementById('responseContent');
            
            if (!query) {
                alert('Please enter a question');
                return;
            }
            
            btn.disabled = true;
            btn.innerText = 'Processing...';
            responseArea.style.display = 'block';
            responseContent.innerHTML = '<div class="loading"><div class="spinner"></div>Agent is processing your query...</div>';
            
            fetch('/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: query})
            })
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    responseContent.innerHTML = '<span style="color: #d32f2f; font-weight: 600;">Error: ' + data.error + '</span>';
                } else {
                    let html = '';
                    if (data.agents) {
                        html += '<div class="agent-flow">Agent Flow: ' + data.agents + '</div>';
                    }
                    html += data.response;
                    responseContent.innerHTML = html;
                }
                btn.disabled = false;
                btn.innerText = 'Ask Agent';
            })
            .catch(err => {
                responseContent.innerHTML = '<span style="color: #d32f2f; font-weight: 600;">Error: ' + err + '</span>';
                btn.disabled = false;
                btn.innerText = 'Ask Agent';
            });
        }
        
        document.getElementById('query').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                askAgent();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Run agent
        message = types.Content(role="user", parts=[types.Part(text=user_query)])
        events = runner.run(
            user_id="web_user",
            session_id=f"web_{hash(user_query) % 100000}",
            new_message=message
        )
        
        # Collect response and agents
        response_text = ""
        agents = []
        for event in events:
            if hasattr(event, 'author') and event.author and event.author not in agents:
                agents.append(event.author)
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text = part.text
        
        return jsonify({
            'response': response_text if response_text else "No response generated",
            'agents': " → ".join(agents) if agents else None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Bruno STARs RAG Agent Web UI")
    print("="*60)
    print("\nStarting on port 8080...")
    print("Access via Cloud Shell Web Preview")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=8080, debug=False)

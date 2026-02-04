# 🌐 Zizo - Advanced AI Assistant
# Deployed Web Application

from flask import Flask, render_template_string, request, jsonify, session
from autoagent import MetaChain, Agent
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# إعدادات AI
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
client = MetaChain(log_path=None)

# إنشاء AI Agent
ai_agent = Agent(
    name="زيزو",
    model=AI_MODEL,
    instructions="""أنا زيزو 🤖، مساعدك الذكي السريع!

قدراتي:
- الإجابة على الأسئلة
- كتابة الأكواد
- المساعدة في البرمجة
- شرح المفاهيم
- الترجمة
- الكتابة الإبداعية

أتحدث العربية والإنجليزية. دائماً في خدمتك! 😊""",
    functions=[]
)

# HTML Template المحسّن
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>زيزو - Zizo AI Assistant</title>
    <meta name="description" content="زيزو - مساعد ذكاء اصطناعي متقدم">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            color: white;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 { font-size: 1.8em; margin-bottom: 5px; }
        .header p { opacity: 0.9; font-size: 0.9em; }
        
        .container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 900px;
            width: 100%;
            margin: 20px auto;
            padding: 0 20px;
        }
        
        .chat-box {
            background: white;
            border-radius: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .message {
            padding: 12px 18px;
            border-radius: 15px;
            max-width: 75%;
            animation: slideIn 0.3s;
            word-wrap: break-word;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user { background: #667eea; color: white; align-self: flex-end; }
        .ai { background: #f0f0f0; color: #333; align-self: flex-start; }
        
        .input-area {
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #ddd;
            display: flex;
            gap: 10px;
        }
        
        #userInput {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 1em;
            outline: none;
            transition: border 0.3s;
        }
        
        #userInput:focus { border-color: #667eea; }
        
        #sendBtn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        #sendBtn:hover { transform: scale(1.05); }
        #sendBtn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .loading {
            display: none;
            text-align: center;
            padding: 10px;
            color: #667eea;
        }
        
        .loading.active { display: block; }
        
        .footer {
            text-align: center;
            color: white;
            padding: 15px;
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .stats {
            background: rgba(255,255,255,0.1);
            padding: 10px;
            text-align: center;
            color: white;
            font-size: 0.85em;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 1.5em; }
            .message { max-width: 85%; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 زيزو - Zizo</h1>
        <p>مساعد ذكاء اصطناعي متقدم | Advanced AI Assistant</p>
    </div>
    
    <div class="container">
        <div class="chat-box">
            <div class="messages" id="messages">
                <div class="message ai">
                    مرحباً! 👋 أنا زيزو، مساعدك الذكي.<br>
                    اسألني عن أي شيء: برمجة، شرح مفاهيم، كتابة محتوى، أو أي شيء تريد! 😊
                </div>
            </div>
            
            <div class="loading" id="loading">
                ⏳ زيزو يفكر...
            </div>
            
            <div class="input-area">
                <input 
                    type="text" 
                    id="userInput" 
                    placeholder="اكتب رسالتك هنا..."
                    onkeypress="if(event.key==='Enter') sendMessage()"
                    autofocus
                >
                <button id="sendBtn" onclick="sendMessage()">إرسال</button>
            </div>
        </div>
        
        <div class="stats">
            النموذج: {{ model }} | الاستجابة: فورية ⚡ | مفتوح المصدر 💚
        </div>
    </div>
    
    <div class="footer">
        صُنع بـ ❤️ باستخدام AutoAgent | Open Source
    </div>

    <script>
        let conversationHistory = [];
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage(message, 'user');
            input.value = '';
            input.disabled = true;
            document.getElementById('sendBtn').disabled = true;
            document.getElementById('loading').classList.add('active');
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ 
                        message: message,
                        history: conversationHistory 
                    })
                });
                
                const data = await response.json();
                
                if (data.response) {
                    addMessage(data.response, 'ai');
                    conversationHistory = data.history || conversationHistory;
                } else {
                    addMessage('❌ عذراً، حدث خطأ. حاول مرة أخرى.', 'ai');
                }
                
            } catch (error) {
                addMessage('❌ خطأ في الاتصال. تأكد من الإنترنت.', 'ai');
            } finally {
                input.disabled = false;
                document.getElementById('sendBtn').disabled = false;
                document.getElementById('loading').classList.remove('active');
                input.focus();
            }
        }
        
        function addMessage(text, type) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Auto-focus on load
        document.getElementById('userInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template_string(HTML, model=AI_MODEL)

@app.route('/chat', methods=['POST'])
def chat():
    """معالجة الرسائل"""
    try:
        data = request.json
        user_message = data.get('message', '')
        history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'رسالة فارغة'}), 400
        
        # إضافة رسالة المستخدم
        history.append({"role": "user", "content": user_message})
        
        # الحصول على رد AI
        response = client.run(
            ai_agent,
            history,
            context_variables={},
            debug=False,
            max_turns=1
        )
        
        ai_response = response.messages[-1]['content']
        
        # إضافة رد AI للسجل
        history.append({"role": "assistant", "content": ai_response})
        
        # الاحتفاظ بآخر 10 رسائل فقط (للذاكرة)
        if len(history) > 20:
            history = history[-20:]
        
        return jsonify({
            'response': ai_response,
            'history': history,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    """فحص صحة التطبيق"""
    return jsonify({
        'status': 'healthy',
        'app': 'Zizo AI Assistant',
        'model': AI_MODEL,
        'version': '2.0.0'
    })

@app.route('/about')
def about():
    """معلومات عن التطبيق"""
    return jsonify({
        'name': 'زيزو - Zizo',
        'description': 'مساعد ذكاء اصطناعي متقدم',
        'capabilities': [
            'المحادثة الذكية',
            'البرمجة والأكواد',
            'شرح المفاهيم',
            'الكتابة الإبداعية',
            'الترجمة',
            'المساعدة في البحث'
        ],
        'languages': ['العربية', 'English'],
        'version': '2.0.0',
        'open_source': True,
        'github': 'https://github.com/aboday2067-dot/sudan'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

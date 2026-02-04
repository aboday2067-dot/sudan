#!/usr/bin/env python3
"""
زيزو - تطبيق AI ويب خفيف وسريع جداً
Zizo - Ultra-light & Fast AI Web App
"""

from flask import Flask, render_template_string, request, jsonify
from autoagent import MetaChain, Agent
import os

app = Flask(__name__)

# إعدادات AI
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
client = MetaChain(log_path=None)

# إنشاء AI Agent مرة واحدة فقط (للسرعة)
ai_agent = Agent(
    name="زيزو",
    model=AI_MODEL,
    instructions="""أنا زيزو 🤖، مساعدك الذكي السريع!

- أجيب بوضوح ودقة
- أكون مختصراً وسريعاً
- أستخدم نفس لغة سؤالك (عربي/إنجليزي)
- دائماً في خدمتك! 😊""",
    functions=[]
)

# HTML Template - خفيف جداً
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تطبيق AI سريع</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 0.9em;
        }
        
        .chat-container {
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
            min-height: 200px;
        }
        
        .message {
            margin: 15px 0;
            padding: 12px 18px;
            border-radius: 15px;
            max-width: 80%;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: #f0f0f0;
            color: #333;
        }
        
        .input-container {
            padding: 20px;
            border-top: 1px solid #eee;
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
        
        #userInput:focus {
            border-color: #667eea;
        }
        
        #sendBtn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        #sendBtn:hover {
            transform: scale(1.05);
        }
        
        #sendBtn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 10px;
            color: #667eea;
        }
        
        .loading.active {
            display: block;
        }
        
        .stats {
            padding: 10px 20px;
            background: #f8f9fa;
            text-align: center;
            font-size: 0.85em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 تطبيق AI سريع</h1>
            <p>مساعد ذكي خفيف وسريع جداً</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message ai-message">
                مرحباً! 👋 أنا زيزو، مساعدك الذكي. اسألني أي شيء!
            </div>
        </div>
        
        <div class="loading" id="loading">
            ⏳ جاري التفكير...
        </div>
        
        <div class="input-container">
            <input 
                type="text" 
                id="userInput" 
                placeholder="اكتب سؤالك هنا..."
                onkeypress="if(event.key=='Enter') sendMessage()"
            >
            <button id="sendBtn" onclick="sendMessage()">إرسال</button>
        </div>
        
        <div class="stats">
            النموذج: {{ model }} | الاستجابة: سريعة جداً ⚡
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // إضافة رسالة المستخدم
            addMessage(message, 'user');
            input.value = '';
            
            // تعطيل الإدخال
            input.disabled = true;
            document.getElementById('sendBtn').disabled = true;
            document.getElementById('loading').classList.add('active');
            
            try {
                // إرسال إلى API
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // إضافة رد AI
                addMessage(data.response, 'ai');
                
            } catch (error) {
                addMessage('❌ عذراً، حدث خطأ. حاول مرة أخرى.', 'ai');
            } finally {
                // تفعيل الإدخال
                input.disabled = false;
                document.getElementById('sendBtn').disabled = false;
                document.getElementById('loading').classList.remove('active');
                input.focus();
            }
        }
        
        function addMessage(text, type) {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;
            messageDiv.textContent = text;
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template_string(HTML_TEMPLATE, model=AI_MODEL)

@app.route('/chat', methods=['POST'])
def chat():
    """معالجة رسائل AI"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'رسالة فارغة'}), 400
        
        # الحصول على رد AI
        messages = [{"role": "user", "content": user_message}]
        response = client.run(
            ai_agent,
            messages,
            context_variables={},
            debug=False,
            max_turns=1
        )
        
        ai_response = response.messages[-1]['content']
        
        return jsonify({
            'response': ai_response,
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
        'model': AI_MODEL,
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🤖 زيزو - تطبيق AI الويب يعمل الآن!")
    print("="*60)
    print(f"\n  📍 الرابط: http://localhost:5000")
    print(f"  🤖 النموذج: {AI_MODEL}")
    print(f"  💬 أنا زيزو، مساعدك الذكي!")
    print(f"\n  اضغط Ctrl+C للإيقاف\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

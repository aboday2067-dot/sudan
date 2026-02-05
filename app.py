# 🌐 Zizo - Advanced AI Assistant
# Deployed Web Application

from flask import Flask, render_template_string, request, jsonify, session
from autoagent import MetaChain, Agent
import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
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
            padding: 10px;
            background: #f8f9fa;
            border-top: 1px solid #ddd;
            display: flex;
            flex-direction: row;
            gap: 8px;
            align-items: stretch;
        }
        
        #userInput {
            flex: 1;
            padding: 10px 15px;
            border: 2px solid #ddd;
            border-radius: 20px;
            font-size: 0.95em;
            outline: none;
            transition: border 0.3s;
            min-width: 0;
        }
        
        #userInput:focus { border-color: #667eea; }
        
        #sendBtn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.95em;
            transition: transform 0.2s;
            white-space: nowrap;
            flex-shrink: 0;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
            user-select: none;
        }
        
        #sendBtn:hover { transform: scale(1.05); }
        #sendBtn:active { transform: scale(0.95); }
        #sendBtn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .pro-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.9em;
            transition: all 0.3s;
            white-space: nowrap;
            box-shadow: 0 2px 10px rgba(245, 87, 108, 0.3);
            flex-shrink: 0;
            order: -1;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
            user-select: none;
        }
        
        .pro-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.5);
        }
        
        .pro-btn:active {
            transform: translateY(0);
        }
        
        @media (max-width: 480px) {
            .input-area {
                padding: 8px;
                gap: 6px;
            }
            #userInput {
                padding: 8px 12px;
                font-size: 0.9em;
            }
            #sendBtn, .pro-btn {
                padding: 8px 15px;
                font-size: 0.85em;
            }
        }
        
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
                    onkeydown="if(event.key==='Enter'){event.preventDefault();sendMessage();}"
                >
                <button type="button" id="sendBtn" style="touch-action: manipulation;">إرسال</button>
                <button type="button" class="pro-btn" style="touch-action: manipulation;">PRO 🚀</button>
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
        console.log('✅ زيزو جاهز! Zizo Ready!');
        let conversationHistory = [];
        
        // ربط الأحداث مباشرة بعد تحميل DOM
        document.addEventListener('DOMContentLoaded', function() {
            console.log('📱 DOM جاهز Ready');
            
            const sendBtn = document.getElementById('sendBtn');
            const proBtn = document.querySelector('.pro-btn');
            const input = document.getElementById('userInput');
            
            console.log('زر الإرسال:', sendBtn ? '✅ موجود' : '❌ غير موجود');
            console.log('زر PRO:', proBtn ? '✅ موجود' : '❌ غير موجود');
            console.log('حقل الإدخال:', input ? '✅ موجود' : '❌ غير موجود');
            
            // ربط زر الإرسال
            if (sendBtn) {
                sendBtn.addEventListener('click', function(e) {
                    console.log('🖱️ تم الضغط على زر الإرسال!');
                    e.preventDefault();
                    sendMessage();
                });
                
                sendBtn.addEventListener('touchend', function(e) {
                    console.log('👆 تم لمس زر الإرسال!');
                    e.preventDefault();
                    sendMessage();
                });
            }
            
            // ربط زر PRO
            if (proBtn) {
                proBtn.addEventListener('click', function(e) {
                    console.log('🖱️ تم الضغط على زر PRO!');
                    e.preventDefault();
                    switchToPro();
                });
                
                proBtn.addEventListener('touchend', function(e) {
                    console.log('👆 تم لمس زر PRO!');
                    e.preventDefault();
                    switchToPro();
                });
            }
            
            // ربط Enter في حقل الإدخال
            if (input) {
                input.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        console.log('⌨️ تم الضغط على Enter!');
                        e.preventDefault();
                        sendMessage();
                    }
                });
                input.focus();
            }
        });
        
        async function sendMessage() {
            console.log('📤 بدء إرسال رسالة...');
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) {
                console.log('⚠️ رسالة فارغة');
                alert('⚠️ الرجاء كتابة رسالة أولاً!');
                return;
            }
            
            console.log('📝 الرسالة:', message);
            addMessage(message, 'user');
            input.value = '';
            input.disabled = true;
            document.getElementById('sendBtn').disabled = true;
            document.getElementById('loading').classList.add('active');
            
            try {
                console.log('🌐 إرسال طلب للخادم...');
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ 
                        message: message,
                        history: conversationHistory 
                    })
                });
                
                console.log('📥 استلام رد من الخادم...');
                const data = await response.json();
                console.log('✅ البيانات:', data);
                
                if (data.response) {
                    addMessage(data.response, 'ai');
                    conversationHistory = data.history || conversationHistory;
                } else {
                    addMessage('❌ عذراً، حدث خطأ. حاول مرة أخرى.', 'ai');
                }
                
            } catch (error) {
                console.error('❌ خطأ:', error);
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
        
        function switchToPro() {
            console.log('🚀 تشغيل وظيفة PRO...');
            const confirmed = confirm('🚀 هل تريد التبديل إلى زيزو برو؟\n\nستحصل على:\n✅ إنشاء الصور (DALL-E 3)\n✅ إنشاء الفيديوهات\n✅ برمجة متقدمة\n✅ دمج APIs\n✅ نشر التطبيقات\n✅ اكتشاف الأخطاء\n✅ نماذج AI مخصصة');
            
            console.log('🤔 الرد:', confirmed ? 'موافق' : 'إلغاء');
            
            if (confirmed) {
                console.log('✅ تم الموافقة - التوجيه إلى PRO');
                addMessage('🚀 جاري التبديل إلى زيزو برو...', 'ai');
                setTimeout(() => {
                    window.location.href = '/pro';
                }, 1000);
            } else {
                console.log('❌ تم الإلغاء');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template_string(HTML, model=AI_MODEL)

@app.route('/pro')
def pro():
    """صفحة زيزو برو - إعادة توجيه"""
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>التبديل إلى زيزو برو</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                text-align: center;
                padding: 20px;
            }
            .container {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                max-width: 600px;
            }
            h1 { font-size: 2.5em; margin-bottom: 20px; }
            p { font-size: 1.2em; margin: 15px 0; line-height: 1.6; }
            .features {
                text-align: right;
                margin: 30px 0;
                font-size: 1.1em;
            }
            .features div {
                margin: 10px 0;
                padding: 10px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            .btn {
                background: white;
                color: #f5576c;
                border: none;
                padding: 15px 40px;
                border-radius: 30px;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                margin: 10px;
                transition: transform 0.3s;
            }
            .btn:hover { transform: scale(1.05); }
            .back-btn {
                background: rgba(255,255,255,0.2);
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 زيزو برو</h1>
            <p>النسخة المتقدمة مع قدرات عبقرية!</p>
            
            <div class="features">
                <div>🎨 إنشاء الصور بجودة HD</div>
                <div>🎬 إنشاء الفيديوهات من النص</div>
                <div>💻 برمجة مواقع وتطبيقات كاملة</div>
                <div>🔌 دمج APIs والخدمات</div>
                <div>🚀 نشر على السيرفرات</div>
                <div>🐛 اكتشاف وإصلاح الأخطاء</div>
                <div>🤖 إنشاء نماذج AI مخصصة</div>
            </div>
            
            <p><strong>للتبديل إلى زيزو برو:</strong></p>
            <p>يرجى تشغيل الأمر التالي:</p>
            <p style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; font-family: monospace;">
                pkill -f "python.*app.py" && cd /home/user/webapp && ./start_zizo_pro.sh
            </p>
            
            <button class="btn back-btn" onclick="window.location.href='/'">← العودة لزيزو الأساسي</button>
        </div>
    </body>
    </html>
    """


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

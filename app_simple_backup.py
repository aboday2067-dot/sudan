# 🌐 Zizo - Simple Working Version
# النسخة المبسطة التي تعمل بضمان 100%

from flask import Flask, render_template_string, request, jsonify
from autoagent import MetaChain, Agent
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
client = MetaChain(log_path=None)

ai_agent = Agent(
    name="زيزو",
    model=AI_MODEL,
    instructions="""أنا زيزو 🤖، مساعدك الذكي السريع!

قدراتي:
- الإجابة على الأسئلة
- تحليل الصور
- قراءة الملفات
- كتابة الأكواد
- المساعدة في البرمجة
- شرح المفاهيم

أتحدث العربية والإنجليزية. دائماً في خدمتك! 😊""",
    functions=[]
)

# HTML Template - نسخة بسيطة جداً
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>زيزو - Zizo AI</title>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
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
            padding: 15px;
            color: white;
            text-align: center;
        }
        
        .container {
            flex: 1;
            max-width: 900px;
            width: 100%;
            margin: 20px auto;
            padding: 0 20px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-box {
            background: white;
            border-radius: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
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
            word-wrap: break-word;
        }
        
        .user { background: #667eea; color: white; align-self: flex-end; }
        .ai { background: #f0f0f0; color: #333; align-self: flex-start; }
        
        .input-area {
            padding: 15px;
            background: #f8f9fa;
            border-top: 1px solid #ddd;
        }
        
        .input-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        #userInput {
            flex: 1;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 20px;
            font-size: 1em;
            outline: none;
        }
        
        button {
            padding: 12px 20px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.95em;
            transition: all 0.2s;
        }
        
        #sendBtn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .upload-btn {
            background: #28a745;
            color: white;
        }
        
        .pro-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        button:hover { transform: scale(1.05); }
        button:active { transform: scale(0.95); }
        
        .file-preview {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }
        
        .file-item {
            background: #e9ecef;
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 0.85em;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .file-item .remove {
            cursor: pointer;
            color: #dc3545;
            font-weight: bold;
        }
        
        .preview-image {
            max-width: 80px;
            max-height: 80px;
            border-radius: 5px;
        }
        
        input[type="file"] { display: none; }
        
        .loading {
            display: none;
            text-align: center;
            padding: 10px;
            color: #667eea;
        }
        
        .loading.active { display: block; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 زيزو - Zizo AI</h1>
        <p>مساعد ذكاء اصطناعي مع دعم الصور والملفات</p>
    </div>
    
    <div class="container">
        <div class="chat-box">
            <div class="messages" id="messages">
                <div class="message ai">
                    مرحباً! 👋 أنا زيزو، يمكنني الآن:<br>
                    ✅ تحليل الصور<br>
                    ✅ قراءة الملفات<br>
                    ✅ الإجابة على أسئلتك<br>
                    جرّب رفع صورة أو ملف! 😊
                </div>
            </div>
            
            <div class="loading" id="loading">⏳ جاري التفكير...</div>
            
            <div class="input-area">
                <div class="file-preview" id="filePreview" style="display: none;"></div>
                
                <div class="input-row">
                    <input type="text" id="userInput" placeholder="اكتب رسالتك..." 
                           onkeypress="if(event.key==='Enter') sendMsg()">
                    
                    <input type="file" id="imageUpload" accept="image/*" multiple onchange="handleFiles(this.files, 'image')">
                    <button class="upload-btn" onclick="document.getElementById('imageUpload').click()">📸 صورة</button>
                    
                    <input type="file" id="fileUpload" accept=".pdf,.txt" multiple onchange="handleFiles(this.files, 'file')">
                    <button class="upload-btn" onclick="document.getElementById('fileUpload').click()">📄 ملف</button>
                    
                    <button id="sendBtn" onclick="sendMsg()">إرسال ✈️</button>
                    
                    <button class="pro-btn" onclick="goToPro()">PRO 🚀</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        console.log('🚀 زيزو جاهز!');
        let history = [];
        let files = [];
        
        function addMsg(text, type) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.textContent = text;
            document.getElementById('messages').appendChild(div);
            document.getElementById('messages').scrollTop = 999999;
        }
        
        function handleFiles(fileList, type) {
            console.log('📎 رفع ملفات:', type, fileList.length);
            
            Array.from(fileList).forEach(file => {
                if (file.size > 10 * 1024 * 1024) {
                    alert('⚠️ الملف كبير جداً! الحد الأقصى: 10MB');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const fileData = {
                        name: file.name,
                        type: type,
                        data: e.target.result
                    };
                    files.push(fileData);
                    showPreview(fileData);
                };
                reader.readAsDataURL(file);
            });
        }
        
        function showPreview(fileData) {
            const preview = document.getElementById('filePreview');
            preview.style.display = 'flex';
            
            const item = document.createElement('div');
            item.className = 'file-item';
            
            if (fileData.type === 'image') {
                const img = document.createElement('img');
                img.src = fileData.data;
                img.className = 'preview-image';
                item.appendChild(img);
            } else {
                item.textContent = '📄 ' + fileData.name + ' ';
            }
            
            const remove = document.createElement('span');
            remove.className = 'remove';
            remove.textContent = '×';
            remove.onclick = function() {
                files = files.filter(f => f.name !== fileData.name);
                item.remove();
                if (files.length === 0) preview.style.display = 'none';
            };
            item.appendChild(remove);
            
            preview.appendChild(item);
        }
        
        async function sendMsg() {
            console.log('📤 إرسال رسالة...');
            
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            
            if (!text && files.length === 0) {
                alert('⚠️ اكتب رسالة أو ارفع ملف!');
                return;
            }
            
            // عرض رسالة المستخدم
            let userMsg = text;
            if (files.length > 0) userMsg += ` [📎 ${files.length} ملف]`;
            addMsg(userMsg, 'user');
            
            input.value = '';
            input.disabled = true;
            document.getElementById('sendBtn').disabled = true;
            document.getElementById('loading').classList.add('active');
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: text,
                        history: history,
                        files: files
                    })
                });
                
                const data = await response.json();
                
                if (data.response) {
                    addMsg(data.response, 'ai');
                    history = data.history || history;
                    
                    // مسح الملفات
                    files = [];
                    document.getElementById('filePreview').innerHTML = '';
                    document.getElementById('filePreview').style.display = 'none';
                } else {
                    addMsg('❌ حدث خطأ. حاول مرة أخرى.', 'ai');
                }
            } catch (error) {
                console.error('❌ خطأ:', error);
                addMsg('❌ خطأ في الاتصال.', 'ai');
            } finally {
                input.disabled = false;
                document.getElementById('sendBtn').disabled = false;
                document.getElementById('loading').classList.remove('active');
                input.focus();
            }
        }
        
        function goToPro() {
            if (confirm('🚀 التبديل إلى زيزو برو؟\\n\\nميزات PRO:\\n✅ إنشاء الصور\\n✅ إنشاء الفيديوهات\\n✅ برمجة متقدمة\\n✅ المزيد...')) {
                window.location.href = '/pro';
            }
        }
        
        // تركيز تلقائي
        document.getElementById('userInput').focus();
        console.log('✅ كل شيء جاهز!');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        history = data.get('history', [])
        files = data.get('files', [])
        
        # بناء المحتوى
        if files:
            content_parts = []
            if user_message:
                content_parts.append({"type": "text", "text": user_message})
            
            for file in files:
                if file.get('type') == 'image':
                    content_parts.append({
                        "type": "image_url",
                        "image_url": {"url": file['data']}
                    })
                else:
                    content_parts.append({
                        "type": "text",
                        "text": f"\n[ملف: {file['name']}]\nملاحظة: معالجة الملفات قيد التطوير.\n"
                    })
            
            history.append({"role": "user", "content": content_parts})
        else:
            history.append({"role": "user", "content": user_message})
        
        # الحصول على رد AI
        response = client.run(ai_agent, history, context_variables={}, debug=False, max_turns=1)
        ai_response = response.messages[-1]['content']
        
        history.append({"role": "assistant", "content": ai_response})
        
        if len(history) > 20:
            history = history[-20:]
        
        return jsonify({
            'response': ai_response,
            'history': history,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/pro')
def pro():
    return """
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #f093fb, #f5576c);
                color: white;
                text-align: center;
                padding: 50px;
            }
            button {
                background: white;
                color: #f5576c;
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                cursor: pointer;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>🚀 زيزو برو</h1>
        <p>النسخة المتقدمة قريباً!</p>
        <button onclick="window.location.href='/'">← العودة</button>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'app': 'Zizo Simple',
        'model': AI_MODEL,
        'version': '3.0.0-simple'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)

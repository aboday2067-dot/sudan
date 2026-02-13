# 🌟 Zizo Pro - GPT-5 Powered Version
# النسخة الاحترافية المدعومة بـ GPT-5

from flask import Flask, render_template_string, request, jsonify, stream_with_context, Response
import os
import secrets
import json
from dotenv import load_dotenv
import yaml

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# تحميل إعدادات OpenAI من الملف
config_path = os.path.expanduser('~/.genspark_llm.yaml')
config = None
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

# إعدادات API
OPENAI_API_KEY = config.get('openai', {}).get('api_key') if config else os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = config.get('openai', {}).get('base_url') if config else os.getenv('OPENAI_BASE_URL', 'https://www.genspark.ai/api/llm_proxy/v1')

# استيراد OpenAI
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    GPT5_AVAILABLE = True
except Exception as e:
    print(f"⚠️ GPT-5 not available: {e}")
    GPT5_AVAILABLE = False

# HTML Template - نسخة محسّنة
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>زيزو برو - GPT-5 Powered</title>
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
            backdrop-filter: blur(10px);
            padding: 20px;
            color: white;
            text-align: center;
        }
        
        .header h1 { 
            font-size: 2em; 
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .badge {
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .container {
            flex: 1;
            max-width: 1000px;
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
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
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
            animation: slideIn 0.3s;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            align-self: flex-end;
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        }
        
        .ai { 
            background: #f0f0f0; 
            color: #333; 
            align-self: flex-start;
            border-left: 4px solid #667eea;
        }
        
        .typing {
            background: #e9ecef;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 75%;
            align-self: flex-start;
            display: flex;
            gap: 5px;
        }
        
        .typing span {
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
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
            transition: border 0.3s;
        }
        
        #userInput:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        }
        
        .upload-btn {
            background: #28a745;
            color: white;
        }
        
        .pro-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .pro-btn::before {
            content: '✨';
            position: absolute;
            top: 50%;
            left: -20px;
            transform: translateY(-50%);
            animation: sparkle 2s infinite;
        }
        
        @keyframes sparkle {
            0%, 100% { left: -20px; opacity: 0; }
            50% { left: 50%; opacity: 1; }
        }
        
        button:hover { transform: scale(1.05); }
        button:active { transform: scale(0.95); }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        
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
        
        .stats {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 15px;
            margin-top: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .stat-label { font-size: 0.8em; opacity: 0.9; }
        .stat-value { font-size: 1.2em; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 زيزو برو - Zizo Pro</h1>
        <div class="badge">🔥 Powered by GPT-5 🔥</div>
        <p style="margin-top: 10px; opacity: 0.9;">مساعد ذكاء اصطناعي متقدم مع رؤية وفهم عميق</p>
    </div>
    
    <div class="container">
        <div class="chat-box">
            <div class="messages" id="messages">
                <div class="message ai">
                    مرحباً! 👋 أنا زيزو برو، المدعوم بـ <strong>GPT-5</strong>! 🚀<br><br>
                    قدراتي المتقدمة:<br>
                    🎨 <strong>تحليل الصور</strong> - أفهم الصور بعمق<br>
                    📄 <strong>قراءة الملفات</strong> - أعالج المستندات<br>
                    💬 <strong>محادثات ذكية</strong> - فهم عميق للسياق<br>
                    🧠 <strong>تفكير متقدم</strong> - حل مشاكل معقدة<br>
                    ⚡ <strong>استجابة فورية</strong> - بدون انتظار<br><br>
                    جرّب الآن! ارفع صورة أو اطرح سؤالاً! 😊
                </div>
            </div>
            
            <div class="input-area">
                <div class="file-preview" id="filePreview" style="display: none;"></div>
                
                <div class="input-row">
                    <input type="text" id="userInput" placeholder="اكتب رسالتك... (اضغط Enter للإرسال)" 
                           onkeypress="if(event.key==='Enter') sendMsg()">
                    
                    <input type="file" id="imageUpload" accept="image/*" multiple onchange="handleFiles(this.files, 'image')">
                    <button class="upload-btn" onclick="document.getElementById('imageUpload').click()" title="رفع صورة">📸</button>
                    
                    <input type="file" id="fileUpload" accept=".pdf,.txt" multiple onchange="handleFiles(this.files, 'file')">
                    <button class="upload-btn" onclick="document.getElementById('fileUpload').click()" title="رفع ملف">📄</button>
                    
                    <button id="sendBtn" onclick="sendMsg()">إرسال ✈️</button>
                </div>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-label">النموذج</div>
                <div class="stat-value">GPT-5</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">الرسائل</div>
                <div class="stat-value" id="msgCount">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">الحالة</div>
                <div class="stat-value">🟢 نشط</div>
            </div>
        </div>
    </div>

    <script>
        console.log('🚀 زيزو برو جاهز - GPT-5 Powered!');
        let history = [];
        let files = [];
        let msgCount = 0;
        
        function addMsg(text, type) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            
            if (type === 'ai') {
                div.innerHTML = text.replace(/\\n/g, '<br>');
            } else {
                div.textContent = text;
            }
            
            document.getElementById('messages').appendChild(div);
            document.getElementById('messages').scrollTop = 999999;
            
            if (type === 'user') {
                msgCount++;
                document.getElementById('msgCount').textContent = msgCount;
            }
        }
        
        function showTyping() {
            const typing = document.createElement('div');
            typing.className = 'typing';
            typing.id = 'typing';
            typing.innerHTML = '<span></span><span></span><span></span>';
            document.getElementById('messages').appendChild(typing);
            document.getElementById('messages').scrollTop = 999999;
        }
        
        function hideTyping() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
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
            if (files.length > 0) {
                userMsg += ` 📎 [${files.length} ${files.length === 1 ? 'ملف' : 'ملفات'}]`;
            }
            addMsg(userMsg, 'user');
            
            input.value = '';
            input.disabled = true;
            document.getElementById('sendBtn').disabled = true;
            showTyping();
            
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
                
                hideTyping();
                
                const data = await response.json();
                
                if (data.response) {
                    addMsg(data.response, 'ai');
                    history = data.history || history;
                    
                    // مسح الملفات
                    files = [];
                    document.getElementById('filePreview').innerHTML = '';
                    document.getElementById('filePreview').style.display = 'none';
                } else {
                    addMsg('❌ حدث خطأ: ' + (data.error || 'خطأ غير معروف'), 'ai');
                }
            } catch (error) {
                hideTyping();
                console.error('❌ خطأ:', error);
                addMsg('❌ خطأ في الاتصال. يرجى المحاولة مرة أخرى.', 'ai');
            } finally {
                input.disabled = false;
                document.getElementById('sendBtn').disabled = false;
                input.focus();
            }
        }
        
        // تركيز تلقائي
        document.getElementById('userInput').focus();
        console.log('✅ كل شيء جاهز - GPT-5 Ready!');
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
        
        if not GPT5_AVAILABLE:
            return jsonify({
                'error': 'GPT-5 غير متاح حالياً. يرجى التحقق من إعدادات API.',
                'status': 'error'
            }), 500
        
        # بناء الرسائل
        messages = []
        
        # إضافة System Prompt
        messages.append({
            "role": "system",
            "content": """أنا زيزو برو 🚀، مساعد ذكاء اصطناعي متقدم مدعوم بـ GPT-5!

قدراتي المتقدمة:
- تحليل الصور بعمق ودقة عالية
- فهم السياق والمحادثات المعقدة
- حل المشاكل البرمجية والرياضية
- شرح المفاهيم بطريقة واضحة
- الإبداع والكتابة

أسلوبي:
- ودود ومحترف
- إجابات واضحة ومباشرة
- أستخدم الأمثلة عند الحاجة
- أتحدث العربية والإنجليزية بطلاقة

دائماً في خدمتك! 😊"""
        })
        
        # إضافة التاريخ
        for msg in history[-10:]:  # آخر 10 رسائل فقط
            messages.append(msg)
        
        # إضافة الرسالة الحالية
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
                        "text": f"\n[ملف مرفق: {file['name']}]\n"
                    })
            
            messages.append({"role": "user", "content": content_parts})
        else:
            messages.append({"role": "user", "content": user_message})
        
        # استدعاء GPT-5
        completion = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        ai_response = completion.choices[0].message.content
        
        # تحديث التاريخ
        history.append({"role": "user", "content": user_message if not files else content_parts})
        history.append({"role": "assistant", "content": ai_response})
        
        if len(history) > 20:
            history = history[-20:]
        
        return jsonify({
            'response': ai_response,
            'history': history,
            'status': 'success',
            'model': 'gpt-5',
            'tokens': completion.usage.total_tokens if hasattr(completion, 'usage') else None
        })
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return jsonify({
            'error': f'حدث خطأ: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'app': 'Zizo Pro',
        'model': 'GPT-5',
        'version': '4.0.0-pro',
        'gpt5_available': GPT5_AVAILABLE,
        'base_url': OPENAI_BASE_URL
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 زيزو برو يعمل على البورت {port}")
    print(f"🔥 GPT-5: {'✅ متاح' if GPT5_AVAILABLE else '❌ غير متاح'}")
    app.run(host='0.0.0.0', port=port, debug=False)

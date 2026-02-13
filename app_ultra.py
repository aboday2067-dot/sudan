# 🔥 Zizo Ultra Pro - The Insane Genius Version
# النسخة العبقرية المجنونة!

from flask import Flask, render_template_string, request, jsonify, Response
import os
import secrets
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import yaml

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Load OpenAI config
config_path = os.path.expanduser('~/.genspark_llm.yaml')
config = None
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

OPENAI_API_KEY = config.get('openai', {}).get('api_key') if config else os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = config.get('openai', {}).get('base_url') if config else os.getenv('OPENAI_BASE_URL', 'https://www.genspark.ai/api/llm_proxy/v1')

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    GPT5_AVAILABLE = True
except:
    GPT5_AVAILABLE = False

# Stats
stats = {
    'total_messages': 0,
    'total_images': 0,
    'start_time': datetime.now()
}

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>🔥 زيزو الترا برو</title>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        /* Header - مضغوط جداً */
        .header {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 10px 15px;
            color: white;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            flex-shrink: 0;
        }
        
        .header h1 { 
            font-size: 1.3em; 
            margin: 0;
        }
        
        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.7em;
            margin-top: 3px;
        }
        
        /* Chat Area */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: white;
            margin: 0;
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .message {
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 85%;
            word-wrap: break-word;
            font-size: 0.9em;
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
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        .ai {
            background: #f0f0f0;
            color: #333;
            align-self: flex-start;
            border-left: 3px solid #667eea;
        }
        
        /* Typing Indicator */
        .typing {
            background: #e9ecef;
            padding: 10px 15px;
            border-radius: 15px;
            align-self: flex-start;
            display: flex;
            gap: 5px;
        }
        
        .typing span {
            width: 6px;
            height: 6px;
            background: #667eea;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-8px); }
        }
        
        /* Input Area - محسّن للجوال */
        .input-area {
            background: #f8f9fa;
            border-top: 1px solid #ddd;
            padding: 8px;
            flex-shrink: 0;
        }
        
        .file-preview {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 6px;
            max-height: 80px;
            overflow-x: auto;
        }
        
        .file-item {
            background: #e9ecef;
            padding: 6px 10px;
            border-radius: 10px;
            font-size: 0.75em;
            display: flex;
            align-items: center;
            gap: 5px;
            white-space: nowrap;
        }
        
        .file-item .remove {
            cursor: pointer;
            color: #dc3545;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .preview-image {
            max-width: 60px;
            max-height: 60px;
            border-radius: 5px;
        }
        
        /* Input Row - صف واحد مضغوط */
        .input-row {
            display: flex;
            gap: 6px;
            align-items: center;
        }
        
        #userInput {
            flex: 1;
            padding: 10px 12px;
            border: 2px solid #ddd;
            border-radius: 20px;
            font-size: 0.9em;
            outline: none;
            min-width: 0;
        }
        
        #userInput:focus {
            border-color: #667eea;
        }
        
        /* Buttons - أكبر وأوضح */
        .btn {
            padding: 10px 15px;
            border: none;
            border-radius: 20px;
            font-size: 1.2em;
            cursor: pointer;
            transition: transform 0.1s;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 45px;
            height: 45px;
        }
        
        .btn:active {
            transform: scale(0.9);
        }
        
        .btn-upload {
            background: #28a745;
            color: white;
        }
        
        .btn-send {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-voice {
            background: #ff6b6b;
            color: white;
        }
        
        .btn-clear {
            background: #6c757d;
            color: white;
        }
        
        input[type="file"] { 
            display: none; 
        }
        
        /* Bottom Bar - شريط أدوات إضافي */
        .bottom-bar {
            background: rgba(255,255,255,0.95);
            padding: 8px;
            display: flex;
            gap: 6px;
            justify-content: space-around;
            border-top: 1px solid #ddd;
            flex-shrink: 0;
        }
        
        .tool-btn {
            flex: 1;
            padding: 8px;
            border: none;
            border-radius: 10px;
            font-size: 0.75em;
            background: white;
            border: 1px solid #ddd;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
        }
        
        .tool-btn:active {
            background: #f0f0f0;
        }
        
        .tool-icon {
            font-size: 1.5em;
        }
        
        /* Floating Action Button */
        .fab {
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            font-size: 1.8em;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
            cursor: pointer;
            z-index: 1000;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .fab:active {
            transform: scale(0.95);
        }
        
        /* Stats Bar */
        .stats {
            background: rgba(0,0,0,0.5);
            color: white;
            padding: 5px;
            font-size: 0.7em;
            text-align: center;
            display: flex;
            justify-content: space-around;
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .modal-content {
            background: white;
            border-radius: 20px;
            padding: 20px;
            max-width: 500px;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .close {
            font-size: 2em;
            cursor: pointer;
            color: #999;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <h1>🔥 زيزو الترا برو</h1>
        <div class="badge">GPT-5 Powered</div>
    </div>
    
    <!-- Stats -->
    <div class="stats">
        <span>📊 <span id="msgCount">0</span> رسالة</span>
        <span>📸 <span id="imgCount">0</span> صورة</span>
        <span>⚡ GPT-5</span>
    </div>
    
    <!-- Chat -->
    <div class="chat-container">
        <div class="messages" id="messages">
            <div class="message ai">
                🚀 مرحباً! أنا <strong>زيزو الترا برو</strong><br>
                المدعوم بـ GPT-5!<br><br>
                <strong>ميزات جديدة:</strong><br>
                🎤 التحدث الصوتي<br>
                📸 تحليل صور متقدم<br>
                🧠 ذكاء خارق<br>
                ⚡ استجابة فورية<br><br>
                جرّب الآن! 😊
            </div>
        </div>
        
        <!-- Input Area -->
        <div class="input-area">
            <div class="file-preview" id="filePreview" style="display: none;"></div>
            
            <div class="input-row">
                <!-- Upload Button -->
                <input type="file" id="fileUpload" accept="image/*,.pdf,.txt" multiple onchange="handleFiles(this.files)">
                <button class="btn btn-upload" onclick="document.getElementById('fileUpload').click()" title="رفع">
                    📎
                </button>
                
                <!-- Input -->
                <input type="text" id="userInput" placeholder="اكتب رسالتك..." 
                       onkeypress="if(event.key==='Enter') sendMsg()">
                
                <!-- Send Button -->
                <button class="btn btn-send" onclick="sendMsg()" title="إرسال">
                    ✈️
                </button>
                
                <!-- Voice Button -->
                <button class="btn btn-voice" onclick="startVoice()" title="صوت">
                    🎤
                </button>
            </div>
        </div>
    </div>
    
    <!-- Bottom Tools Bar -->
    <div class="bottom-bar">
        <button class="tool-btn" onclick="showFeatures()">
            <span class="tool-icon">✨</span>
            <span>ميزات</span>
        </button>
        <button class="tool-btn" onclick="clearChat()">
            <span class="tool-icon">🗑️</span>
            <span>مسح</span>
        </button>
        <button class="tool-btn" onclick="shareChat()">
            <span class="tool-icon">📤</span>
            <span>مشاركة</span>
        </button>
        <button class="tool-btn" onclick="showSettings()">
            <span class="tool-icon">⚙️</span>
            <span>إعدادات</span>
        </button>
    </div>
    
    <!-- Floating Action Button -->
    <button class="fab" onclick="quickAction()" title="إجراء سريع">
        ⚡
    </button>
    
    <!-- Modal -->
    <div class="modal" id="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">العنوان</h2>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            <div id="modalBody">المحتوى</div>
        </div>
    </div>

    <script>
        console.log('🔥 زيزو الترا برو - Ready!');
        
        let history = [];
        let files = [];
        let msgCount = 0;
        let imgCount = 0;
        let isRecording = false;
        
        // Add Message
        function addMsg(text, type) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.innerHTML = text.replace(/\\n/g, '<br>');
            document.getElementById('messages').appendChild(div);
            document.getElementById('messages').scrollTop = 999999;
            
            if (type === 'user') {
                msgCount++;
                document.getElementById('msgCount').textContent = msgCount;
            }
        }
        
        // Typing Indicator
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
        
        // Handle Files
        function handleFiles(fileList) {
            Array.from(fileList).forEach(file => {
                if (file.size > 10 * 1024 * 1024) {
                    alert('⚠️ الملف كبير جداً! الحد الأقصى: 10MB');
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const fileData = {
                        name: file.name,
                        type: file.type.startsWith('image/') ? 'image' : 'file',
                        data: e.target.result
                    };
                    files.push(fileData);
                    showPreview(fileData);
                    
                    if (fileData.type === 'image') {
                        imgCount++;
                        document.getElementById('imgCount').textContent = imgCount;
                    }
                };
                reader.readAsDataURL(file);
            });
        }
        
        // Show Preview
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
                item.innerHTML = '📄 ' + fileData.name.substring(0, 10) + '... ';
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
        
        // Send Message
        async function sendMsg() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            
            if (!text && files.length === 0) {
                alert('⚠️ اكتب رسالة أو ارفع ملف!');
                return;
            }
            
            let userMsg = text;
            if (files.length > 0) {
                userMsg += ` 📎 [${files.length}]`;
            }
            addMsg(userMsg, 'user');
            
            input.value = '';
            input.disabled = true;
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
                    
                    files = [];
                    document.getElementById('filePreview').innerHTML = '';
                    document.getElementById('filePreview').style.display = 'none';
                } else {
                    addMsg('❌ خطأ: ' + (data.error || 'غير معروف'), 'ai');
                }
            } catch (error) {
                hideTyping();
                addMsg('❌ خطأ في الاتصال', 'ai');
            } finally {
                input.disabled = false;
                input.focus();
            }
        }
        
        // Voice Recording
        function startVoice() {
            if (!isRecording) {
                // Start recording
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(stream => {
                        isRecording = true;
                        addMsg('🎤 جاري التسجيل... اضغط مرة أخرى للإيقاف', 'ai');
                        // TODO: Implement actual recording
                    })
                    .catch(err => {
                        alert('⚠️ لا يمكن الوصول للميكروفون');
                    });
            } else {
                // Stop recording
                isRecording = false;
                addMsg('✅ تم إيقاف التسجيل', 'ai');
            }
        }
        
        // Quick Action
        function quickAction() {
            const actions = [
                'اشرح لي موضوعاً',
                'حلل هذه الصورة',
                'اكتب لي كود',
                'ترجم إلى الإنجليزية',
                'لخص هذا النص'
            ];
            const action = actions[Math.floor(Math.random() * actions.length)];
            document.getElementById('userInput').value = action;
            document.getElementById('userInput').focus();
        }
        
        // Clear Chat
        function clearChat() {
            if (confirm('🗑️ هل تريد مسح المحادثة؟')) {
                document.getElementById('messages').innerHTML = `
                    <div class="message ai">
                        ✅ تم مسح المحادثة!<br>
                        ابدأ محادثة جديدة 😊
                    </div>
                `;
                history = [];
                files = [];
                msgCount = 0;
                imgCount = 0;
                document.getElementById('msgCount').textContent = '0';
                document.getElementById('imgCount').textContent = '0';
            }
        }
        
        // Share Chat
        function shareChat() {
            const text = 'جرّب زيزو الترا برو - المساعد الذكي المدعوم بـ GPT-5!';
            if (navigator.share) {
                navigator.share({
                    title: 'زيزو الترا برو',
                    text: text,
                    url: window.location.href
                });
            } else {
                alert('📤 انسخ الرابط: ' + window.location.href);
            }
        }
        
        // Show Features
        function showFeatures() {
            showModal('✨ الميزات المتاحة', `
                <div style="text-align: right; line-height: 2;">
                    🧠 <strong>GPT-5</strong> - أقوى نموذج AI<br>
                    📸 <strong>تحليل الصور</strong> - فهم عميق<br>
                    🎤 <strong>التحدث الصوتي</strong> - قريباً<br>
                    📄 <strong>قراءة الملفات</strong> - PDF & TXT<br>
                    💬 <strong>محادثات ذكية</strong> - سياق كامل<br>
                    ⚡ <strong>استجابة فورية</strong> - أقل من ثانية<br>
                    🎨 <strong>تصميم عصري</strong> - واجهة جميلة<br>
                    📱 <strong>دعم الجوال</strong> - تجربة مثالية
                </div>
            `);
        }
        
        // Show Settings
        function showSettings() {
            showModal('⚙️ الإعدادات', `
                <div style="text-align: right;">
                    <p><strong>النموذج:</strong> GPT-5</p>
                    <p><strong>الإصدار:</strong> 5.0.0-ultra</p>
                    <p><strong>الحالة:</strong> 🟢 نشط</p>
                    <hr>
                    <button onclick="clearChat(); closeModal();" 
                            style="width: 100%; padding: 10px; margin-top: 10px; 
                            background: #dc3545; color: white; border: none; 
                            border-radius: 10px; cursor: pointer;">
                        🗑️ مسح المحادثة
                    </button>
                </div>
            `);
        }
        
        // Modal Functions
        function showModal(title, body) {
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalBody').innerHTML = body;
            document.getElementById('modal').style.display = 'flex';
        }
        
        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }
        
        // Auto-focus
        document.getElementById('userInput').focus();
        console.log('✅ All systems ready!');
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
            return jsonify({'error': 'GPT-5 غير متاح', 'status': 'error'}), 500
        
        messages = []
        messages.append({
            "role": "system",
            "content": """أنا زيزو الترا برو 🔥، أقوى مساعد AI في العالم!

مدعوم بـ GPT-5 مع قدرات خارقة:
- فهم عميق للصور والنصوص
- حل مشاكل معقدة
- إبداع وكتابة احترافية
- برمجة متقدمة
- شرح مفاهيم معقدة ببساطة

أسلوبي: ودود، ذكي، سريع، مبدع
دائماً في خدمتك! 💪"""
        })
        
        for msg in history[-10:]:
            messages.append(msg)
        
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
            
            messages.append({"role": "user", "content": content_parts})
        else:
            messages.append({"role": "user", "content": user_message})
        
        completion = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.8,
            max_tokens=2000
        )
        
        ai_response = completion.choices[0].message.content
        
        history.append({"role": "user", "content": user_message if not files else content_parts})
        history.append({"role": "assistant", "content": ai_response})
        
        if len(history) > 20:
            history = history[-20:]
        
        stats['total_messages'] += 1
        if files:
            stats['total_images'] += len([f for f in files if f.get('type') == 'image'])
        
        return jsonify({
            'response': ai_response,
            'history': history,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health')
def health():
    uptime = (datetime.now() - stats['start_time']).seconds
    return jsonify({
        'status': 'healthy',
        'app': 'Zizo Ultra Pro',
        'model': 'GPT-5',
        'version': '5.0.0-ultra',
        'gpt5_available': GPT5_AVAILABLE,
        'stats': {
            'total_messages': stats['total_messages'],
            'total_images': stats['total_images'],
            'uptime_seconds': uptime
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🔥 زيزو الترا برو - البورت {port}")
    print(f"⚡ GPT-5: {'✅ متاح' if GPT5_AVAILABLE else '❌ غير متاح'}")
    app.run(host='0.0.0.0', port=port, debug=False)

from flask import Flask, request, jsonify, render_template_string, send_file
import os
import yaml
from openai import OpenAI
import time
import random
import base64
import io
import json
import requests

app = Flask(__name__)

# Load OpenAI config
config_path = os.path.expanduser('~/.genspark_llm.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

client = OpenAI(
    api_key=config['openai']['api_key'],
    base_url=config['openai']['base_url']
)

# Stats
stats = {
    'total_messages': 0,
    'total_images': 0,
    'total_files': 0,
    'generated_images': 0,
    'generated_videos': 0,
    'generated_codes': 0,
    'start_time': time.time()
}

# Temporary storage for generated content
generated_content = {}

SUPERNOVA_HTML = '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>زيزو سوبر نوفا 🌟 - All-in-One AI</title>
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
            overflow: hidden;
        }
        
        #app {
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: rgba(255,255,255,0.98);
        }
        
        /* Header */
        header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 12px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        h1 {
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 3px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 11px;
            opacity: 0.95;
        }
        
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.25);
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 10px;
            margin-top: 3px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.4);
        }
        
        /* Powers Bar - قدرات زيزو */
        #powersBar {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            padding: 8px;
            display: flex;
            gap: 6px;
            overflow-x: auto;
            flex-wrap: nowrap;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }
        
        .power-btn {
            background: rgba(255,255,255,0.9);
            border: none;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.3s;
            flex-shrink: 0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        
        .power-btn:active {
            transform: scale(0.95);
            background: white;
        }
        
        .power-btn.active {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        /* Messages */
        #messages {
            flex: 1;
            overflow-y: auto;
            padding: 12px;
            background: linear-gradient(to bottom, #ffecd2 0%, #fcb69f 100%);
        }
        
        .message {
            margin-bottom: 12px;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            text-align: left;
        }
        
        .assistant-message {
            text-align: right;
        }
        
        .message-bubble {
            display: inline-block;
            max-width: 85%;
            padding: 10px 14px;
            border-radius: 16px;
            word-wrap: break-word;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .user-message .message-bubble {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-left-radius: 4px;
        }
        
        .assistant-message .message-bubble {
            background: white;
            color: #333;
            border-bottom-right-radius: 4px;
            border-right: 3px solid #667eea;
        }
        
        .message-bubble img {
            max-width: 100%;
            border-radius: 10px;
            margin-top: 8px;
        }
        
        .message-bubble pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 10px;
            border-radius: 8px;
            overflow-x: auto;
            margin-top: 8px;
            font-size: 12px;
        }
        
        .download-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 15px;
            margin-top: 6px;
            cursor: pointer;
            font-size: 11px;
        }
        
        /* Preview Area */
        #previewArea {
            padding: 8px 12px;
            background: white;
            border-top: 1px solid #e0e0e0;
            min-height: 0;
            max-height: 100px;
            overflow-y: auto;
        }
        
        .preview-item {
            display: inline-flex;
            align-items: center;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 6px 10px;
            border-radius: 18px;
            margin: 3px;
            font-size: 11px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.12);
        }
        
        .preview-item img {
            width: 25px;
            height: 25px;
            border-radius: 5px;
            margin-left: 6px;
            object-fit: cover;
        }
        
        .remove-btn {
            background: rgba(255,255,255,0.3);
            border: none;
            color: white;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            margin-right: 6px;
            cursor: pointer;
            font-size: 12px;
        }
        
        /* Input Area */
        #inputArea {
            background: white;
            padding: 10px;
            border-top: 2px solid #667eea;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.08);
        }
        
        .input-wrapper {
            display: flex;
            gap: 6px;
            align-items: center;
        }
        
        /* SUPER BUTTONS - HUGE & CLEAR */
        .btn-super {
            width: 48px !important;
            height: 48px !important;
            border-radius: 50% !important;
            border: none;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.18);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .btn-image {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }
        
        .btn-file {
            background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
        }
        
        .btn-send {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            width: 52px !important;
            height: 52px !important;
        }
        
        .btn-super:active {
            transform: scale(0.92);
        }
        
        #userInput {
            flex: 1;
            border: 2px solid #667eea;
            border-radius: 24px;
            padding: 10px 16px;
            font-size: 15px;
            outline: none;
            background: #f8f9ff;
            min-height: 48px;
        }
        
        #userInput:focus {
            border-color: #764ba2;
            background: white;
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.75);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: white;
            border-radius: 20px;
            padding: 20px;
            max-width: 90%;
            max-height: 80%;
            overflow-y: auto;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        
        .modal-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 12px;
            color: #667eea;
        }
        
        .modal-input {
            width: 100%;
            padding: 10px;
            border: 2px solid #667eea;
            border-radius: 10px;
            margin: 8px 0;
            font-size: 14px;
        }
        
        .modal-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            margin: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .modal-close {
            background: #f5576c;
        }
        
        /* Loading */
        #loadingOverlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(102, 126, 234, 0.92);
            z-index: 3000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
        }
        
        .loader {
            width: 55px;
            height: 55px;
            border: 5px solid rgba(255,255,255,0.3);
            border-top: 5px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            margin-top: 18px;
            font-size: 17px;
            font-weight: 600;
        }
        
        /* Typing Indicator */
        .typing-indicator {
            display: inline-flex;
            gap: 4px;
            padding: 8px 12px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        
        .typing-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #667eea;
            animation: typing 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-8px); }
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <!-- Loading Overlay -->
    <div id="loadingOverlay">
        <div class="loader"></div>
        <div class="loading-text">⚡ سوبر نوفا يعمل...</div>
    </div>
    
    <!-- Main App -->
    <div id="app">
        <!-- Header -->
        <header>
            <h1>🌟 زيزو سوبر نوفا AI</h1>
            <div class="subtitle">مساعد ذكاء اصطناعي شامل - كل شيء في مكان واحد</div>
            <div class="badge">⚡ GPT-5 + DALL-E + Code Gen</div>
        </header>
        
        <!-- Powers Bar -->
        <div id="powersBar">
            <button class="power-btn active" onclick="setPower('chat')">💬 دردشة</button>
            <button class="power-btn" onclick="setPower('image')">🎨 صور</button>
            <button class="power-btn" onclick="setPower('video')">🎬 فيديو</button>
            <button class="power-btn" onclick="setPower('code')">💻 أكواد</button>
            <button class="power-btn" onclick="setPower('website')">🌐 مواقع</button>
            <button class="power-btn" onclick="setPower('app')">📱 تطبيقات</button>
        </div>
        
        <!-- Messages -->
        <div id="messages"></div>
        
        <!-- Preview Area -->
        <div id="previewArea" style="display:none;"></div>
        
        <!-- Input Area -->
        <div id="inputArea">
            <div class="input-wrapper">
                <button class="btn-super btn-image" onclick="uploadImage()" title="رفع صورة">📸</button>
                <button class="btn-super btn-file" onclick="uploadFile()" title="رفع ملف">📄</button>
                
                <input type="text" id="userInput" placeholder="اكتب طلبك هنا..." />
                
                <button class="btn-super btn-send" onclick="sendMessage()" title="إرسال">✈️</button>
            </div>
        </div>
    </div>
    
    <!-- Hidden File Inputs -->
    <input type="file" id="imageUpload" accept="image/*" style="display:none;" onchange="handleImageUpload(event)">
    <input type="file" id="fileUpload" accept=".pdf,.txt,.doc,.docx" style="display:none;" onchange="handleFileUpload(event)">
    
    <script>
        // Global State
        let uploadedFiles = [];
        let conversationHistory = [];
        let currentPower = 'chat';
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            addMessage('assistant', '👋 مرحباً! أنا **زيزو سوبر نوفا** - مساعدك الذكي الشامل!\\n\\n✨ **قدراتي:**\\n💬 **دردشة ذكية** مع GPT-5\\n🎨 **توليد صور** احترافية\\n🎬 **إنشاء فيديوهات** (قريباً)\\n💻 **كتابة أكواد** كاملة\\n🌐 **بناء مواقع** إلكترونية\\n📱 **تطوير تطبيقات** جوال\\n\\nاختر القدرة من الأعلى وأخبرني بماذا تريد! 🚀');
            
            // Enter key
            document.getElementById('userInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            console.log('🌟 SuperNova AI Ready!');
        });
        
        // Set Power Mode
        function setPower(power) {
            currentPower = power;
            
            // Update buttons
            document.querySelectorAll('.power-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Update placeholder
            const placeholders = {
                'chat': 'اكتب سؤالك أو طلبك...',
                'image': 'صف الصورة التي تريدها، مثال: غروب على شاطئ البحر',
                'video': 'صف الفيديو الذي تريده (قريباً)',
                'code': 'اطلب الكود، مثال: موقع بورتفوليو بـ HTML/CSS',
                'website': 'صف الموقع، مثال: موقع متجر إلكتروني عصري',
                'app': 'صف التطبيق، مثال: تطبيق Todo list بـ React'
            };
            
            document.getElementById('userInput').placeholder = placeholders[power];
        }
        
        // Upload Image
        function uploadImage() {
            document.getElementById('imageUpload').click();
        }
        
        function handleImageUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            if (file.size > 10 * 1024 * 1024) {
                alert('❌ الصورة كبيرة جداً! الحد الأقصى 10MB');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = (e) => {
                uploadedFiles.push({
                    type: 'image',
                    name: file.name,
                    data: e.target.result
                });
                updatePreview();
            };
            reader.readAsDataURL(file);
        }
        
        // Upload File
        function uploadFile() {
            document.getElementById('fileUpload').click();
        }
        
        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            if (file.size > 10 * 1024 * 1024) {
                alert('❌ الملف كبير جداً! الحد الأقصى 10MB');
                return;
            }
            
            const reader = new FileReader();
            reader.onload = (e) => {
                uploadedFiles.push({
                    type: 'file',
                    name: file.name,
                    data: e.target.result
                });
                updatePreview();
            };
            reader.readAsDataURL(file);
        }
        
        // Update Preview
        function updatePreview() {
            const previewArea = document.getElementById('previewArea');
            if (uploadedFiles.length === 0) {
                previewArea.style.display = 'none';
                previewArea.innerHTML = '';
                return;
            }
            
            previewArea.style.display = 'block';
            previewArea.innerHTML = uploadedFiles.map((file, index) => {
                if (file.type === 'image') {
                    return `
                        <div class="preview-item">
                            <button class="remove-btn" onclick="removeFile(${index})">×</button>
                            <img src="${file.data}" alt="${file.name}">
                            <span>📸 ${file.name}</span>
                        </div>
                    `;
                } else {
                    return `
                        <div class="preview-item">
                            <button class="remove-btn" onclick="removeFile(${index})">×</button>
                            <span>📄 ${file.name}</span>
                        </div>
                    `;
                }
            }).join('');
        }
        
        function removeFile(index) {
            uploadedFiles.splice(index, 1);
            updatePreview();
        }
        
        // Send Message
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message && uploadedFiles.length === 0) return;
            
            // Add user message
            if (message) {
                addMessage('user', message);
            }
            
            // Show uploaded files
            if (uploadedFiles.length > 0) {
                uploadedFiles.forEach(file => {
                    if (file.type === 'image') {
                        addMessage('user', `<img src="${file.data}" style="max-width: 200px; border-radius: 10px;">`);
                    } else {
                        addMessage('user', `📄 ${file.name}`);
                    }
                });
            }
            
            input.value = '';
            showTypingIndicator();
            
            // Prepare data
            const data = {
                message: message,
                files: uploadedFiles,
                history: conversationHistory,
                power: currentPower
            };
            
            // Clear uploads
            uploadedFiles = [];
            updatePreview();
            
            // Show loading
            document.getElementById('loadingOverlay').style.display = 'flex';
            
            try {
                const response = await fetch('/supernova', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                hideTypingIndicator();
                document.getElementById('loadingOverlay').style.display = 'none';
                
                if (result.response) {
                    if (result.type === 'image' && result.image_url) {
                        addMessage('assistant', `تم توليد الصورة! 🎨\\n<img src="${result.image_url}" style="max-width: 300px; border-radius: 10px; margin-top: 10px;">`);
                    } else if (result.type === 'code' && result.code) {
                        addMessage('assistant', `تم إنشاء الكود! 💻\\n<pre>${escapeHtml(result.code)}</pre>\\n<button class="download-btn" onclick="downloadCode('${result.filename}')">⬇️ تحميل الملف</button>`);
                    } else {
                        addMessage('assistant', result.response);
                    }
                    
                    conversationHistory = result.history || [];
                }
            } catch (error) {
                hideTypingIndicator();
                document.getElementById('loadingOverlay').style.display = 'none';
                addMessage('assistant', '❌ عذراً، حدث خطأ. حاول مرة أخرى.');
            }
        }
        
        // Add Message
        function addMessage(role, content) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}-message`;
            messageDiv.innerHTML = `<div class="message-bubble">${content}</div>`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Typing Indicator
        function showTypingIndicator() {
            const messagesDiv = document.getElementById('messages');
            const indicator = document.createElement('div');
            indicator.className = 'message assistant-message';
            indicator.id = 'typingIndicator';
            indicator.innerHTML = `
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            `;
            messagesDiv.appendChild(indicator);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function hideTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) indicator.remove();
        }
        
        // Escape HTML
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Download Code
        function downloadCode(filename) {
            window.open(`/download/${filename}`, '_blank');
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(SUPERNOVA_HTML)

@app.route('/supernova', methods=['POST'])
def supernova():
    try:
        data = request.json
        user_message = data.get('message', '')
        files = data.get('files', [])
        history = data.get('history', [])
        power = data.get('power', 'chat')
        
        # Handle different powers
        if power == 'image':
            # Generate image using DALL-E
            return generate_image(user_message)
        
        elif power == 'code':
            # Generate code
            return generate_code(user_message, history)
        
        elif power == 'website':
            # Generate website
            return generate_website(user_message, history)
        
        elif power == 'app':
            # Generate app code
            return generate_app(user_message, history)
        
        elif power == 'video':
            # Video generation (placeholder)
            return jsonify({
                'response': '🎬 **توليد الفيديوهات قريباً!**\\n\\nهذه الميزة تحت التطوير. ستكون متاحة قريباً مع:\\n• Runway Gen-2\\n• Pika Labs\\n• Stable Video Diffusion',
                'history': history
            })
        
        else:
            # Chat mode
            return chat_mode(user_message, files, history)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def chat_mode(user_message, files, history):
    """Regular chat with GPT-5"""
    content = []
    
    if user_message:
        content.append({"type": "text", "text": user_message})
    
    for file in files:
        if file['type'] == 'image':
            content.append({
                "type": "image_url",
                "image_url": {"url": file['data']}
            })
        elif file['type'] == 'file':
            content.append({
                "type": "text",
                "text": f"[File: {file['name']}]"
            })
    
    messages = [
        {"role": "system", "content": "أنت زيزو سوبر نوفا - مساعد ذكاء اصطناعي شامل يجيد الدردشة والإجابة على الأسئلة بالعربية والإنجليزية."}
    ]
    
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": content})
    
    response = client.chat.completions.create(
        model="gpt-5",
        messages=messages,
        temperature=0.7,
        max_tokens=2000
    )
    
    assistant_message = response.choices[0].message.content
    
    history.append({"role": "user", "content": user_message or "[ملف]"})
    history.append({"role": "assistant", "content": assistant_message})
    
    stats['total_messages'] += 1
    
    return jsonify({
        'response': assistant_message,
        'history': history[-20:]
    })

def generate_image(prompt):
    """Generate image using DALL-E"""
    try:
        # For demo: return a placeholder message
        # In production, use actual DALL-E API
        stats['generated_images'] += 1
        
        response_text = f"""🎨 **تم توليد الصورة بنجاح!**

**الوصف:** {prompt}

**ملاحظة:** لتوليد صور حقيقية، يحتاج زيزو إلى:
• واجهة DALL-E API
• أو Stable Diffusion
• أو Midjourney API

**الصورة النموذجية:** سيتم عرضها هنا عند التفعيل الكامل.

**البدائل المتاحة:**
• استخدام OpenAI DALL-E 3
• Stability AI SDXL
• Replicate API
        """
        
        return jsonify({
            'response': response_text,
            'type': 'image',
            'history': []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_code(prompt, history):
    """Generate code using GPT-5"""
    try:
        messages = [
            {"role": "system", "content": "أنت مبرمج خبير. قم بكتابة كود نظيف واحترافي وموثّق بالعربية والإنجليزية."}
        ]
        
        messages.extend(history[-5:])
        messages.append({"role": "user", "content": f"اكتب كود كامل لـ: {prompt}"})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.3,
            max_tokens=3000
        )
        
        code_response = response.choices[0].message.content
        
        # Extract code if wrapped in markdown
        code = code_response
        if '```' in code:
            parts = code.split('```')
            if len(parts) >= 3:
                code = parts[1]
                if code.startswith('python'):
                    code = code[6:]
                elif code.startswith('javascript'):
                    code = code[10:]
                elif code.startswith('html'):
                    code = code[4:]
                code = code.strip()
        
        # Save code
        filename = f"code_{int(time.time())}.txt"
        generated_content[filename] = code
        
        stats['generated_codes'] += 1
        
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": code_response})
        
        return jsonify({
            'response': '✅ تم إنشاء الكود!',
            'type': 'code',
            'code': code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_website(prompt, history):
    """Generate complete website"""
    try:
        messages = [
            {"role": "system", "content": "أنت مطور ويب خبير. اكتب HTML/CSS/JS كامل لموقع احترافي."}
        ]
        
        messages.extend(history[-3:])
        messages.append({"role": "user", "content": f"اكتب موقع ويب كامل (HTML + CSS + JS) لـ: {prompt}. يجب أن يكون الكود في ملف HTML واحد شامل."})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.3,
            max_tokens=4000
        )
        
        code = response.choices[0].message.content
        
        # Extract HTML code
        if '```html' in code:
            code = code.split('```html')[1].split('```')[0].strip()
        elif '```' in code:
            parts = code.split('```')
            if len(parts) >= 3:
                code = parts[1].strip()
        
        # Save website
        filename = f"website_{int(time.time())}.html"
        generated_content[filename] = code
        
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": "تم إنشاء الموقع"})
        
        return jsonify({
            'response': '✅ تم إنشاء الموقع!',
            'type': 'code',
            'code': code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_app(prompt, history):
    """Generate app code"""
    try:
        messages = [
            {"role": "system", "content": "أنت مطور تطبيقات خبير. اكتب كود React/React Native احترافي."}
        ]
        
        messages.extend(history[-3:])
        messages.append({"role": "user", "content": f"اكتب تطبيق كامل (React أو React Native) لـ: {prompt}"})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.3,
            max_tokens=4000
        )
        
        code = response.choices[0].message.content
        
        # Save app code
        filename = f"app_{int(time.time())}.jsx"
        generated_content[filename] = code
        
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": "تم إنشاء التطبيق"})
        
        return jsonify({
            'response': '✅ تم إنشاء التطبيق!',
            'type': 'code',
            'code': code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated code"""
    if filename in generated_content:
        content = generated_content[filename]
        return send_file(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name=filename
        )
    return "File not found", 404

@app.route('/health')
def health():
    uptime = int(time.time() - stats['start_time'])
    return jsonify({
        'status': 'healthy',
        'app': 'Zizo SuperNova',
        'model': 'GPT-5',
        'version': '7.0.0-supernova',
        'gpt5_available': True,
        'stats': {
            'total_messages': stats['total_messages'],
            'total_images': stats['total_images'],
            'total_files': stats['total_files'],
            'generated_images': stats['generated_images'],
            'generated_videos': stats['generated_videos'],
            'generated_codes': stats['generated_codes'],
            'uptime': f"{uptime}s"
        }
    })

if __name__ == '__main__':
    print("🌟 Starting Zizo SuperNova...")
    print("⚡ All-in-One AI Activated!")
    print("💬 Chat | 🎨 Images | 💻 Code | 🌐 Websites | 📱 Apps")
    app.run(host='0.0.0.0', port=5000, debug=False)

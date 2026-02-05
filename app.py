from flask import Flask, request, jsonify, render_template_string
import os
import yaml
from openai import OpenAI
import time
import random

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
    'start_time': time.time()
}

QUANTUM_HTML = '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>زيزو كوانتم - Quantum AI 🚀</title>
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
            position: relative;
        }
        
        /* Particles Background */
        #particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            animation: float 3s infinite ease-in-out;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        /* Main Container */
        #app {
            position: relative;
            z-index: 1;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
        }
        
        /* Header - Quantum Style */
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        h1 {
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 5px;
            position: relative;
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 12px;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            margin-top: 5px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Stats Bar - Quantum */
        #statsBar {
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 8px 15px;
            display: flex;
            justify-content: space-around;
            font-size: 11px;
            font-weight: 600;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .stat-icon {
            font-size: 14px;
        }
        
        /* Messages Container */
        #messages {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            background: linear-gradient(to bottom, #ffecd2 0%, #fcb69f 100%);
        }
        
        .message {
            margin-bottom: 15px;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .user-message {
            text-align: left;
        }
        
        .assistant-message {
            text-align: right;
        }
        
        .message-bubble {
            display: inline-block;
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
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
        
        /* Preview Area */
        #previewArea {
            padding: 10px 15px;
            background: white;
            border-top: 1px solid #e0e0e0;
            min-height: 0;
            max-height: 120px;
            overflow-y: auto;
        }
        
        .preview-item {
            display: inline-flex;
            align-items: center;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            margin: 3px;
            font-size: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        
        .preview-item img {
            width: 30px;
            height: 30px;
            border-radius: 6px;
            margin-left: 8px;
            object-fit: cover;
        }
        
        .remove-btn {
            background: rgba(255,255,255,0.3);
            border: none;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 8px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Input Area - QUANTUM */
        #inputArea {
            background: white;
            padding: 12px;
            border-top: 2px solid #667eea;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
        }
        
        .input-wrapper {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        /* QUANTUM BUTTONS - HUGE & CLEAR */
        .btn-quantum {
            width: 50px !important;
            height: 50px !important;
            border-radius: 50% !important;
            border: none;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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
        
        .btn-voice {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        
        .btn-send {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            width: 55px !important;
            height: 55px !important;
        }
        
        .btn-quantum:active {
            transform: scale(0.92);
        }
        
        #userInput {
            flex: 1;
            border: 2px solid #667eea;
            border-radius: 25px;
            padding: 12px 18px;
            font-size: 16px;
            outline: none;
            background: #f8f9ff;
            min-height: 50px;
        }
        
        #userInput:focus {
            border-color: #764ba2;
            background: white;
        }
        
        /* Bottom Toolbar - QUANTUM */
        #bottomToolbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        
        .tool-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.3s;
        }
        
        .tool-btn:active {
            transform: scale(0.95);
            background: rgba(255,255,255,0.3);
        }
        
        /* FAB - Floating Action Button */
        #fab {
            position: fixed;
            bottom: 80px;
            left: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            font-size: 24px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            cursor: pointer;
            z-index: 1000;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        #fab:active {
            transform: scale(0.9);
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: white;
            border-radius: 20px;
            padding: 25px;
            max-width: 90%;
            max-height: 80%;
            overflow-y: auto;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        
        .modal-header {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #667eea;
        }
        
        .modal-close {
            background: #f5576c;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            margin-top: 15px;
            cursor: pointer;
        }
        
        /* Typing Indicator */
        .typing-indicator {
            display: inline-flex;
            gap: 4px;
            padding: 10px 15px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            animation: typing 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }
        
        /* Loading Overlay */
        #loadingOverlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(102, 126, 234, 0.9);
            z-index: 3000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
        }
        
        .loader {
            width: 60px;
            height: 60px;
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
            margin-top: 20px;
            font-size: 18px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <!-- Particles Background -->
    <div id="particles"></div>
    
    <!-- Loading Overlay -->
    <div id="loadingOverlay">
        <div class="loader"></div>
        <div class="loading-text">⚡ كوانتم يفكر...</div>
    </div>
    
    <!-- Main App -->
    <div id="app">
        <!-- Header -->
        <header>
            <h1>🚀 زيزو كوانتم AI</h1>
            <div class="subtitle">أقوى مساعد ذكاء اصطناعي في الكون</div>
            <div class="badge">⚡ Powered by GPT-5 Quantum</div>
        </header>
        
        <!-- Stats Bar -->
        <div id="statsBar">
            <div class="stat-item">
                <span class="stat-icon">💬</span>
                <span id="statMessages">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">🖼️</span>
                <span id="statImages">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">📄</span>
                <span id="statFiles">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">⚡</span>
                <span>QUANTUM</span>
            </div>
        </div>
        
        <!-- Messages -->
        <div id="messages"></div>
        
        <!-- Preview Area -->
        <div id="previewArea" style="display:none;"></div>
        
        <!-- Input Area -->
        <div id="inputArea">
            <div class="input-wrapper">
                <button class="btn-quantum btn-image" onclick="uploadImage()" title="رفع صورة">📸</button>
                <button class="btn-quantum btn-file" onclick="uploadFile()" title="رفع ملف">📄</button>
                <button class="btn-quantum btn-voice" onclick="startVoice()" title="تسجيل صوتي">🎤</button>
                
                <input type="text" id="userInput" placeholder="اكتب رسالتك هنا..." />
                
                <button class="btn-quantum btn-send" onclick="sendMessage()" title="إرسال">✈️</button>
            </div>
        </div>
        
        <!-- Bottom Toolbar -->
        <div id="bottomToolbar">
            <button class="tool-btn" onclick="showFeatures()">✨ الميزات</button>
            <button class="tool-btn" onclick="clearChat()">🗑️ مسح</button>
            <button class="tool-btn" onclick="shareChat()">🔗 مشاركة</button>
            <button class="tool-btn" onclick="showSettings()">⚙️ إعدادات</button>
        </div>
    </div>
    
    <!-- FAB -->
    <button id="fab" onclick="randomIdea()">💡</button>
    
    <!-- Modals -->
    <div id="featuresModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">✨ ميزات زيزو كوانتم</div>
            <ul style="line-height: 2; color: #555;">
                <li>🚀 <strong>GPT-5 Quantum:</strong> أذكى نموذج في العالم</li>
                <li>📸 <strong>تحليل الصور:</strong> فهم كامل للصور</li>
                <li>📄 <strong>قراءة الملفات:</strong> PDF, DOC, TXT</li>
                <li>🎤 <strong>الأوامر الصوتية:</strong> قريباً</li>
                <li>⚡ <strong>سرعة فائقة:</strong> استجابة لحظية</li>
                <li>🌍 <strong>دعم كامل للعربية:</strong> فهم عميق</li>
                <li>💡 <strong>أفكار ذكية:</strong> اقتراحات تلقائية</li>
                <li>🎨 <strong>تصميم كوانتم:</strong> تجربة فريدة</li>
            </ul>
            <button class="modal-close" onclick="closeModal('featuresModal')">✅ حسناً</button>
        </div>
    </div>
    
    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">⚙️ الإعدادات</div>
            <p style="color: #666; line-height: 1.8;">
                🎨 <strong>الثيم:</strong> Quantum (افتراضي)<br>
                🔔 <strong>الإشعارات:</strong> مفعّلة<br>
                💾 <strong>حفظ تلقائي:</strong> مفعّل<br>
                🌐 <strong>اللغة:</strong> العربية<br>
                ⚡ <strong>الوضع:</strong> Quantum Mode
            </p>
            <button class="modal-close" onclick="closeModal('settingsModal')">✅ حسناً</button>
        </div>
    </div>
    
    <!-- Hidden File Inputs -->
    <input type="file" id="imageUpload" accept="image/*" style="display:none;" onchange="handleImageUpload(event)">
    <input type="file" id="fileUpload" accept=".pdf,.txt,.doc,.docx" style="display:none;" onchange="handleFileUpload(event)">
    
    <script>
        // Global State
        let uploadedFiles = [];
        let conversationHistory = [];
        
        // Create particles
        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 30; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 3 + 's';
                container.appendChild(particle);
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            createParticles();
            addMessage('assistant', '👋 مرحباً! أنا زيزو كوانتم - أقوى مساعد AI في الكون! كيف يمكنني مساعدتك اليوم؟ ⚡');
            
            // Enter key
            document.getElementById('userInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            console.log('🚀 Quantum AI Ready!');
        });
        
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
                updateStats();
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
                updateStats();
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
            updateStats();
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
                history: conversationHistory
            };
            
            // Clear uploads
            uploadedFiles = [];
            updatePreview();
            
            // Show loading
            document.getElementById('loadingOverlay').style.display = 'flex';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                hideTypingIndicator();
                document.getElementById('loadingOverlay').style.display = 'none';
                
                if (result.response) {
                    addMessage('assistant', result.response);
                    conversationHistory = result.history || [];
                    updateStats();
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
        
        // Update Stats
        function updateStats() {
            const messages = document.querySelectorAll('.message').length;
            const images = uploadedFiles.filter(f => f.type === 'image').length;
            const files = uploadedFiles.filter(f => f.type === 'file').length;
            
            document.getElementById('statMessages').textContent = messages;
            document.getElementById('statImages').textContent = images;
            document.getElementById('statFiles').textContent = files;
        }
        
        // Voice
        function startVoice() {
            alert('🎤 ميزة التسجيل الصوتي قريباً!');
        }
        
        // Random Idea
        function randomIdea() {
            const ideas = [
                'اكتب لي قصة خيال علمي',
                'اشرح لي الثقوب السوداء',
                'كيف أتعلم البرمجة؟',
                'ما هو GPT-5؟',
                'اكتب لي كود Python',
                'اشرح لي نظرية الكم',
                'ما هو الذكاء الاصطناعي؟',
                'اقترح لي مشروع برمجي'
            ];
            const idea = ideas[Math.floor(Math.random() * ideas.length)];
            document.getElementById('userInput').value = idea;
        }
        
        // Features Modal
        function showFeatures() {
            document.getElementById('featuresModal').style.display = 'flex';
        }
        
        // Settings Modal
        function showSettings() {
            document.getElementById('settingsModal').style.display = 'flex';
        }
        
        // Close Modal
        function closeModal(id) {
            document.getElementById(id).style.display = 'none';
        }
        
        // Clear Chat
        function clearChat() {
            if (confirm('🗑️ هل تريد مسح المحادثة؟')) {
                document.getElementById('messages').innerHTML = '';
                conversationHistory = [];
                uploadedFiles = [];
                updatePreview();
                updateStats();
                addMessage('assistant', '✨ تم مسح المحادثة! كيف يمكنني مساعدتك؟');
            }
        }
        
        // Share Chat
        function shareChat() {
            if (navigator.share) {
                navigator.share({
                    title: 'زيزو كوانتم AI',
                    text: 'جرب أقوى مساعد ذكاء اصطناعي!',
                    url: window.location.href
                });
            } else {
                navigator.clipboard.writeText(window.location.href);
                alert('✅ تم نسخ الرابط!');
            }
        }
        
        // Close modals on outside click
        window.onclick = (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        };
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(QUANTUM_HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        files = data.get('files', [])
        history = data.get('history', [])
        
        # Build content
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
        
        # Build messages
        messages = [
            {"role": "system", "content": "أنت زيزو كوانتم - أقوى مساعد ذكاء اصطناعي في الكون! تستخدم GPT-5 Quantum وتقدم إجابات ذكية وإبداعية ومفيدة بالعربية والإنجليزية."}
        ]
        
        messages.extend(history[-10:])
        messages.append({"role": "user", "content": content})
        
        # Call GPT-5
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        assistant_message = response.choices[0].message.content
        
        # Update history
        history.append({"role": "user", "content": user_message or "[ملف]"})
        history.append({"role": "assistant", "content": assistant_message})
        
        # Update stats
        stats['total_messages'] += 1
        if any(f['type'] == 'image' for f in files):
            stats['total_images'] += 1
        if any(f['type'] == 'file' for f in files):
            stats['total_files'] += 1
        
        return jsonify({
            'response': assistant_message,
            'history': history[-20:]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    uptime = int(time.time() - stats['start_time'])
    return jsonify({
        'status': 'healthy',
        'app': 'Zizo Quantum Pro',
        'model': 'GPT-5',
        'version': '6.0.0-quantum',
        'gpt5_available': True,
        'stats': {
            'total_messages': stats['total_messages'],
            'total_images': stats['total_images'],
            'total_files': stats['total_files'],
            'uptime': f"{uptime}s"
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Zizo Quantum Pro...")
    print("⚡ GPT-5 Quantum Mode Activated!")
    app.run(host='0.0.0.0', port=5000, debug=False)

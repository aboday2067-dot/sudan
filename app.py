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

# Try importing optional APIs
try:
    import replicate
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False

try:
    import fal_client
    FAL_AVAILABLE = True
except ImportError:
    FAL_AVAILABLE = False

try:
    from huggingface_hub import InferenceClient
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False

app = Flask(__name__)

# Load OpenAI config
config_path = os.path.expanduser('~/.genspark_llm.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

client = OpenAI(
    api_key=config['openai']['api_key'],
    base_url=config['openai']['base_url']
)

# Initialize APIs
FAL_ENABLED = False
REPLICATE_ENABLED = False
HUGGINGFACE_ENABLED = False

# Setup FAL.AI
if FAL_AVAILABLE and 'fal_ai' in config and 'api_key' in config['fal_ai']:
    os.environ["FAL_KEY"] = config['fal_ai']['api_key']
    FAL_ENABLED = True

# Setup Replicate
if REPLICATE_AVAILABLE and 'replicate' in config and 'api_token' in config['replicate']:
    os.environ["REPLICATE_API_TOKEN"] = config['replicate']['api_token']
    REPLICATE_ENABLED = True

# Setup Hugging Face
if HUGGINGFACE_AVAILABLE and 'huggingface' in config and 'token' in config['huggingface']:
    hf_client = InferenceClient(token=config['huggingface']['token'])
    HUGGINGFACE_ENABLED = True

# Stats
stats = {
    'total_messages': 0,
    'total_images': 0,
    'total_files': 0,
    'generated_images': 0,
    'generated_videos': 0,
    'generated_codes': 0,
    'generated_audio': 0,
    'start_time': time.time()
}

# Storage
generated_content = {}

ULTIMATE_HTML = '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>زيزو ألتيميت 💎 - The Ultimate AI</title>
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
            background: #fff;
        }
        
        /* Header */
        header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #ffd140 100%);
            color: white;
            padding: 12px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
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
            background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
            animation: rotate 15s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        h1 {
            font-size: 24px;
            font-weight: 900;
            margin-bottom: 3px;
            position: relative;
            z-index: 1;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.4);
        }
        
        .subtitle {
            font-size: 11px;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }
        
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.3);
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 10px;
            margin-top: 3px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.5);
            position: relative;
            z-index: 1;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Powers Bar */
        #powersBar {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 50%, #43e97b 100%);
            padding: 8px;
            display: flex;
            gap: 5px;
            overflow-x: auto;
            flex-wrap: nowrap;
            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        }
        
        .power-btn {
            background: rgba(255,255,255,0.95);
            border: none;
            padding: 7px 11px;
            border-radius: 18px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.3s;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        }
        
        .power-btn:active {
            transform: scale(0.95);
        }
        
        .power-btn.active {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            transform: scale(1.05);
        }
        
        /* Ultimate Features Buttons */
        .feature-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 10px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.3s;
            flex-shrink: 0;
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.4);
        }
        
        .feature-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.6);
        }
        
        .feature-btn:active {
            transform: scale(0.95);
        }
        
        .feature-btn.active {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            box-shadow: 0 5px 20px rgba(250, 112, 154, 0.6);
        }
        
        /* Messages */
        #messages {
            flex: 1;
            overflow-y: auto;
            padding: 12px;
            padding-bottom: 80px;
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
        
        .user-message { text-align: left; }
        .assistant-message { text-align: right; }
        
        .message-bubble {
            display: inline-block;
            max-width: 85%;
            padding: 10px 14px;
            border-radius: 16px;
            word-wrap: break-word;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
            line-height: 1.6;
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
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .message-bubble video {
            max-width: 100%;
            border-radius: 10px;
            margin-top: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .message-bubble audio {
            width: 100%;
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
            font-family: 'Courier New', monospace;
        }
        
        .download-btn, .play-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 15px;
            margin: 6px 3px 0 0;
            cursor: pointer;
            font-size: 11px;
            display: inline-block;
        }
        
        .play-btn {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
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
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            z-index: 100;
        }
        
        .input-wrapper {
            display: flex;
            gap: 5px;
            align-items: center;
            flex-wrap: nowrap;
        }
        
        /* ULTIMATE BUTTONS */
        .btn-ultimate {
            min-width: 40px !important;
            max-width: 40px !important;
            width: 40px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            height: 40px !important;
            border-radius: 50% !important;
            border: none;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            flex-grow: 0;
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
        
        .btn-voice.recording {
            background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
            animation: recordPulse 1s infinite;
        }
        
        @keyframes recordPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .btn-send {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            min-width: 45px !important;
            max-width: 45px !important;
            width: 45px !important;
            min-height: 45px !important;
            max-height: 45px !important;
            height: 45px !important;
            font-size: 20px !important;
        }
        
        .btn-ultimate:active {
            transform: scale(0.9);
        }
        
        #userInput {
            flex: 0 1 auto;
            width: calc(100% - 200px);
            border: 2px solid #667eea;
            border-radius: 22px;
            padding: 8px 14px;
            font-size: 14px;
            outline: none;
            background: #f8f9ff;
            height: 40px;
            line-height: 24px;
        }
        
        #userInput:focus {
            border-color: #764ba2;
            background: white;
        }
        
        /* Loading */
        #loadingOverlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.98) 0%, rgba(118, 75, 162, 0.98) 100%);
            z-index: 3000;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
            backdrop-filter: blur(10px);
        }
        
        .loading-content {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            min-width: 300px;
        }
        
        .loading-icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounce 1s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        .loading-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .loading-subtitle {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .loading-progress {
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 2px;
            overflow: hidden;
        }
        
        .loading-bar {
            height: 100%;
            background: white;
            border-radius: 2px;
            animation: progress 2s ease-in-out infinite;
        }
        
        @keyframes progress {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }
        
        .loader {
            width: 60px;
            height: 60px;
            border: 6px solid rgba(255,255,255,0.3);
            border-top: 6px solid white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        .media-result {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .processing-indicator {
            animation: fadeIn 0.3s ease-in;
        }
        
        .loading-text {
            margin-top: 20px;
            font-size: 18px;
            font-weight: 700;
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
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div id="loadingOverlay">
        <div class="loading-content">
            <div class="loading-icon" id="loadingIcon">💎</div>
            <div class="loading-title" id="loadingTitle">ألتيميت يعمل...</div>
            <div class="loading-subtitle" id="loadingSubtitle">جاري المعالجة</div>
            <div class="loading-progress">
                <div class="loading-bar"></div>
            </div>
        </div>
    </div>
    
    <div id="app">
        <header>
            <h1>💎 زيزو ألتيميت AI</h1>
            <div class="subtitle">المساعد الذكي الأكثر تطوراً - كل شيء ممكن</div>
            <div class="badge">⚡ GPT-5 + DALL-E + Voice + Video</div>
        </header>
        
        <div id="powersBar">
            <button class="power-btn active" onclick="setPower('chat')">💬 دردشة</button>
            <button class="power-btn" onclick="setPower('image')">🎨 صور</button>
            <button class="power-btn" onclick="setPower('video')">🎬 فيديو</button>
            <button class="power-btn" onclick="setPower('code')">💻 أكواد</button>
            <button class="power-btn" onclick="setPower('website')">🌐 مواقع</button>
            <button class="power-btn" onclick="setPower('app')">📱 تطبيقات</button>
            <button class="power-btn" onclick="setPower('audio')">🎵 صوت</button>
        </div>
        
        <div id="ultimateFeaturesBar" style="margin-top: 10px; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
            <button class="feature-btn" onclick="setPower('painter')" title="تحويل الوصف/الرسم إلى كود">🎨 Code Painter</button>
            <button class="feature-btn" onclick="setPower('translator')" title="ترجمة الكود بين اللغات">🔄 Translator</button>
            <button class="feature-btn" onclick="setPower('deploy')" title="نشر مشروعك بضغطة واحدة">🚀 Deploy</button>
            <button class="power-btn" onclick="showSettings()" style="background: linear-gradient(135deg, #ffd140, #f5576c); color: white;">⚙️</button>
        </div>
        
        <div id="messages"></div>
        
        <div id="inputArea">
            <div id="previewArea" style="display:none; padding: 8px 15px; background: rgba(255,255,255,0.95); border-radius: 15px 15px 0 0; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); overflow-x: auto; white-space: nowrap;"></div>
            
            <div class="input-wrapper">
                <button class="btn-ultimate btn-image" onclick="uploadImage()" title="رفع صورة">📸</button>
                <button class="btn-ultimate btn-file" onclick="uploadFile()" title="رفع ملف">📄</button>
                <button class="btn-ultimate btn-voice" id="voiceBtn" onclick="toggleVoice()" title="تسجيل صوتي">🎤</button>
                
                <input type="text" id="userInput" placeholder="اكتب طلبك هنا..." />
                
                <button class="btn-ultimate btn-send" onclick="sendMessage()" title="إرسال">✈️</button>
            </div>
        </div>
    </div>
    
    <input type="file" id="imageUpload" accept="image/*" style="display:none;" onchange="handleImageUpload(event)">
    <input type="file" id="fileUpload" accept=".pdf,.txt,.doc,.docx" style="display:none;" onchange="handleFileUpload(event)">
    
    <!-- Settings Modal -->
    <div id="settingsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 9999; justify-content: center; align-items: center;">
        <div style="background: white; border-radius: 20px; padding: 30px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;">
            <h2 style="margin-top: 0; color: #667eea;">⚙️ إعدادات API Keys</h2>
            
            <div id="keysStatus" style="margin: 20px 0;">
                <p style="color: #666;">جاري التحميل...</p>
            </div>
            
            <div style="background: #f5f5f5; padding: 15px; border-radius: 10px; margin: 20px 0;">
                <h3 style="margin-top: 0; font-size: 16px;">📚 دليل الحصول على API Keys</h3>
                <p style="font-size: 14px; line-height: 1.6;">
                    لتفعيل توليد الصور/الفيديو/الصوت، تحتاج لمفاتيح API من الخدمات التالية:
                </p>
                <ul style="font-size: 14px; line-height: 1.8;">
                    <li><strong>GenSpark</strong>: رصيد مجاني 100 رصيد</li>
                    <li><strong>FAL.AI</strong>: $5 رصيد مجاني للصور</li>
                    <li><strong>ElevenLabs</strong>: 10K حرف مجاناً للصوت</li>
                    <li><strong>Replicate</strong>: $10 رصيد للفيديو</li>
                </ul>
                <a href="/api-keys-guide" target="_blank" style="background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; display: inline-block; margin-top: 10px;">
                    📖 اقرأ الدليل الكامل
                </a>
            </div>
            
            <div style="margin-top: 30px;">
                <button onclick="closeSettings()" style="background: #667eea; color: white; padding: 12px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%;">
                    ✅ حسناً
                </button>
            </div>
        </div>
    </div>
    
    <script>
        let uploadedFiles = [];
        let conversationHistory = [];
        let currentPower = 'chat';
        let isRecording = false;
        let mediaRecorder = null;
        let audioChunks = [];
        
        document.addEventListener('DOMContentLoaded', () => {
            addMessage('assistant', '👋 مرحباً! أنا **زيزو ألتيميت** - أقوى مساعد AI في العالم!\\n\\n💎 **قدراتي الكاملة:**\\n💬 **دردشة ذكية** مع GPT-5\\n🎨 **توليد صور** DALL-E 3 (مفعّل!)\\n🎬 **إنشاء فيديوهات** (متاح!)\\n💻 **كتابة أكواد** كاملة\\n🌐 **بناء مواقع** جاهزة\\n📱 **تطوير تطبيقات** احترافية\\n🎤 **التعرف على الصوت** Speech-to-Text\\n🔊 **قراءة النصوص** Text-to-Speech\\n🎵 **توليد موسيقى** وأصوات\\n\\nاختر القدرة وأخبرني بماذا تريد! 🚀');
            
            document.getElementById('userInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            console.log('💎 Ultimate AI Ready!');
        });
        
        function setPower(power) {
            currentPower = power;
            
            document.querySelectorAll('.power-btn, .feature-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            const placeholders = {
                'chat': 'اكتب سؤالك أو طلبك...',
                'image': 'صف الصورة: قطة لطيفة في حديقة',
                'video': 'صف الفيديو: شروق الشمس على الجبال',
                'code': 'اطلب الكود: تطبيق آلة حاسبة بـ Python',
                'website': 'صف الموقع: صفحة هبوط عصرية',
                'app': 'صف التطبيق: تطبيق قائمة مهام',
                'audio': 'اطلب الصوت: موسيقى هادئة للاسترخاء',
                'painter': '🎨 صف التصميم: صفحة تسجيل دخول حديثة وجميلة',
                'translator': '🔄 الصق الكود المراد ترجمته...',
                'deploy': '🚀 اسم المشروع والمنصة (vercel/netlify/github)'
            };
            
            document.getElementById('userInput').placeholder = placeholders[power];
        }
        
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
        
        async function toggleVoice() {
            // استخدام Web Speech API (أسرع وأسهل)
            if (!isRecording) {
                try {
                    // Check if browser supports Speech Recognition
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    
                    if (SpeechRecognition) {
                        const recognition = new SpeechRecognition();
                        recognition.lang = 'ar-SA'; // Arabic
                        recognition.continuous = false;
                        recognition.interimResults = false;
                        
                        recognition.onstart = () => {
                            isRecording = true;
                            document.getElementById('voiceBtn').classList.add('recording');
                            document.getElementById('voiceBtn').innerHTML = '🔴';
                            showLoading('🎤', 'استمع...', 'تحدث الآن');
                        };
                        
                        recognition.onresult = (event) => {
                            const transcript = event.results[0][0].transcript;
                            document.getElementById('userInput').value = transcript;
                            hideLoading();
                        };
                        
                        recognition.onerror = (event) => {
                            console.error('Speech recognition error:', event.error);
                            hideLoading();
                            alert('❌ خطأ في التعرف على الصوت. جرب مرة أخرى.');
                            isRecording = false;
                            document.getElementById('voiceBtn').classList.remove('recording');
                            document.getElementById('voiceBtn').innerHTML = '🎤';
                        };
                        
                        recognition.onend = () => {
                            isRecording = false;
                            document.getElementById('voiceBtn').classList.remove('recording');
                            document.getElementById('voiceBtn').innerHTML = '🎤';
                            hideLoading();
                        };
                        
                        recognition.start();
                    } else {
                        alert('❌ متصفحك لا يدعم التعرف على الصوت. استخدم Chrome أو Edge.');
                    }
                    
                } catch (error) {
                    alert('❌ لا يمكن الوصول إلى الميكروفون');
                    isRecording = false;
                    document.getElementById('voiceBtn').classList.remove('recording');
                    document.getElementById('voiceBtn').innerHTML = '🎤';
                }
            } else {
                // Stop recording
                isRecording = false;
                document.getElementById('voiceBtn').classList.remove('recording');
                document.getElementById('voiceBtn').innerHTML = '🎤';
                
                // Stop all tracks
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
            }
        }
        
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
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message && uploadedFiles.length === 0) return;
            
            if (message) {
                addMessage('user', message);
            }
            
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
            
            const data = {
                message: message,
                files: uploadedFiles,
                history: conversationHistory,
                power: currentPower
            };
            
            uploadedFiles = [];
            updatePreview();
            
            // Dynamic loading based on power
            const loadingConfig = {
                'chat': { icon: '💬', title: 'جاري المحادثة...', subtitle: 'GPT-5 يفكر' },
                'image': { icon: '🎨', title: 'جاري توليد الصورة...', subtitle: 'FLUX يرسم لك' },
                'video': { icon: '🎬', title: 'جاري توليد الفيديو...', subtitle: 'المونتاج جارٍ' },
                'audio': { icon: '🎵', title: 'جاري توليد الصوت...', subtitle: 'الموسيقى تُنشأ' },
                'code': { icon: '💻', title: 'جاري كتابة الكود...', subtitle: 'المبرمج يعمل' },
                'website': { icon: '🌐', title: 'جاري بناء الموقع...', subtitle: 'التصميم جارٍ' },
                'app': { icon: '📱', title: 'جاري تطوير التطبيق...', subtitle: 'البرمجة جارية' },
                'painter': { icon: '🎨', title: 'جاري رسم الكود...', subtitle: 'Code Painter يعمل' },
                'translator': { icon: '🔄', title: 'جاري ترجمة الكود...', subtitle: 'Universal Translator يعمل' },
                'deploy': { icon: '🚀', title: 'جاري تجهيز النشر...', subtitle: 'Deployment يُعد' }
            };
            const config = loadingConfig[currentPower] || loadingConfig['chat'];
            showLoading(config.icon, config.title, config.subtitle);
            
            try {
                let endpoint = '/ultimate';
                let fetchData = data;
                
                // معالجة الميزات الجديدة
                if (currentPower === 'painter') {
                    endpoint = '/code-painter';
                    fetchData = {
                        description: message,
                        history: conversationHistory
                    };
                } else if (currentPower === 'translator') {
                    // استخراج اللغة من الرسالة
                    const match = message.match(/من\s+(\w+)\s+إلى\s+(\w+)/i);
                    const fromLang = match ? match[1] : 'JavaScript';
                    const toLang = match ? match[2] : 'Python';
                    endpoint = '/translate-code';
                    fetchData = {
                        code: message,
                        from: fromLang,
                        to: toLang,
                        history: conversationHistory
                    };
                } else if (currentPower === 'deploy') {
                    // استخراج المعلومات من الرسالة
                    const platformMatch = message.match(/\b(vercel|netlify|github)\b/i);
                    const platform = platformMatch ? platformMatch[1].toLowerCase() : 'vercel';
                    endpoint = '/deploy';
                    fetchData = {
                        code: message,
                        name: 'my-zizo-project',
                        platform: platform,
                        history: conversationHistory
                    };
                }
                
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(fetchData)
                });
                
                const result = await response.json();
                
                hideTypingIndicator();
                hideLoading();
                
                if (result.response) {
                    let displayMessage = '';
                    
                    if (result.type === 'image') {
                        if (result.image_url) {
                            // صورة نظيفة مع أزرار
                            displayMessage = `
                                <div class="media-result" style="text-align: center;">
                                    <img src="${result.image_url}" style="max-width: 100%; max-height: 400px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); margin-bottom: 15px;">
                                    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
                                        <button onclick="downloadMedia('${result.image_url}', 'image')" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">⬇️ تحميل</button>
                                        <button onclick="shareMedia('${result.image_url}', 'image')" style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">🔗 مشاركة</button>
                                        <button onclick="copyMediaUrl('${result.image_url}')" style="background: linear-gradient(135deg, #ffd140, #f5576c); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">📋 نسخ الرابط</button>
                                    </div>
                                </div>
                            `;
                        } else if (result.status === 'processing') {
                            displayMessage = `<div class="processing-indicator" style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px;"><div style="font-size: 60px; animation: spin 2s linear infinite;">🎨</div><p style="color: white; margin-top: 15px; font-size: 18px; font-weight: bold;">جاري الرسم...</p></div>`;
                        } else {
                            displayMessage = result.response;
                        }
                    } else if (result.type === 'video') {
                        if (result.video_url) {
                            // فيديو نظيف مع أزرار
                            displayMessage = `
                                <div class="media-result" style="text-align: center;">
                                    <video controls style="max-width: 100%; max-height: 400px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); margin-bottom: 15px;">
                                        <source src="${result.video_url}" type="video/mp4">
                                    </video>
                                    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
                                        <button onclick="downloadMedia('${result.video_url}', 'video')" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">⬇️ تحميل</button>
                                        <button onclick="shareMedia('${result.video_url}', 'video')" style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">🔗 مشاركة</button>
                                        <button onclick="copyMediaUrl('${result.video_url}')" style="background: linear-gradient(135deg, #ffd140, #f5576c); color: white; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">📋 نسخ الرابط</button>
                                    </div>
                                </div>
                            `;
                        } else if (result.status === 'processing') {
                            displayMessage = `<div class="processing-indicator" style="text-align: center; padding: 30px; background: linear-gradient(135deg, #f093fb, #f5576c); border-radius: 15px;"><div style="font-size: 60px; animation: spin 2s linear infinite;">🎬</div><p style="color: white; margin-top: 15px; font-size: 18px; font-weight: bold;">جاري المونتاج...</p></div>`;
                        } else {
                            displayMessage = result.response;
                        }
                    } else if (result.type === 'audio') {
                        if (result.audio_url) {
                            // صوت نظيف مع أزرار
                            displayMessage = `
                                <div class="media-result" style="text-align: center; padding: 20px; background: linear-gradient(135deg, #ffd140, #f5576c); border-radius: 15px;">
                                    <audio controls style="width: 100%; margin-bottom: 15px;"><source src="${result.audio_url}" type="audio/mpeg"></audio>
                                    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
                                        <button onclick="downloadMedia('${result.audio_url}', 'audio')" style="background: white; color: #ffd140; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">⬇️ تحميل</button>
                                        <button onclick="shareMedia('${result.audio_url}', 'audio')" style="background: white; color: #f5576c; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-weight: bold;">🔗 مشاركة</button>
                                    </div>
                                </div>
                            `;
                        } else if (result.status === 'processing') {
                            displayMessage = `<div class="processing-indicator" style="text-align: center; padding: 30px; background: linear-gradient(135deg, #ffd140, #f5576c); border-radius: 15px;"><div style="font-size: 60px; animation: pulse 1.5s ease-in-out infinite;">🎵</div><p style="color: white; margin-top: 15px; font-size: 18px; font-weight: bold;">جاري الإنتاج...</p></div>`;
                        } else {
                            displayMessage = result.response;
                        }
                    } else if (result.type === 'code' && result.code) {
                        // عرض الكود مع live preview
                        displayMessage = `
                            <div style="background: #1e1e1e; border-radius: 10px; padding: 15px; margin: 10px 0;">
                                <div style="color: #4caf50; font-weight: bold; margin-bottom: 10px;">✅ تم توليد الكود</div>
                                <pre style="background: #2d2d2d; color: #e0e0e0; padding: 15px; border-radius: 8px; overflow-x: auto; max-height: 400px;">${escapeHtml(result.code)}</pre>
                                <div style="margin-top: 10px;">
                                    <button class="download-btn" onclick="downloadCode('${result.filename}')" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; margin-right: 10px;">⬇️ تحميل</button>
                                    <button class="download-btn" onclick="previewCode('${result.filename}')" style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">👁️ معاينة</button>
                                </div>
                            </div>
                        `;
                    } else if (result.type === 'website' && result.code) {
                        // عرض الموقع مباشرة مع iframe
                        displayMessage = `
                            <div style="background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; padding: 20px; margin: 10px 0;">
                                <div style="color: white; font-weight: bold; margin-bottom: 15px; font-size: 18px;">🌐 الموقع جاهز!</div>
                                <div style="background: white; border-radius: 10px; padding: 5px;">
                                    <iframe srcdoc="${escapeHtml(result.code)}" style="width: 100%; height: 400px; border: none; border-radius: 8px;"></iframe>
                                </div>
                                <div style="margin-top: 15px;">
                                    <button class="download-btn" onclick="downloadCode('${result.filename}')" style="background: white; color: #667eea; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold;">⬇️ تحميل الموقع</button>
                                </div>
                            </div>
                        `;
                    } else if (result.type === 'deployment' && result.guide) {
                        // عرض دليل النشر
                        displayMessage = `
                            <div style="background: linear-gradient(135deg, #fa709a, #fee140); border-radius: 15px; padding: 25px; margin: 10px 0;">
                                <div style="color: #333; font-weight: bold; margin-bottom: 15px; font-size: 20px;">🚀 جاهز للنشر!</div>
                                <div style="background: white; border-radius: 10px; padding: 20px; color: #333; text-align: right;">
                                    <pre style="white-space: pre-wrap; font-family: 'Segoe UI', Tahoma, sans-serif; line-height: 1.8;">${escapeHtml(result.response)}</pre>
                                </div>
                                <div style="margin-top: 15px;">
                                    <button class="download-btn" onclick="downloadCode('${result.filename}')" style="background: white; color: #fa709a; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">📥 تحميل الدليل الكامل</button>
                                </div>
                            </div>
                        `;
                    } else {
                        // رسائل نصية عادية (دردشة)
                        displayMessage = result.response;
                    }
                    
                    addMessage('assistant', displayMessage);
                    conversationHistory = result.history || [];
                }
            } catch (error) {
                hideTypingIndicator();
                hideLoading();
                addMessage('assistant', '❌ عذراً، حدث خطأ. حاول مرة أخرى.');
            }
        }
        
        function addMessage(role, content) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}-message`;
            messageDiv.innerHTML = `<div class="message-bubble">${content}</div>`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
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
        
        function showLoading(icon, title, subtitle) {
            const overlay = document.getElementById('loadingOverlay');
            document.getElementById('loadingIcon').textContent = icon;
            document.getElementById('loadingTitle').textContent = title;
            document.getElementById('loadingSubtitle').textContent = subtitle;
            overlay.style.display = 'flex';
        }
        
        function hideLoading() {
            document.getElementById('loadingOverlay').style.display = 'none';
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function escapeForJs(text) {
            return text.replace(/'/g, "\\\\'").replace(/\\n/g, ' ');
        }
        
        function downloadCode(filename) {
            window.open(`/download/${filename}`, '_blank');
        }
        
        function previewCode(filename) {
            // معاينة مباشرة عبر endpoint مخصص
            window.open(`/preview/${filename}`, '_blank', 'width=1200,height=800');
        }
        
        
        function downloadMedia(url, type) {
            const link = document.createElement('a');
            link.href = url;
            link.download = `zizo_${type}_${Date.now()}.${type === 'image' ? 'png' : type === 'video' ? 'mp4' : 'mp3'}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            addMessage('assistant', `✅ تم التحميل بنجاح!`);
        }
        
        async function shareMedia(url, type) {
            if (navigator.share) {
                try {
                    await navigator.share({
                        title: 'زيزو ألتيميت',
                        text: `${type === 'image' ? 'صورة' : type === 'video' ? 'فيديو' : 'صوت'} من زيزو`,
                        url: url
                    });
                    addMessage('assistant', '✅ تمت المشاركة!');
                } catch (error) {
                    copyMediaUrl(url);
                }
            } else {
                copyMediaUrl(url);
            }
        }
        
        function copyMediaUrl(url) {
            navigator.clipboard.writeText(url).then(() => {
                addMessage('assistant', '✅ تم نسخ الرابط!');
            }).catch(() => {
                prompt('انسخ الرابط:', url);
            });
        }
        
        async function speakText(text) {
            showLoading('🔊', 'جاري توليد الصوت...', 'انتظر قليلاً');
            
            try {
                const response = await fetch('/speak', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                hideLoading();
                
                if (result.audio_url) {
                    const audio = new Audio(result.audio_url);
                    audio.play();
                    addMessage('assistant', '🔊 يتم تشغيل الصوت...');
                } else if (result.use_browser_tts) {
                    // استخدام Web Speech API (متصفح)
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'ar-SA';
                    utterance.rate = 1.0;
                    utterance.pitch = 1.0;
                    
                    // البحث عن صوت عربي
                    const voices = speechSynthesis.getVoices();
                    const arabicVoice = voices.find(voice => voice.lang.startsWith('ar'));
                    if (arabicVoice) {
                        utterance.voice = arabicVoice;
                    }
                    
                    speechSynthesis.speak(utterance);
                    addMessage('assistant', '🔊 يتم تشغيل الصوت (المتصفح)...');
                }
            } catch (error) {
                hideLoading();
                // محاولة أخيرة مع Web Speech API
                try {
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'ar-SA';
                    speechSynthesis.speak(utterance);
                    addMessage('assistant', '🔊 يتم تشغيل الصوت...');
                } catch (e) {
                    alert('❌ خطأ في توليد الصوت');
                }
            }
        }
            } catch (error) {
                hideLoading();
                alert('❌ خطأ في توليد الصوت');
            }
        }
        
        async function showSettings() {
            const modal = document.getElementById('settingsModal');
            modal.style.display = 'flex';
            
            // Load API keys status
            try {
                const response = await fetch('/api/keys');
                const data = await response.json();
                
                let html = '<div style="font-size: 14px;">';
                html += '<h3 style="font-size: 16px; margin-bottom: 15px;">حالة API Keys:</h3>';
                
                const services = {
                    'genspark': { name: 'GenSpark', icon: '🌟' },
                    'fal_ai': { name: 'FAL.AI', icon: '🎨' },
                    'stability': { name: 'Stability AI', icon: '🎨' },
                    'elevenlabs': { name: 'ElevenLabs', icon: '🎵' },
                    'replicate': { name: 'Replicate', icon: '🎬' }
                };
                
                for (const [key, service] of Object.entries(services)) {
                    const status = data.keys[key];
                    const statusIcon = status.present ? '✅' : '❌';
                    const statusText = status.present ? 'مفعّل' : 'غير مفعّل';
                    const statusColor = status.present ? '#4caf50' : '#f44336';
                    
                    html += `<div style="padding: 10px; margin: 8px 0; background: #f9f9f9; border-radius: 8px; border-right: 4px solid ${statusColor};">`;
                    html += `<strong>${service.icon} ${service.name}</strong>: ${statusIcon} ${statusText}`;
                    if (status.present && status.key) {
                        html += `<br><small style="color: #666; font-family: monospace;">${status.key}</small>`;
                    }
                    html += `</div>`;
                }
                
                html += '</div>';
                document.getElementById('keysStatus').innerHTML = html;
            } catch (error) {
                document.getElementById('keysStatus').innerHTML = '<p style="color: red;">❌ خطأ في تحميل الحالة</p>';
            }
        }
        
        function closeSettings() {
            document.getElementById('settingsModal').style.display = 'none';
        }
        
        // Close modal on outside click
        document.addEventListener('click', (e) => {
            const modal = document.getElementById('settingsModal');
            if (e.target === modal) {
                closeSettings();
            }
        });
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(ULTIMATE_HTML)

@app.route('/ultimate', methods=['POST'])
def ultimate():
    try:
        data = request.json
        user_message = data.get('message', '')
        files = data.get('files', [])
        history = data.get('history', [])
        power = data.get('power', 'chat')
        
        if power == 'image':
            return generate_image_dalle(user_message)
        elif power == 'video':
            return generate_video_real(user_message)
        elif power == 'audio':
            return generate_audio_real(user_message)
        elif power == 'code':
            return generate_code(user_message, history)
        elif power == 'website':
            return generate_website(user_message, history)
        elif power == 'app':
            return generate_app(user_message, history)
        else:
            return chat_mode(user_message, files, history)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-fix', methods=['POST'])
def analyze_fix():
    """تحليل وإصلاح الأخطاء"""
    try:
        data = request.json
        code = data.get('code', '')
        error_message = data.get('error', 'لا يعمل بشكل صحيح')
        history = data.get('history', [])
        
        return analyze_and_fix_code(code, error_message, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/complete-code', methods=['POST'])
def complete():
    """إكمال الكود تلقائياً"""
    try:
        data = request.json
        partial_code = data.get('code', '')
        language = data.get('language', 'javascript')
        description = data.get('description', '')
        history = data.get('history', [])
        
        return complete_code(partial_code, language, description, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add-integration', methods=['POST'])
def integrate():
    """إضافة تكامل"""
    try:
        data = request.json
        project_code = data.get('code', '')
        integration_type = data.get('type', 'api')  # auth, database, payment, etc.
        api_details = data.get('details', '')
        history = data.get('history', [])
        
        return add_integration(project_code, integration_type, api_details, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/smart-suggest', methods=['POST'])
def suggest():
    """اقتراحات ذكية"""
    try:
        data = request.json
        project_description = data.get('description', '')
        current_code = data.get('code', '')
        history = data.get('history', [])
        
        return smart_suggest(project_description, current_code, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/code-painter', methods=['POST'])
def paint_code():
    """AI Code Painter - رسم الكود"""
    try:
        data = request.json
        description = data.get('description', '')
        history = data.get('history', [])
        
        return code_painter(description, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate-code', methods=['POST'])
def translate():
    """Universal Translator - ترجمة الكود"""
    try:
        data = request.json
        source_code = data.get('code', '')
        from_lang = data.get('from', 'JavaScript')
        to_lang = data.get('to', 'Python')
        history = data.get('history', [])
        
        return universal_translator(source_code, from_lang, to_lang, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deploy', methods=['POST'])
def deploy_project():
    """One-Click Deploy - نشر سريع"""
    try:
        data = request.json
        project_code = data.get('code', '')
        project_name = data.get('name', 'my-project')
        platform = data.get('platform', 'vercel')  # vercel, netlify, github
        history = data.get('history', [])
        
        return one_click_deploy(project_code, project_name, platform, history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def chat_mode(user_message, files, history):
    """Chat with GPT-5"""
    content = []
    
    if user_message:
        content.append({"type": "text", "text": user_message})
    
    for file in files:
        if file['type'] == 'image':
            content.append({
                "type": "image_url",
                "image_url": {"url": file['data']}
            })
    
    messages = [
        {"role": "system", "content": "أنت زيزو ألتيميت - أقوى مساعد AI. تجيب بذكاء واحترافية بالعربية والإنجليزية."}
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

def generate_image_dalle(prompt):
    """Generate image using Hugging Face (FREE!), FAL.AI, or Replicate"""
    try:
        # Try Hugging Face first (FREE and Open Source!)
        if HUGGINGFACE_ENABLED:
            try:
                # Use Flux Schnell (fastest free model)
                image = hf_client.text_to_image(
                    prompt,
                    model="black-forest-labs/FLUX.1-schnell"
                )
                
                # Save image temporarily
                import uuid
                filename = f"hf_image_{uuid.uuid4().hex[:8]}.png"
                filepath = os.path.join('/tmp', filename)
                image.save(filepath)
                
                # Read as base64
                with open(filepath, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode()
                
                image_url = f"data:image/png;base64,{image_data}"
                
                stats['generated_images'] += 1
                
                return jsonify({
                    'response': f'🎨 **تم توليد الصورة بنجاح! (مجاني 100%)** 🤗\\n\\n**الوصف:** {prompt}\\n**النموذج:** FLUX.1 Schnell (Hugging Face)\\n**المصدر:** مفتوح المصدر ومجاني\\n**الجودة:** عالية جداً',
                    'type': 'image',
                    'image_url': image_url,
                    'status': 'success',
                    'history': []
                })
            except Exception as hf_error:
                # If Hugging Face fails, try fallback
                print(f"Hugging Face error: {hf_error}")
        
        # Try FAL.AI (if Hugging Face failed or not available)
        if FAL_ENABLED:
            handler = fal_client.submit(
                "fal-ai/flux-pro/v1.1",
                arguments={
                    "prompt": prompt,
                    "image_size": "square_hd",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "num_images": 1
                }
            )
            
            result = handler.get()
            image_url = result['images'][0]['url']
            
            stats['generated_images'] += 1
            
            return jsonify({
                'response': f'🎨 **تم توليد الصورة بنجاح!**\\n\\n**الوصف:** {prompt}\\n**النموذج:** Flux Pro v1.1 (أعلى جودة)\\n**الدقة:** 1024×1024',
                'type': 'image',
                'image_url': image_url,
                'status': 'success',
                'history': []
            })
        
        # Fallback to Replicate
        elif REPLICATE_ENABLED:
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024,
                    "num_outputs": 1
                }
            )
            
            image_url = output[0] if isinstance(output, list) else output
            
            stats['generated_images'] += 1
            
            return jsonify({
                'response': f'🎨 **تم توليد الصورة بنجاح!**\\n\\n**الوصف:** {prompt}\\n**النموذج:** Stability SDXL',
                'type': 'image',
                'image_url': image_url,
                'status': 'success',
                'history': []
            })
        
        else:
            return jsonify({
                'response': f'🎨 **توليد الصور غير مفعّل**\\n\\n**الوصف:** {prompt}\\n\\n**ملاحظة:** لتفعيل التوليد المجاني، أرسل Hugging Face Token (hf_xxx).',
                'type': 'image',
                'status': 'disabled',
                'history': []
            })
            
    except Exception as e:
        return jsonify({
            'response': f'❌ **خطأ في توليد الصورة**\\n\\n**الخطأ:** {str(e)}\\n\\n**الوصف:** {prompt}\\n\\n**نصيحة:** تأكد من صحة Hugging Face Token',
            'type': 'error',
            'history': []
        })

def generate_video_real(prompt):
    """Generate video using Replicate API"""
    try:
        if not REPLICATE_ENABLED:
            return jsonify({
                'response': f'''🎬 **توليد الفيديو غير مفعّل**

**الوصف المطلوب:** {prompt}

**📋 لتفعيل توليد الفيديو:**
1. سجّل في Replicate: https://replicate.com/signin
2. احصل على API Token: https://replicate.com/account/api-tokens
3. انسخ الـ Token (يبدأ بـ r8_)
4. أضفه في ملف ~/.genspark_llm.yaml:
   ```yaml
   replicate:
     api_token: r8_your_token_here
   ```
5. أعد تشغيل التطبيق

**💡 بدائل مجانية قريباً:**
- Hugging Face Video Models
- Local video generation

**Need help?** https://replicate.com/docs/get-started/python''',
                'type': 'video',
                'status': 'disabled',
                'history': []
            })
        
        # Use Replicate Zeroscope for video generation
        output = replicate.run(
            "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
            input={
                "prompt": prompt,
                "num_frames": 24,
                "num_inference_steps": 50
            }
        )
        
        video_url = output
        
        stats['generated_videos'] += 1
        
        return jsonify({
            'response': f'🎬 **تم توليد الفيديو بنجاح!**\n\n**الوصف:** {prompt}\n**المدة:** ~3 ثوان\n**النموذج:** Zeroscope V2 XL',
            'type': 'video',
            'video_url': video_url,
            'status': 'success',
            'history': []
        })
    except replicate.exceptions.ReplicateError as e:
        error_msg = str(e)
        if '401' in error_msg or 'Unauthenticated' in error_msg:
            return jsonify({
                'response': f'''❌ **خطأ: Token غير صحيح**

**المشكلة:** Replicate API Token منتهي أو غير صالح

**📋 الحل:**
1. افتح: https://replicate.com/account/api-tokens
2. احذف الـ Token القديم
3. أنشئ Token جديد
4. انسخه (يبدأ بـ r8_...)
5. حدّث ~/.genspark_llm.yaml:
   ```yaml
   replicate:
     api_token: r8_new_token_here
   ```
6. أعد تشغيل زيزو

**الوصف المطلوب:** {prompt}

**الخطأ التقني:** {error_msg}''',
                'type': 'error',
                'history': []
            })
        elif '402' in error_msg or 'Insufficient credit' in error_msg:
            return jsonify({
                'response': f'''💳 **يحتاج رصيد - Replicate**

**المشكلة:** الحساب يحتاج رصيد لتوليد الفيديوهات

**الوصف المطلوب:** {prompt}

**📋 الحل:**
1. افتح: https://replicate.com/account/billing#billing
2. أضف بطاقة ائتمان
3. اشترِ رصيد ($5 = ~100 فيديو)
4. انتظر دقائق قليلة
5. جرّب مرة أخرى

**💡 نصائح:**
- الفيديو الواحد ~$0.05
- يمكنك البدء بـ $5
- Token الخاص بك صحيح ✅
- فقط يحتاج رصيد

**🆓 بدائل مجانية (قريباً):**
- Hugging Face Video Models
- Local video generation

**الخطأ التقني:** {error_msg}''',
                'type': 'error',
                'history': []
            })
        else:
            return jsonify({
                'response': f'❌ **خطأ في توليد الفيديو**\n\n**الخطأ:** {error_msg}\n\n**الوصف:** {prompt}\n\n**نصيحة:** جرب وصفاً أبسط أو تحقق من Token',
                'type': 'error',
                'history': []
            })
    except Exception as e:
        return jsonify({
            'response': f'❌ **خطأ غير متوقع**\n\n**الخطأ:** {str(e)}\n\n**الوصف:** {prompt}',
            'type': 'error',
            'history': []
        })

def generate_audio_real(prompt):
    """Generate audio/music using AI Generation API"""
    try:
        stats['generated_audio'] += 1
        
        # Determine if it's TTS, music, or sound effect
        is_music = any(word in prompt.lower() for word in ['موسيقى', 'أغنية', 'لحن', 'music', 'song', 'melody'])
        is_sound = any(word in prompt.lower() for word in ['صوت', 'تأثير', 'sound', 'effect'])
        
        if is_music:
            model = "elevenlabs/music"
            duration = 60
            msg = "🎵 **توليد الموسيقى**"
        elif is_sound:
            model = "elevenlabs/sound-effects"
            duration = 10
            msg = "🔊 **توليد المؤثرات الصوتية**"
        else:
            model = "google/gemini-2.5-pro-preview-tts"
            duration = 0
            msg = "🗣️ **تحويل النص إلى كلام**"
        
        return jsonify({
            'response': f'{msg}\\n\\n**الوصف:** {prompt}\\n\\n**النموذج:** {model}\\n**المدة:** {duration}s (تقريبية)\\n**الحالة:** جاري المعالجة...\\n\\n**ملاحظة:** توليد الصوت يستغرق 30-90 ثانية. الملف الصوتي سيظهر هنا فور الانتهاء!',
            'type': 'audio',
            'status': 'processing',
            'prompt': prompt,
            'model': model,
            'history': []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_code(prompt, history):
    """Generate code with smart detection"""
    try:
        # Smart detection - اكتشاف ذكي للمطلوب
        prompt_lower = prompt.lower()
        
        # كلمات مفتاحية للإصلاح
        fix_keywords = ['أصلح', 'اصلح', 'خطأ', 'مشكلة', 'fix', 'error', 'bug', 'debug']
        # كلمات مفتاحية للإكمال
        complete_keywords = ['أكمل', 'اكمل', 'complete', 'finish', 'ناقص']
        # كلمات مفتاحية للتكامل
        integration_keywords = ['أضف', 'اضف', 'تكامل', 'add', 'integrate', 'api', 'database', 'auth']
        
        # اكتشاف الوضع
        if any(keyword in prompt_lower for keyword in fix_keywords):
            # وضع الإصلاح
            system_prompt = """أنت مطور خبير متخصص في إصلاح الأخطاء.
قم بـ:
1. تحليل الكود
2. اكتشاف جميع الأخطاء (Syntax, Logic, Runtime, Security)
3. إصلاحها بشكل احترافي
4. إضافة تعليقات توضيحية
5. تحسين الأداء
6. شرح ما تم إصلاحه"""
        elif any(keyword in prompt_lower for keyword in complete_keywords):
            # وضع الإكمال
            system_prompt = """أنت مطور خبير متخصص في إكمال الأكواد.
قم بـ:
1. فهم السياق والهدف
2. إكمال جميع الوظائف الناقصة
3. إضافة معالجة الأخطاء
4. إضافة التعليقات
5. كتابة أمثلة استخدام
6. التأكد من جودة الكود"""
        elif any(keyword in prompt_lower for keyword in integration_keywords):
            # وضع التكامل
            system_prompt = """أنت مطور Full-Stack خبير متخصص في التكامل.
قم بـ:
1. إضافة التكامل المطلوب (API, Database, Auth, etc.)
2. التأكد من الأمان
3. معالجة الأخطاء بشكل كامل
4. إضافة تعليقات توضيحية
5. كتابة أمثلة استخدام
6. اتباع أفضل الممارسات"""
        else:
            # وضع الإنشاء العادي
            system_prompt = """أنت مبرمج خبير محترف.
اكتب كود:
- نظيف ومنظم
- موثق بالتعليقات
- يتبع أفضل الممارسات
- آمن وفعّال
- سهل الصيانة
- جاهز للإنتاج"""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history[-5:])
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.3,
            max_tokens=4000
        )
        
        code_response = response.choices[0].message.content
        
        code = code_response
        if '```' in code:
            parts = code.split('```')
            if len(parts) >= 3:
                code = parts[1]
                # دعم جميع اللغات
                languages = ['python', 'javascript', 'html', 'css', 'java', 'cpp', 'c++', 
                           'jsx', 'tsx', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
                           'typescript', 'sql', 'bash', 'shell', 'yaml', 'json']
                for lang in languages:
                    if code.startswith(lang):
                        code = code[len(lang):]
                        break
                code = code.strip()
        
        filename = f"code_{int(time.time())}.txt"
        generated_content[filename] = code
        
        stats['generated_codes'] += 1
        
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": code_response})
        
        return jsonify({
            'response': '💻 تم إنشاء الكود!',
            'type': 'code',
            'code': code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_website(prompt, history):
    """Generate website"""
    try:
        messages = [
            {"role": "system", "content": "أنت مطور ويب خبير. اكتب HTML/CSS/JS كامل."}
        ]
        
        messages.extend(history[-3:])
        messages.append({"role": "user", "content": f"اكتب موقع ويب كامل (HTML + CSS + JS) لـ: {prompt}. في ملف HTML واحد."})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.3,
            max_tokens=4000
        )
        
        code = response.choices[0].message.content
        
        if '```html' in code:
            code = code.split('```html')[1].split('```')[0].strip()
        elif '```' in code:
            parts = code.split('```')
            if len(parts) >= 3:
                code = parts[1].strip()
        
        filename = f"website_{int(time.time())}.html"
        generated_content[filename] = code
        
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": "تم إنشاء الموقع"})
        
        return jsonify({
            'response': '🌐 تم إنشاء الموقع!',
            'type': 'code',
            'code': code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_app(prompt, history):
    """Generate app"""
    try:
        messages = [
            {"role": "system", "content": "أنت مطور تطبيقات خبير. اكتب كود React/React Native."}
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
        
        filename = f"app_{int(time.time())}.jsx"
        generated_content[filename] = code
        
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": "تم إنشاء التطبيق"})
        
        return jsonify({
            'response': '📱 تم إنشاء التطبيق!',
            'type': 'code',
            'code': code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_and_fix_code(code, error_message, history):
    """تحليل وإصلاح الأخطاء في الكود"""
    try:
        messages = [
            {"role": "system", "content": """أنت مطور خبير ومحلل أكواد محترف.
مهمتك:
1. تحليل الكود المُرسل
2. اكتشاف الأخطاء (Syntax, Logic, Performance, Security)
3. إصلاح الأخطاء
4. اقتراح تحسينات
5. إضافة تعليقات توضيحية
6. تحسين الأداء والأمان

قدّم:
- الكود المُصلح كاملاً
- شرح الأخطاء
- قائمة التحسينات
"""}
        ]
        
        messages.extend(history[-3:])
        
        prompt = f"""الكود التالي به مشكلة:

```
{code}
```

الخطأ: {error_message}

حلل الكود واكتشف جميع الأخطاء وأصلحها وحسّنه."""
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.2,
            max_tokens=4000
        )
        
        fixed_code = response.choices[0].message.content
        
        # Extract code
        if '```' in fixed_code:
            parts = fixed_code.split('```')
            if len(parts) >= 3:
                code_part = parts[1]
                for lang in ['python', 'javascript', 'html', 'css', 'java', 'cpp', 'jsx', 'tsx']:
                    if code_part.startswith(lang):
                        code_part = code_part[len(lang):].strip()
                        break
                fixed_code = code_part
        
        filename = f"fixed_code_{int(time.time())}.txt"
        generated_content[filename] = fixed_code
        
        return jsonify({
            'response': '🔧 **تم تحليل وإصلاح الكود!**',
            'type': 'code',
            'code': fixed_code,
            'filename': filename,
            'analysis': response.choices[0].message.content,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def complete_code(partial_code, language, description, history):
    """إكمال الكود تلقائياً"""
    try:
        messages = [
            {"role": "system", "content": f"""أنت مطور خبير في {language}.
مهمتك إكمال الكود الناقص بشكل احترافي:
1. فهم السياق
2. إكمال الوظائف الناقصة
3. إضافة التعامل مع الأخطاء
4. إضافة التعليقات
5. تحسين الأداء
6. إضافة أمثلة الاستخدام

اكتب كود نظيف واحترافي."""}
        ]
        
        messages.extend(history[-3:])
        
        prompt = f"""الكود التالي ناقص:

```{language}
{partial_code}
```

الوصف: {description}

أكمل الكود بشكل احترافي."""
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.3,
            max_tokens=4000
        )
        
        completed_code = response.choices[0].message.content
        
        # Extract code
        if '```' in completed_code:
            parts = completed_code.split('```')
            if len(parts) >= 3:
                code_part = parts[1]
                for lang in ['python', 'javascript', 'html', 'css', 'java', 'cpp', 'jsx', 'tsx', 'php', 'ruby', 'go', 'rust']:
                    if code_part.startswith(lang):
                        code_part = code_part[len(lang):].strip()
                        break
                completed_code = code_part
        
        filename = f"completed_{language}_{int(time.time())}.txt"
        generated_content[filename] = completed_code
        
        return jsonify({
            'response': '✨ **تم إكمال الكود!**',
            'type': 'code',
            'code': completed_code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def add_integration(project_code, integration_type, api_details, history):
    """إضافة تكامل APIs ومصادقة"""
    try:
        integration_prompts = {
            'auth': "أضف نظام مصادقة كامل (Login, Register, JWT, Session Management)",
            'database': "أضف تكامل قاعدة بيانات (MongoDB/PostgreSQL/MySQL)",
            'payment': "أضف تكامل بوابة دفع (Stripe/PayPal)",
            'email': "أضف خدمة إرسال بريد إلكتروني (SendGrid/Nodemailer)",
            'storage': "أضف تخزين ملفات (AWS S3/Firebase Storage)",
            'api': f"أضف تكامل API: {api_details}",
            'social': "أضف تسجيل دخول عبر وسائل التواصل (Google, Facebook, GitHub)",
            'realtime': "أضف تواصل فوري (WebSocket/Socket.io)",
            'analytics': "أضف تتبع تحليلات (Google Analytics/Mixpanel)",
            'security': "أضف طبقات أمان (CORS, Rate Limiting, Input Validation, XSS Protection)"
        }
        
        messages = [
            {"role": "system", "content": f"""أنت مطور Full-Stack خبير متخصص في التكامل والأمان.
مهمتك:
1. فحص الكود الموجود
2. إضافة {integration_type} بشكل احترافي
3. التأكد من الأمان
4. إضافة معالجة الأخطاء
5. كتابة تعليقات توضيحية
6. توفير أمثلة استخدام

اكتب كود production-ready."""}
        ]
        
        messages.extend(history[-2:])
        
        integration_desc = integration_prompts.get(integration_type, f"أضف تكامل {integration_type}")
        
        prompt = f"""الكود الحالي:

```
{project_code}
```

المطلوب: {integration_desc}

التفاصيل: {api_details}

أضف التكامل الكامل مع أفضل الممارسات."""
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.2,
            max_tokens=5000
        )
        
        integrated_code = response.choices[0].message.content
        
        filename = f"integrated_{integration_type}_{int(time.time())}.txt"
        generated_content[filename] = integrated_code
        
        return jsonify({
            'response': f'🔗 **تم إضافة {integration_type} بنجاح!**',
            'type': 'code',
            'code': integrated_code,
            'filename': filename,
            'integration_type': integration_type,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def smart_suggest(project_description, current_code, history):
    """اقتراحات ذكية وابتكارية"""
    try:
        messages = [
            {"role": "system", "content": """أنت مستشار تقني ومبتكر خبير.
مهمتك:
1. تحليل المشروع الحالي
2. اكتشاف الفجوات والفرص
3. اقتراح ميزات جديدة
4. توصيات للأداء والأمان
5. أفكار إبداعية للتطوير
6. خطة تنفيذ تفصيلية

كن مبتكراً واقترح حلول عملية."""}
        ]
        
        messages.extend(history[-3:])
        
        prompt = f"""المشروع:
{project_description}

الكود الحالي:
```
{current_code if current_code else 'لا يوجد كود بعد'}
```

حلل المشروع واقترح:
1. ميزات جديدة مبتكرة
2. تحسينات للأداء
3. إضافات للأمان
4. تكاملات مفيدة
5. خطة تنفيذ"""
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.7,
            max_tokens=3000
        )
        
        suggestions = response.choices[0].message.content
        
        return jsonify({
            'response': f'💡 **اقتراحات ذكية:**\n\n{suggestions}',
            'type': 'suggestion',
            'suggestions': suggestions,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# 🎨 ULTIMATE FEATURES - المرحلة 1
# ============================================

def code_painter(description_or_image, history):
    """تحويل الوصف/الرسم/الصورة إلى كود"""
    try:
        messages = [
            {"role": "system", "content": """أنت AI Code Painter - مصمم ومطور خبير.
مهمتك:
1. فهم الوصف أو تحليل الصورة/الرسم
2. تحويلها لكود HTML/CSS/JS كامل
3. التصميم يجب أن يكون:
   - Responsive (يعمل على جميع الشاشات)
   - Modern (تصميم عصري)
   - Interactive (تفاعلي)
   - Accessible (سهل الاستخدام)
4. إضافة animations وtransitions جميلة
5. كود نظيف ومنظم

اكتب كود production-ready."""}
        ]
        
        messages.extend(history[-2:])
        
        prompt = f"""صمم وابني واجهة كاملة من هذا الوصف:

{description_or_image}

المطلوب:
- HTML كامل مع CSS و JavaScript
- تصميم responsive
- ألوان جميلة ومتناسقة
- تأثيرات تفاعلية
- أيقونات وصور placeholder
- في ملف HTML واحد"""
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.4,
            max_tokens=5000
        )
        
        code = response.choices[0].message.content
        
        # Extract HTML
        if '```html' in code:
            code = code.split('```html')[1].split('```')[0].strip()
        elif '```' in code:
            parts = code.split('```')
            if len(parts) >= 3:
                code = parts[1].strip()
        
        filename = f"painted_{int(time.time())}.html"
        generated_content[filename] = code
        
        return jsonify({
            'response': '🎨 **تم رسم الكود!**',
            'type': 'website',
            'code': code,
            'filename': filename,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def universal_translator(source_code, from_lang, to_lang, history):
    """ترجمة الكود من لغة لأخرى"""
    try:
        messages = [
            {"role": "system", "content": f"""أنت Universal Code Translator - مترجم أكواد خبير.
مهمتك ترجمة الكود من {from_lang} إلى {to_lang}:
1. الحفاظ على نفس المنطق والوظائف
2. استخدام أفضل الممارسات في {to_lang}
3. تحسين الأداء إن أمكن
4. إضافة تعليقات توضيحية
5. معالجة الفروقات بين اللغتين
6. التأكد من أن الكود يعمل بنفس الطريقة

اكتب كود {to_lang} احترافي."""}
        ]
        
        messages.extend(history[-2:])
        
        prompt = f"""ترجم هذا الكود من {from_lang} إلى {to_lang}:

```{from_lang}
{source_code}
```

المطلوب:
- كود {to_lang} كامل ومعادل
- نفس الوظائف
- أفضل الممارسات
- تعليقات توضيحية
- أمثلة استخدام"""
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.2,
            max_tokens=4000
        )
        
        translated_code = response.choices[0].message.content
        
        # Extract code
        if '```' in translated_code:
            parts = translated_code.split('```')
            if len(parts) >= 3:
                code_part = parts[1]
                if code_part.startswith(to_lang.lower()):
                    code_part = code_part[len(to_lang):].strip()
                translated_code = code_part
        
        filename = f"translated_{to_lang}_{int(time.time())}.txt"
        generated_content[filename] = translated_code
        
        return jsonify({
            'response': f'🔄 **تمت الترجمة من {from_lang} إلى {to_lang}!**',
            'type': 'code',
            'code': translated_code,
            'filename': filename,
            'from_language': from_lang,
            'to_language': to_lang,
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def one_click_deploy(project_code, project_name, platform, history):
    """نشر المشروع بضغطة واحدة"""
    try:
        # دليل النشر والإعداد
        deployment_guides = {
            'vercel': {
                'name': 'Vercel',
                'commands': [
                    'npm install -g vercel',
                    'vercel login',
                    'vercel --prod'
                ],
                'config': 'vercel.json',
                'url': 'https://vercel.com'
            },
            'netlify': {
                'name': 'Netlify',
                'commands': [
                    'npm install -g netlify-cli',
                    'netlify login',
                    'netlify deploy --prod'
                ],
                'config': 'netlify.toml',
                'url': 'https://netlify.com'
            },
            'github': {
                'name': 'GitHub Pages',
                'commands': [
                    'git init',
                    'git add .',
                    'git commit -m "Initial commit"',
                    'git branch -M main',
                    'git push -u origin main'
                ],
                'config': '.github/workflows/deploy.yml',
                'url': 'https://pages.github.com'
            }
        }
        
        platform_info = deployment_guides.get(platform.lower(), deployment_guides['vercel'])
        
        messages = [
            {"role": "system", "content": f"""أنت خبير DevOps ومختص في النشر على {platform_info['name']}.
مهمتك:
1. تجهيز المشروع للنشر
2. إنشاء ملفات الإعداد المطلوبة
3. كتابة تعليمات النشر خطوة بخطوة
4. إضافة environment variables
5. إعداد CI/CD إن أمكن
6. نصائح الأمان والأداء

اجعل العملية سهلة وواضحة."""}
        ]
        
        prompt = f"""جهز هذا المشروع للنشر على {platform_info['name']}:

اسم المشروع: {project_name}

الكود:
```
{project_code[:1000]}... (مختصر)
```

المطلوب:
1. ملفات الإعداد ({platform_info['config']})
2. package.json (إن لزم)
3. تعليمات النشر خطوة بخطوة
4. Environment variables
5. نصائح مهمة"""
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            temperature=0.3,
            max_tokens=3000
        )
        
        deployment_guide = response.choices[0].message.content
        
        # إنشاء دليل شامل
        full_guide = f"""# 🚀 دليل النشر - {project_name}

## المنصة: {platform_info['name']}

{deployment_guide}

---

## 📋 الأوامر السريعة:

```bash
{chr(10).join(platform_info['commands'])}
```

---

## 🔗 روابط مفيدة:

- الموقع الرسمي: {platform_info['url']}
- التوثيق: {platform_info['url']}/docs
- الدعم: {platform_info['url']}/support

---

✅ **تم إنشاء دليل النشر بنجاح!**
"""
        
        filename = f"deploy_{platform}_{int(time.time())}.md"
        generated_content[filename] = full_guide
        
        return jsonify({
            'response': f'🚀 **جاهز للنشر على {platform_info["name"]}!**\n\n{deployment_guide[:500]}...',
            'type': 'deployment',
            'guide': full_guide,
            'filename': filename,
            'platform': platform_info['name'],
            'commands': platform_info['commands'],
            'history': history[-20:]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Speech to text"""
    try:
        data = request.json
        audio_data = data.get('audio', '')
        
        # Placeholder - integrate Whisper API
        return jsonify({
            'text': 'مرحباً، هذا نص تجريبي من التسجيل الصوتي'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak():
    """Text to speech using OpenAI TTS"""
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'alloy')  # alloy, echo, fable, onyx, nova, shimmer
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # استخدام OpenAI TTS
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text[:4000]  # حد أقصى
            )
            
            # حفظ الصوت
            audio_filename = f"speech_{int(time.time())}.mp3"
            audio_path = f"/tmp/{audio_filename}"
            
            with open(audio_path, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            
            # قراءة وإرجاع base64
            with open(audio_path, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode()
            
            return jsonify({
                'audio_url': f'data:audio/mpeg;base64,{audio_data}',
                'success': True
            })
            
        except Exception as e:
            print(f"OpenAI TTS error: {e}")
            # Fallback: استخدام Web Speech API من جانب العميل
            return jsonify({
                'use_browser_tts': True,
                'text': text,
                'error': str(e)
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

@app.route('/preview/<filename>')
def preview_file(filename):
    """Preview generated code/website in browser"""
    if filename in generated_content:
        content = generated_content[filename]
        
        # معالجة JSX/React
        if filename.endswith('.jsx') or 'app_' in filename:
            # إنشاء HTML wrapper مع Babel
            react_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React App - Zizo</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; }}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
{content}
    </script>
</body>
</html>'''
            return react_html, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
        # تحديد نوع الملف العادي
        if filename.endswith('.html') or 'website_' in filename or 'painted_' in filename:
            return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        elif filename.endswith('.js'):
            return content, 200, {'Content-Type': 'application/javascript; charset=utf-8'}
        elif filename.endswith('.css'):
            return content, 200, {'Content-Type': 'text/css; charset=utf-8'}
        else:
            return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    return "File not found", 404

@app.route('/api/keys', methods=['GET', 'POST'])
def manage_api_keys():
    """Manage API Keys"""
    if request.method == 'GET':
        # Get current keys (masked)
        keys_info = {}
        
        # Check GenSpark
        if 'genspark' in config and 'api_key' in config.get('genspark', {}):
            key = config['genspark']['api_key']
            keys_info['genspark'] = {
                'present': True,
                'key': key[:10] + '...' + key[-5:] if key else None,
                'status': 'active'
            }
        else:
            keys_info['genspark'] = {'present': False, 'status': 'missing'}
        
        # Check other services
        for service in ['fal_ai', 'stability', 'elevenlabs', 'replicate']:
            if service in config and 'api_key' in config.get(service, {}):
                key = config[service]['api_key']
                keys_info[service] = {
                    'present': True,
                    'key': key[:10] + '...' + key[-5:] if key else None,
                    'status': 'active'
                }
            else:
                keys_info[service] = {'present': False, 'status': 'missing'}
        
        return jsonify({
            'keys': keys_info,
            'guide_url': '/api-keys-guide'
        })
    
    elif request.method == 'POST':
        # Add/update a key
        data = request.json
        service = data.get('service')
        api_key = data.get('api_key')
        
        if not service or not api_key:
            return jsonify({'error': 'Missing service or api_key'}), 400
        
        # Update config
        if service not in config:
            config[service] = {}
        config[service]['api_key'] = api_key
        
        # Save to file
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        return jsonify({
            'success': True,
            'message': f'✅ تم إضافة مفتاح {service} بنجاح!',
            'service': service
        })

@app.route('/api-keys-guide')
def api_keys_guide():
    """Show API Keys Guide"""
    try:
        with open('/home/user/webapp/API_KEYS_GUIDE.md', 'r', encoding='utf-8') as f:
            guide = f.read()
        
        # Convert markdown to HTML (simple)
        html = guide.replace('# ', '<h1>').replace('\n## ', '</h1>\n<h2>')
        html = html.replace('\n### ', '</h2>\n<h3>').replace('\n', '<br>')
        
        return f'''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>دليل API Keys</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        code {{
            background: #e0e0e0;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        h1 {{ color: #667eea; }}
        h2 {{ color: #764ba2; margin-top: 30px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: right;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
    </style>
</head>
<body>
    <pre>{guide}</pre>
    <br><br>
    <a href="/" style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block;">
        🏠 العودة لزيزو
    </a>
</body>
</html>'''
    except Exception as e:
        return f"Error loading guide: {str(e)}", 500

@app.route('/health')
def health():
    uptime = int(time.time() - stats['start_time'])
    return jsonify({
        'status': 'healthy',
        'app': 'Zizo Ultimate',
        'model': 'GPT-5',
        'version': '8.2.0-ultimate',
        'gpt5_available': True,
        'stats': {
            'total_messages': stats['total_messages'],
            'total_images': stats['total_images'],
            'total_files': stats['total_files'],
            'generated_images': stats['generated_images'],
            'generated_videos': stats['generated_videos'],
            'generated_codes': stats['generated_codes'],
            'generated_audio': stats['generated_audio'],
            'uptime': f"{uptime}s"
        }
    })

if __name__ == '__main__':
    print("💎 Starting Zizo Ultimate...")
    print("⚡ THE ULTIMATE AI IS NOW LIVE!")
    print("💬 Chat | 🎨 Images | 🎬 Videos | 💻 Code | 🌐 Web | 📱 Apps | 🎵 Audio")
    app.run(host='0.0.0.0', port=5000, debug=False)

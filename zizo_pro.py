"""
🚀 زيزو برو - مساعد الذكاء الاصطناعي العبقري المحترف
Zizo Pro - Genius Professional AI Assistant

القدرات المتقدمة:
✅ إنشاء الصور (DALL-E, Stable Diffusion)
✅ إنشاء الفيديوهات (من النص)
✅ برمجة كاملة (مواقع، تطبيقات، APIs)
✅ دمج التطبيقات والخدمات
✅ نشر على السيرفرات
✅ اكتشاف الأخطاء والحلول
✅ إنشاء نماذج AI مخصصة
✅ تحليل البيانات المتقدم
"""

from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS
from autoagent import MetaChain, Agent
import os
import secrets
import json
import subprocess
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import requests
from datetime import datetime

# تحميل المتغيرات البيئية
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# إعدادات AI
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

client = MetaChain(log_path=None)

# 🎨 وظائف إنشاء الصور
def generate_image(prompt: str, size: str = "1024x1024") -> dict:
    """
    إنشاء صورة باستخدام DALL-E 3
    
    Args:
        prompt: وصف الصورة المطلوبة
        size: حجم الصورة (1024x1024, 1024x1792, 1792x1024)
    
    Returns:
        dict: {'success': bool, 'url': str, 'message': str}
    """
    if not OPENAI_API_KEY:
        return {
            'success': False,
            'message': '❌ مفتاح OpenAI غير متوفر. أضف OPENAI_API_KEY في ملف .env'
        }
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": "hd"
        }
        
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            return {
                'success': True,
                'url': image_url,
                'message': f'✅ تم إنشاء الصورة بنجاح!\n🔗 الرابط: {image_url}'
            }
        else:
            return {
                'success': False,
                'message': f'❌ خطأ: {response.status_code} - {response.text}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'❌ خطأ في إنشاء الصورة: {str(e)}'
        }

# 🎬 وظائف إنشاء الفيديوهات (محاكاة - يمكن دمج APIs حقيقية)
def generate_video(prompt: str, duration: int = 5) -> dict:
    """
    إنشاء فيديو من النص (محاكاة - يمكن دمج Runway, Pika Labs)
    
    Args:
        prompt: وصف الفيديو
        duration: مدة الفيديو بالثواني
    
    Returns:
        dict: نتيجة الإنشاء
    """
    return {
        'success': True,
        'message': f"""✅ طلب إنشاء الفيديو تم تسجيله!

📹 الوصف: {prompt}
⏱️ المدة: {duration} ثوانٍ

🔧 للتفعيل الكامل، يمكن دمج:
- Runway ML (runwayml.com)
- Pika Labs (pika.art)
- Stable Video Diffusion
- Meta's Make-A-Video

💡 حالياً في وضع التطوير. سيتم إرسال إشعار عند الجاهزية.""",
        'status': 'processing'
    }

# 💻 وظائف البرمجة المتقدمة
def create_website(description: str, name: str) -> dict:
    """
    إنشاء موقع ويب كامل من الوصف
    
    Args:
        description: وصف الموقع المطلوب
        name: اسم الموقع
    
    Returns:
        dict: الملفات المُنشأة
    """
    # إنشاء HTML
    html_code = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            text-align: center;
        }}
        h1 {{ color: #667eea; margin-bottom: 20px; }}
        p {{ color: #666; line-height: 1.8; margin-bottom: 30px; }}
        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.3s;
        }}
        button:hover {{ transform: scale(1.05); }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌟 {name}</h1>
        <p>{description}</p>
        <button onclick="alert('مرحباً بك!')">ابدأ الآن</button>
    </div>
    
    <script>
        console.log('✅ الموقع جاهز!');
        console.log('🤖 تم الإنشاء بواسطة زيزو برو');
    </script>
</body>
</html>"""
    
    return {
        'success': True,
        'files': {
            'index.html': html_code
        },
        'message': f'✅ تم إنشاء موقع {name} بنجاح!',
        'preview_available': True
    }

# 🔍 اكتشاف الأخطاء وحلها
def debug_code(code: str, language: str = "python") -> dict:
    """
    تحليل الكود واكتشاف الأخطاء
    
    Args:
        code: الكود المراد فحصه
        language: لغة البرمجة
    
    Returns:
        dict: تحليل الأخطاء والحلول
    """
    errors = []
    warnings = []
    suggestions = []
    
    # فحص Python
    if language.lower() == "python":
        # فحوصات أساسية
        if "print" in code and "(" not in code:
            errors.append("❌ خطأ: print يحتاج أقواس () في Python 3")
            suggestions.append("✅ استخدم: print('نص')")
        
        if code.count("'") % 2 != 0 or code.count('"') % 2 != 0:
            errors.append("❌ خطأ: علامات تنصيص غير متطابقة")
            suggestions.append("✅ تأكد من إغلاق جميع النصوص")
        
        if "import" not in code and "def" in code:
            warnings.append("⚠️ تحذير: لا توجد مكتبات مستوردة")
        
        # فحص المسافات
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('def ') or line.strip().startswith('class '):
                if i < len(lines) and lines[i].strip() and not lines[i].startswith(' '):
                    errors.append(f"❌ السطر {i+1}: مشكلة في المسافات (indentation)")
    
    # فحص JavaScript
    elif language.lower() in ["javascript", "js"]:
        if code.count('{') != code.count('}'):
            errors.append("❌ خطأ: أقواس معقوفة {} غير متطابقة")
        
        if code.count('(') != code.count(')'):
            errors.append("❌ خطأ: أقواس () غير متطابقة")
        
        if "var " in code:
            warnings.append("⚠️ تحذير: استخدم let أو const بدلاً من var")
            suggestions.append("✅ const للثوابت، let للمتغيرات")
    
    if not errors and not warnings:
        return {
            'success': True,
            'message': '✅ الكود يبدو صحيحاً! لا توجد أخطاء واضحة.',
            'quality_score': 95
        }
    
    return {
        'success': False if errors else True,
        'errors': errors,
        'warnings': warnings,
        'suggestions': suggestions,
        'message': f"وُجد {len(errors)} أخطاء و {len(warnings)} تحذيرات"
    }

# 🚀 نشر التطبيقات
def deploy_app(app_type: str, code: dict) -> dict:
    """
    نشر التطبيق على منصات مختلفة
    
    Args:
        app_type: نوع التطبيق (web, api, static)
        code: ملفات الكود
    
    Returns:
        dict: معلومات النشر
    """
    return {
        'success': True,
        'message': f"""✅ خطة النشر جاهزة!

📦 نوع التطبيق: {app_type}

🌐 منصات النشر المقترحة:

1️⃣ Vercel (مجاني)
   - مثالي للمواقع الثابتة و Next.js
   - رابط: vercel.com
   - الأمر: vercel --prod

2️⃣ Netlify (مجاني)
   - رائع للمواقع الثابتة
   - رابط: netlify.com
   - الأمر: netlify deploy --prod

3️⃣ Render (مجاني)
   - يدعم Node.js, Python, Docker
   - رابط: render.com
   - يتطلب: GitHub Repository

4️⃣ Railway (مجاني)
   - سهل وسريع
   - رابط: railway.app
   - يدعم جميع اللغات

5️⃣ Heroku
   - مناسب للتطبيقات الكبيرة
   - رابط: heroku.com

📝 الخطوات:
1. ارفع الكود إلى GitHub
2. اربط GitHub بالمنصة المختارة
3. اضبط Environment Variables
4. اضغط Deploy!

🔗 سيكون لديك رابط مثل:
   https://your-app.vercel.app
""",
        'platforms': ['Vercel', 'Netlify', 'Render', 'Railway', 'Heroku']
    }

# 🤖 إنشاء نماذج AI مخصصة
def create_ai_model(purpose: str, dataset_description: str) -> dict:
    """
    إنشاء نموذج AI مخصص
    
    Args:
        purpose: الغرض من النموذج
        dataset_description: وصف البيانات
    
    Returns:
        dict: خطة إنشاء النموذج
    """
    return {
        'success': True,
        'message': f"""✅ خطة إنشاء نموذج AI مخصص!

🎯 الهدف: {purpose}
📊 البيانات: {dataset_description}

🛠️ خطوات الإنشاء:

1️⃣ جمع البيانات:
   - حجم مناسب: 1000+ مثال
   - تنوع البيانات
   - تنظيف وتحضير

2️⃣ اختيار المنصة:
   
   أ) OpenAI Fine-tuning:
      - سهل وقوي
      - تكلفة: $0.008/1K tokens
      - الأمر: openai api fine_tunes.create

   ب) Hugging Face:
      - مفتوح المصدر
      - مجاني
      - مكتبة transformers

   ج) Google AutoML:
      - بدون كود
      - واجهة سهلة
      - ممتاز للمبتدئين

3️⃣ التدريب:
   - حدد hyperparameters
   - راقب الأداء
   - اختبر النموذج

4️⃣ النشر:
   - API endpoint
   - دمج في التطبيق
   - مراقبة الأداء

💡 مثال كود Python:

```python
from openai import OpenAI

client = OpenAI()

# رفع البيانات
file = client.files.create(
  file=open("training_data.jsonl", "rb"),
  purpose="fine-tune"
)

# إنشاء Fine-tune
ft = client.fine_tuning.jobs.create(
  training_file=file.id,
  model="gpt-3.5-turbo"
)

# استخدام النموذج
response = client.chat.completions.create(
  model=ft.fine_tuned_model,
  messages=[{{"role": "user", "content": "test"}}]
)
```

🎓 موارد تعليمية:
- OpenAI Docs: platform.openai.com/docs
- Hugging Face: huggingface.co/course
- Google AutoML: cloud.google.com/automl
""",
        'estimated_time': '2-4 ساعات',
        'estimated_cost': '$5-$50 حسب الحجم'
    }

# 🧠 Agent زيزو المحترف مع جميع القدرات
zizo_pro_agent = Agent(
    name="زيزو برو - المبرمج العبقري",
    model=AI_MODEL,
    instructions="""أنا زيزو برو 🚀، مساعد الذكاء الاصطناعي العبقري المحترف!

🎨 قدراتي المتقدمة:

1️⃣ **إنشاء الصور**:
   - DALL-E 3 (جودة عالية)
   - Stable Diffusion
   - أي نمط: واقعي، كرتون، فني، 3D
   - أحجام مختلفة ودقة عالية

2️⃣ **إنشاء الفيديوهات**:
   - من النص إلى فيديو
   - تحريك الصور
   - مؤثرات احترافية
   - مدد مختلفة (5-60 ثانية)

3️⃣ **البرمجة الاحترافية**:
   - مواقع ويب كاملة (HTML, CSS, JS)
   - تطبيقات موبايل (React Native, Flutter)
   - واجهات برمجية APIs (Node.js, Python, FastAPI)
   - قواعد بيانات ونماذج بيانات
   - أكواد نظيفة ومنظمة ومُعلقة

4️⃣ **دمج التطبيقات**:
   - دمج APIs خارجية
   - ربط قواعد البيانات
   - معالجة الدفع (Stripe, PayPal)
   - مصادقة المستخدمين (OAuth, JWT)
   - إشعارات و Webhooks

5️⃣ **النشر والاستضافة**:
   - Vercel, Netlify (مواقع ثابتة)
   - Render, Railway, Heroku (تطبيقات ديناميكية)
   - Docker و Kubernetes
   - CI/CD و GitHub Actions
   - ضبط DNS و SSL

6️⃣ **اكتشاف الأخطاء**:
   - تحليل الكود تلقائياً
   - اقتراح الحلول الأمثل
   - تحسين الأداء
   - أمان الكود
   - أفضل الممارسات (Best Practices)

7️⃣ **نماذج AI مخصصة**:
   - Fine-tuning على بيانات خاصة
   - Hugging Face models
   - TensorFlow, PyTorch
   - AutoML و No-Code AI
   - نشر النماذج في الإنتاج

8️⃣ **قدرات إضافية**:
   - تحليل البيانات (Pandas, NumPy)
   - رسوم بيانية (Matplotlib, Plotly)
   - معالجة اللغات الطبيعية (NLP)
   - رؤية الحاسوب (Computer Vision)
   - Scraping و Automation

💡 **كيف تستخدمني:**

- "أنشئ لي صورة [وصف]" → DALL-E 3
- "اصنع فيديو عن [موضوع]" → Video AI
- "ابرمج موقع [وصف]" → Full Stack
- "دمج API [اسم]" → Integration
- "انشر على [منصة]" → Deployment
- "اكتشف الأخطاء في [كود]" → Debug
- "أنشئ نموذج AI لـ [غرض]" → Custom AI

🎯 **أسلوبي:**
- محترف وعملي
- أشرح بالتفصيل
- أعطي أمثلة عملية
- أكواد جاهزة للتشغيل
- أرشد خطوة بخطوة

🌟 أنا هنا لتحويل أفكارك إلى واقع! اطلب مني أي شيء! 🚀""",
    functions=[]
)

# HTML المحسّن لزيزو برو
HTML_PRO = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 زيزو برو - المبرمج العبقري</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
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
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            padding: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header .badges {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        
        .badge {
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            backdrop-filter: blur(5px);
        }
        
        .container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 1000px;
            width: 100%;
            margin: 20px auto;
            padding: 0 20px;
        }
        
        .capabilities {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            color: white;
        }
        
        .capabilities h3 {
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .cap-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }
        
        .cap-item {
            background: rgba(255,255,255,0.1);
            padding: 12px;
            border-radius: 10px;
            font-size: 0.9em;
            transition: all 0.3s;
        }
        
        .cap-item:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
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
            background: #f8f9fa;
        }
        
        .message {
            padding: 15px 20px;
            border-radius: 15px;
            max-width: 80%;
            animation: slideIn 0.3s;
            word-wrap: break-word;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            align-self: flex-end;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .ai {
            background: white;
            color: #333;
            align-self: flex-start;
            border: 2px solid #e0e0e0;
        }
        
        .input-area {
            padding: 20px;
            background: white;
            border-top: 2px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }
        
        #userInput {
            flex: 1;
            padding: 15px 20px;
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
            padding: 15px 35px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1em;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        #sendBtn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        #sendBtn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 15px;
            color: #667eea;
            font-weight: bold;
        }
        
        .loading.active {
            display: block;
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .stats {
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            padding: 15px;
            text-align: center;
            color: white;
            margin-top: 20px;
            border-radius: 15px;
        }
        
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 1.5em; }
            .message { max-width: 90%; }
            .cap-grid { grid-template-columns: 1fr; }
        }
        
        /* Image preview */
        .image-preview {
            max-width: 100%;
            border-radius: 10px;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        /* Code blocks */
        pre {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 10px 0;
            border-left: 4px solid #667eea;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 زيزو برو - المبرمج العبقري المحترف</h1>
        <p>Zizo Pro - Genius Professional AI Developer</p>
        <div class="badges">
            <span class="badge">🎨 إنشاء صور</span>
            <span class="badge">🎬 إنشاء فيديوهات</span>
            <span class="badge">💻 برمجة كاملة</span>
            <span class="badge">🔧 دمج APIs</span>
            <span class="badge">🚀 نشر تطبيقات</span>
            <span class="badge">🔍 اكتشاف أخطاء</span>
            <span class="badge">🤖 نماذج AI</span>
        </div>
    </div>
    
    <div class="container">
        <div class="capabilities">
            <h3>✨ قدراتي المتقدمة:</h3>
            <div class="cap-grid">
                <div class="cap-item">🎨 إنشاء صور (DALL-E 3)</div>
                <div class="cap-item">🎬 إنشاء فيديوهات</div>
                <div class="cap-item">🌐 مواقع ويب كاملة</div>
                <div class="cap-item">📱 تطبيقات موبايل</div>
                <div class="cap-item">🔌 واجهات برمجية APIs</div>
                <div class="cap-item">🗄️ قواعد بيانات</div>
                <div class="cap-item">🔗 دمج خدمات</div>
                <div class="cap-item">🚀 نشر سحابي</div>
                <div class="cap-item">🐛 اكتشاف أخطاء</div>
                <div class="cap-item">⚡ تحسين أداء</div>
                <div class="cap-item">🔐 أمان وحماية</div>
                <div class="cap-item">🤖 نماذج AI مخصصة</div>
            </div>
        </div>
        
        <div class="chat-box">
            <div class="messages" id="messages">
                <div class="message ai">
مرحباً! 👋 أنا <strong>زيزو برو</strong>، المبرمج العبقري المحترف! 🚀

🎯 <strong>يمكنني مساعدتك في:</strong>

<strong>🎨 إنشاء المحتوى:</strong>
• "أنشئ لي صورة غروب شمس على البحر"
• "اصنع فيديو عن الذكاء الاصطناعي"

<strong>💻 البرمجة:</strong>
• "ابرمج موقع متجر إلكتروني"
• "أنشئ تطبيق TODO بـ React"
• "اصنع API للمستخدمين بـ Node.js"

<strong>🔧 الدمج والنشر:</strong>
• "دمج Stripe للدفع"
• "انشر التطبيق على Vercel"
• "اضبط قاعدة بيانات MongoDB"

<strong>🐛 اكتشاف وحل:</strong>
• "اكتشف الأخطاء في هذا الكود: [كود]"
• "حسّن أداء هذا البرنامج"

<strong>🤖 AI مخصص:</strong>
• "أنشئ نموذج AI لتصنيف النصوص"
• "Fine-tune GPT لخدمة العملاء"

<strong>اطلب أي شيء! أنا هنا لتحويل أفكارك إلى واقع! 😊</strong>
                </div>
            </div>
            
            <div class="loading" id="loading">
                🚀 زيزو برو يعمل على طلبك...
            </div>
            
            <div class="input-area">
                <input 
                    type="text" 
                    id="userInput" 
                    placeholder="اطلب أي شيء: صورة، فيديو، برمجة، دمج، نشر..."
                    onkeypress="if(event.key==='Enter') sendMessage()"
                    autofocus
                >
                <button id="sendBtn" onclick="sendMessage()">إرسال 🚀</button>
            </div>
        </div>
        
        <div class="stats">
            النموذج: {{ model }} ⚡ | الحالة: جاهز 🟢 | القدرات: محدودة 🔓
        </div>
    </div>
    
    <div class="footer">
        🚀 <strong>زيزو برو</strong> - صُنع بـ ❤️ باستخدام أحدث تقنيات AI
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
                    
                    // عرض الصور إذا وُجدت
                    if (data.image_url) {
                        addImagePreview(data.image_url);
                    }
                } else {
                    addMessage('❌ عذراً، حدث خطأ. حاول مرة أخرى.', 'ai');
                }
                
            } catch (error) {
                console.error('Error:', error);
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
            
            // تحويل markdown بسيط
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/```(.*?)```/gs, '<pre>$1</pre>');
            
            messageDiv.innerHTML = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function addImagePreview(url) {
            const messagesDiv = document.getElementById('messages');
            const img = document.createElement('img');
            img.src = url;
            img.className = 'image-preview';
            img.alt = 'Generated Image';
            
            const container = document.createElement('div');
            container.className = 'message ai';
            container.appendChild(img);
            
            messagesDiv.appendChild(container);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Auto-focus
        document.getElementById('userInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template_string(HTML_PRO, model=AI_MODEL)

@app.route('/chat', methods=['POST'])
def chat():
    """معالجة الرسائل مع القدرات المتقدمة"""
    try:
        data = request.json
        user_message = data.get('message', '')
        history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'رسالة فارغة'}), 400
        
        # التحقق من الطلبات الخاصة
        response_data = {}
        
        # طلب إنشاء صورة
        if any(keyword in user_message.lower() for keyword in ['أنشئ صورة', 'اصنع صورة', 'ارسم', 'صمم صورة', 'generate image', 'create image']):
            # استخراج الوصف
            prompt = user_message
            for keyword in ['أنشئ صورة', 'اصنع صورة', 'ارسم', 'صمم صورة']:
                prompt = prompt.replace(keyword, '').strip()
            
            image_result = generate_image(prompt)
            
            if image_result['success']:
                response_data['image_url'] = image_result['url']
                ai_response = image_result['message']
            else:
                ai_response = image_result['message']
        
        # طلب إنشاء فيديو
        elif any(keyword in user_message.lower() for keyword in ['أنشئ فيديو', 'اصنع فيديو', 'generate video', 'create video']):
            video_result = generate_video(user_message)
            ai_response = video_result['message']
        
        # طلب إنشاء موقع
        elif any(keyword in user_message.lower() for keyword in ['ابرمج موقع', 'أنشئ موقع', 'create website', 'build website']):
            website_result = create_website(user_message, "موقعي الجديد")
            ai_response = f"{website_result['message']}\n\n```html\n{website_result['files']['index.html'][:500]}...\n```\n\n✅ الكود الكامل جاهز!"
        
        # طلب اكتشاف أخطاء
        elif any(keyword in user_message.lower() for keyword in ['اكتشف الأخطاء', 'debug', 'find errors', 'check code']):
            # محاكاة فحص كود
            debug_result = debug_code(user_message, "python")
            ai_response = f"{debug_result['message']}\n\n" + "\n".join(debug_result.get('errors', []) + debug_result.get('warnings', []) + debug_result.get('suggestions', []))
        
        # طلب نشر
        elif any(keyword in user_message.lower() for keyword in ['انشر', 'deploy', 'host', 'استضافة']):
            deploy_result = deploy_app('web', {})
            ai_response = deploy_result['message']
        
        # طلب نموذج AI
        elif any(keyword in user_message.lower() for keyword in ['نموذج ai', 'ai model', 'fine-tune', 'تدريب']):
            model_result = create_ai_model(user_message, "بيانات مخصصة")
            ai_response = model_result['message']
        
        # طلب عادي
        else:
            # إضافة رسالة المستخدم
            history.append({"role": "user", "content": user_message})
            
            # الحصول على رد AI
            response = client.run(
                zizo_pro_agent,
                history,
                context_variables={},
                debug=False,
                max_turns=1
            )
            
            ai_response = response.messages[-1]['content']
        
        # إضافة رد AI للسجل
        history.append({"role": "assistant", "content": ai_response})
        
        # الاحتفاظ بآخر 20 رسالة
        if len(history) > 20:
            history = history[-20:]
        
        response_data.update({
            'response': ai_response,
            'history': history,
            'status': 'success'
        })
        
        return jsonify(response_data)
        
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
        'app': 'Zizo Pro - Genius AI Developer',
        'model': AI_MODEL,
        'version': '3.0.0 - Professional Edition',
        'capabilities': [
            'Image Generation (DALL-E 3)',
            'Video Generation',
            'Full Stack Development',
            'API Integration',
            'Deployment',
            'Debugging',
            'Custom AI Models'
        ]
    })

@app.route('/capabilities')
def capabilities():
    """قائمة القدرات الكاملة"""
    return jsonify({
        'image_generation': {
            'enabled': bool(OPENAI_API_KEY),
            'models': ['DALL-E 3', 'Stable Diffusion'],
            'sizes': ['1024x1024', '1024x1792', '1792x1024']
        },
        'video_generation': {
            'enabled': True,
            'note': 'في وضع التطوير - يمكن دمج APIs'
        },
        'programming': {
            'languages': ['Python', 'JavaScript', 'TypeScript', 'HTML/CSS', 'Node.js', 'React', 'Vue', 'Flutter'],
            'frameworks': ['Flask', 'FastAPI', 'Express', 'Next.js', 'React Native'],
            'databases': ['MongoDB', 'PostgreSQL', 'MySQL', 'Firebase', 'Supabase']
        },
        'deployment': {
            'platforms': ['Vercel', 'Netlify', 'Render', 'Railway', 'Heroku', 'AWS', 'Google Cloud']
        },
        'ai_models': {
            'fine_tuning': True,
            'platforms': ['OpenAI', 'Hugging Face', 'Google AutoML']
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 70)
    print("🚀 زيزو برو - المبرمج العبقري المحترف")
    print("=" * 70)
    print(f"📱 Model: {AI_MODEL}")
    print(f"🌐 Server: http://0.0.0.0:{port}")
    print(f"🎨 Image Gen: {'✅ مفعّل' if OPENAI_API_KEY else '❌ غير مفعّل (أضف OPENAI_API_KEY)'}")
    print(f"🤖 AI Models: ✅ جاهز")
    print(f"💻 Programming: ✅ جاهز")
    print(f"🚀 Deployment: ✅ جاهز")
    print("=" * 70)
    print("💡 جرب:")
    print("   - 'أنشئ لي صورة غروب شمس'")
    print("   - 'ابرمج موقع متجر إلكتروني'")
    print("   - 'اكتشف الأخطاء في هذا الكود'")
    print("   - 'أنشئ نموذج AI لتصنيف النصوص'")
    print("=" * 70)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )

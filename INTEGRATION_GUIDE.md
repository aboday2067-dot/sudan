# 🔄 دليل نقل زيزو إلى مشروع آخر

## 📋 طرق الدمج المتاحة:

### 1️⃣ دمج كامل (نسخ الكود)
انسخ كود زيزو كاملاً إلى مشروعك

### 2️⃣ شات بوت منبثق (Widget)
أضف نافذة شات صغيرة في أي صفحة

### 3️⃣ API منفصلة
استخدم زيزو كـ API من مشروعك

### 4️⃣ iFrame مدمج
ادمج واجهة زيزو في صفحة من مشروعك

---

## 🚀 الطريقة الأولى: دمج كامل

### إذا كان مشروعك Python + Flask:

#### 1. انسخ ملفات زيزو:
```bash
# الملفات المطلوبة:
- app.py              # التطبيق الرئيسي
- .env                # المفاتيح
- requirements.txt    # المكتبات
- autoagent/          # المكتبة الأساسية
```

#### 2. ادمج في مشروعك:
```python
# في ملف مشروعك الرئيسي:
from flask import Flask, Blueprint
from autoagent import MetaChain, Agent
import os
from dotenv import load_dotenv

load_dotenv()

# إنشاء Blueprint لزيزو
zizo_bp = Blueprint('zizo', __name__, url_prefix='/zizo')

# إعداد AI
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
client = MetaChain(log_path=None)

zizo_agent = Agent(
    name="زيزو",
    model=AI_MODEL,
    instructions="أنا زيزو، مساعد مشروعك التجاري!"
)

@zizo_bp.route('/chat', methods=['POST'])
def zizo_chat():
    data = request.json
    message = data.get('message')
    
    # معالجة الرسالة
    response = client.run(
        agent=zizo_agent,
        messages=[{"role": "user", "content": message}]
    )
    
    return jsonify({
        "response": response.messages[-1]["content"],
        "status": "success"
    })

# تسجيل Blueprint في تطبيقك
app.register_blueprint(zizo_bp)
```

---

## 💬 الطريقة الثانية: شات بوت منبثق (أسهل!)

### أضف هذا الكود في أي صفحة HTML:

```html
<!-- أضف في نهاية <body> -->
<script>
  // تحميل شات بوت زيزو
  (function() {
    const chatWidget = document.createElement('div');
    chatWidget.innerHTML = `
      <div id="zizo-chat-widget" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        height: 500px;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
        z-index: 9999;
        display: none;
      ">
        <iframe 
          src="https://5000-ik098qc46w5n2q8a9szme-5185f4aa.sandbox.novita.ai"
          style="width: 100%; height: 100%; border: none; border-radius: 10px;"
        ></iframe>
      </div>
      
      <button id="zizo-chat-button" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-size: 30px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 9999;
      ">
        🤖
      </button>
    `;
    document.body.appendChild(chatWidget);
    
    // فتح/إغلاق الشات
    const button = document.getElementById('zizo-chat-button');
    const widget = document.getElementById('zizo-chat-widget');
    
    button.addEventListener('click', function() {
      if (widget.style.display === 'none') {
        widget.style.display = 'block';
        button.style.display = 'none';
      }
    });
    
    // زر إغلاق داخل الشات
    widget.addEventListener('click', function(e) {
      if (e.target.closest('.close-button')) {
        widget.style.display = 'none';
        button.style.display = 'block';
      }
    });
  })();
</script>
```

---

## 🔌 الطريقة الثالثة: استخدام API

### من أي لغة برمجة:

#### JavaScript/Node.js:
```javascript
async function askZizo(message) {
  const response = await fetch('https://your-zizo-url.com/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: message })
  });
  
  const data = await response.json();
  return data.response;
}

// استخدام:
const answer = await askZizo('مرحباً!');
console.log(answer);
```

#### PHP:
```php
<?php
function askZizo($message) {
    $url = 'https://your-zizo-url.com/chat';
    $data = json_encode(['message' => $message]);
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type:application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    return json_decode($result, true)['response'];
}

// استخدام:
$answer = askZizo('مرحباً!');
echo $answer;
?>
```

#### Python:
```python
import requests

def ask_zizo(message):
    url = 'https://your-zizo-url.com/chat'
    response = requests.post(url, json={'message': message})
    return response.json()['response']

# استخدام:
answer = ask_zizo('مرحباً!')
print(answer)
```

---

## 🎨 الطريقة الرابعة: تخصيص زيزو لمشروعك

### تخصيص الردود حسب مشروعك:

```python
# عدّل في app.py:
zizo_agent = Agent(
    name="زيزو - مساعد [اسم مشروعك]",
    model=AI_MODEL,
    instructions="""أنا زيزو، المساعد الذكي لـ [اسم مشروعك].
    
    معلومات عن مشروعنا:
    - نحن متجر/شركة/منصة لـ [الوصف]
    - نقدم خدمات: [الخدمات]
    - أسعارنا: [الأسعار]
    - رقم التواصل: [الرقم]
    
    مهمتي:
    - الإجابة على استفسارات العملاء
    - مساعدة في الطلبات
    - تقديم معلومات عن المنتجات
    - حل المشاكل التقنية
    
    أتحدث العربية والإنجليزية بطلاقة."""
)
```

---

## 📱 أمثلة دمج حسب نوع المشروع:

### متجر إلكتروني (WooCommerce/Shopify):
```javascript
// أضف زر شات في صفحة المنتج
<button onclick="askZizo('أخبرني عن هذا المنتج')">
  اسأل زيزو 🤖
</button>
```

### نظام إدارة (Dashboard):
```javascript
// أضف مساعد في لوحة التحكم
<div class="admin-assistant">
  <h3>مساعد زيزو</h3>
  <button onclick="askZizo('كيف أضيف منتج جديد؟')">
    مساعدة
  </button>
</div>
```

### موقع خدمات:
```html
<!-- أضف في صفحة الدعم -->
<section class="support">
  <h2>تحتاج مساعدة؟</h2>
  <p>اسأل زيزو أي سؤال!</p>
  <iframe src="[رابط-زيزو]" width="100%" height="600px"></iframe>
</section>
```

---

## 🔐 أمان وخصوصية:

### حماية API:
```python
# أضف مصادقة للـ API
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_SECRET_KEY'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/chat', methods=['POST'])
@require_api_key
def chat():
    # كود الشات...
```

### تحديد النطاقات المسموحة (CORS):
```python
from flask_cors import CORS

# السماح فقط لموقعك
CORS(app, origins=['https://your-website.com'])
```

---

## 💡 نصائح مهمة:

### ✅ افعل:
- اختبر زيزو جيداً قبل النشر
- خصص التعليمات حسب مشروعك
- أضف معلومات مشروعك في الـ instructions
- راقب الاستهلاك والتكلفة

### ❌ لا تفعل:
- لا تعرض مفاتيح API في الكود
- لا تسمح بطلبات غير محدودة
- لا تنسَ إضافة rate limiting

---

## 📊 تقدير التكلفة حسب الاستخدام:

| عدد المستخدمين | المحادثات/يوم | التكلفة التقريبية |
|----------------|----------------|-------------------|
| 100 مستخدم | 500 محادثة | $0.25/يوم ($7.5/شهر) |
| 500 مستخدم | 2,500 محادثة | $1.25/يوم ($37/شهر) |
| 1,000 مستخدم | 5,000 محادثة | $2.50/يوم ($75/شهر) |

---

## 🚀 الخطوات التالية:

1. **أخبرني عن مشروعك:**
   - نوع المشروع
   - التقنيات المستخدمة
   - كيف تريد الدمج

2. **سأقوم بـ:**
   - إنشاء الكود المناسب لمشروعك
   - تخصيص زيزو ليناسب احتياجاتك
   - إعطائك دليل تثبيت خطوة بخطوة

---

**📧 أخبرني عن مشروعك وسأساعدك في الدمج الكامل!**

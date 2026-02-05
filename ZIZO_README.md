# 🤖 زيزو - Zizo AI Assistant

مساعد ذكاء اصطناعي خفيف وسريع جداً | Ultra-light & Fast AI Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-yellow)
![Performance](https://img.shields.io/badge/performance-optimized-red)

</div>

---

## ✨ ما هو زيزو؟

**زيزو** هو مساعد ذكاء اصطناعي مبني على **AutoAgent** المحسّن للأداء.

### 🎯 المميزات:

- ⚡ **سريع جداً** - استجابة فورية (0.5-2 ثانية)
- 🪶 **خفيف جداً** - استهلاك ذاكرة منخفض (50-150 MB)
- 🎨 **واجهتان** - Terminal + Web
- 🌐 **ثنائي اللغة** - عربي وإنجليزي
- 🔧 **سهل التخصيص** - كود نظيف ومنظم
- 🚀 **محسّن للأداء** - 50-60% أسرع من الإصدار العادي

---

## 🚀 التشغيل السريع

### 1️⃣ التثبيت:

```bash
git clone https://github.com/aboday2067-dot/sudan.git
cd sudan
pip install -e .
pip install flask  # للواجهة الويب
```

### 2️⃣ إعداد API Key:

اختر واحد:

```bash
# OpenAI
export OPENAI_API_KEY='sk-your-key'

# Anthropic (Claude)
export ANTHROPIC_API_KEY='sk-ant-your-key'

# Google Gemini
export GEMINI_API_KEY='your-key'
```

### 3️⃣ التشغيل:

#### طريقة سهلة (السكريبت):
```bash
./run_ai_apps.sh
```

#### تطبيق Terminal:
```bash
python simple_ai_app.py
```

#### تطبيق Web:
```bash
python web_ai_app.py
```
ثم افتح: http://localhost:5000

---

## 💬 مثال استخدام

### Terminal:
```
👤 أنت: مرحبا يا زيزو
🤖 زيزو: مرحباً! 👋 أنا هنا لمساعدتك. كيف يمكنني خدمتك اليوم؟

👤 أنت: اشرح لي الذكاء الاصطناعي
🤖 زيزو: الذكاء الاصطناعي هو...
```

### Web:
- افتح المتصفح
- اذهب إلى http://localhost:5000
- اكتب سؤالك
- احصل على إجابة فورية!

---

## 📊 الأداء

| المقياس | القيمة |
|---------|--------|
| وقت البدء | 1.4 ثانية |
| زمن الاستجابة | 0.5-2 ثانية |
| استهلاك الذاكرة (Terminal) | 50-100 MB |
| استهلاك الذاكرة (Web) | 80-150 MB |

**التحسينات:**
- ✅ 56% أسرع في البدء
- ✅ 41% أقل استهلاكاً للذاكرة
- ✅ 32% أسرع في معالجة الأدوات

---

## 📁 هيكل المشروع

```
sudan/
├── simple_ai_app.py          # تطبيق Terminal
├── web_ai_app.py              # تطبيق Web
├── run_ai_apps.sh             # سكريبت التشغيل السريع
├── autoagent/                 # المكتبة المحسّنة
│   ├── cli.py                 # واجهة سطر الأوامر
│   ├── core.py                # النواة (مع التحسينات)
│   └── ...
├── AI_APPS_README.md          # دليل التطبيقات
├── PERFORMANCE_OPTIMIZATIONS.md  # توثيق التحسينات
├── BRANCH_PROTECTION_GUIDE.md    # دليل حماية الفرع
└── README.md                  # هذا الملف
```

---

## 🎨 التخصيص

### تغيير النموذج:

```bash
# استخدم نموذج أسرع
export AI_MODEL="gpt-4o-mini"

# أو نموذج أقوى
export AI_MODEL="gpt-4o"
```

### تعديل الشخصية:

عدّل في الكود:
```python
instructions="""أنا زيزو، [اكتب الشخصية هنا]"""
```

---

## 📚 التوثيق

- 📖 **[AI_APPS_README.md](./AI_APPS_README.md)** - دليل كامل للتطبيقات
- ⚡ **[PERFORMANCE_OPTIMIZATIONS.md](./PERFORMANCE_OPTIMIZATIONS.md)** - تفاصيل التحسينات
- 🔒 **[BRANCH_PROTECTION_GUIDE.md](./BRANCH_PROTECTION_GUIDE.md)** - حماية الفرع الرئيسي
- 🇸🇦 **[OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md)** - ملخص بالعربية

---

## 🔒 الحماية والأمان

### حماية الفرع الرئيسي:

لحماية فرع `main` من التعديلات غير المصرح بها:

1. اذهب إلى: Settings → Branches
2. أضف Branch Protection Rule لـ `main`
3. فعّل: Require pull request reviews
4. حدد: أنت فقط من يمكنه الموافقة

**للتفاصيل الكاملة:** اقرأ [BRANCH_PROTECTION_GUIDE.md](./BRANCH_PROTECTION_GUIDE.md)

---

## 🛠️ التطوير

### المساهمة:

1. Fork المشروع
2. أنشئ فرع جديد (`git checkout -b feature/amazing`)
3. Commit تغييراتك (`git commit -m 'Add feature'`)
4. Push للفرع (`git push origin feature/amazing`)
5. افتح Pull Request

**ملاحظة:** الفرع الرئيسي محمي - يجب إنشاء PR للدمج.

---

## 🌟 النماذج المدعومة

- ✅ OpenAI (GPT-4o, GPT-4o-mini)
- ✅ Anthropic (Claude 3.5 Sonnet, Haiku)
- ✅ Google (Gemini 2.0 Flash, Pro)
- ✅ DeepSeek, Groq, Mistral, وغيرها

---

## 📞 الدعم

واجهت مشكلة؟

1. تأكد من API key صحيح
2. تأكد من التثبيت السليم
3. راجع التوثيق في [AI_APPS_README.md](./AI_APPS_README.md)
4. افتح Issue على GitHub

---

## 📝 الترخيص

MIT License - استخدم بحرية!

---

## 🙏 شكر خاص

مبني على:
- [AutoAgent](https://github.com/HKUDS/AutoAgent) - الإطار الأساسي
- OpenAI Swarm - الإلهام المعماري
- المجتمع مفتوح المصدر

---

## 📈 إحصائيات

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/aboday2067-dot/sudan)
![GitHub forks](https://img.shields.io/github/forks/aboday2067-dot/sudan)
![GitHub issues](https://img.shields.io/github/issues/aboday2067-dot/sudan)

</div>

---

<div align="center">

**صُنع بـ ❤️ بواسطة [aboday2067-dot](https://github.com/aboday2067-dot)**

⭐ إذا أعجبك المشروع، لا تنسَ النجمة!

</div>

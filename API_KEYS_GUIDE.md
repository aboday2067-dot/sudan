# 🔑 دليل الحصول على API Keys لزيزو ألتيميت

## 📋 جدول المحتويات
1. [المقدمة](#المقدمة)
2. [الخيار الأول: استخدام GenSpark APIs (موصى به)](#الخيار-الأول-genspark)
3. [الخيار الثاني: APIs خارجية](#الخيار-الثاني-apis-خارجية)
4. [إضافة المفاتيح لزيزو](#إضافة-المفاتيح-لزيزو)
5. [الأسعار والتكاليف](#الأسعار-والتكاليف)

---

## 🎯 المقدمة

زيزو ألتيميت يحتاج إلى 3 أنواع من APIs:
- 🎨 **توليد الصور**: Flux, DALL-E, Stable Diffusion
- 🎬 **توليد الفيديو**: Runway, Pika Labs, Gemini Veo
- 🎵 **توليد الصوت**: ElevenLabs, Google TTS

**الخبر السار**: يمكنك البدء **مجاناً** بعدة طرق!

---

## ✅ الخيار الأول: استخدام GenSpark APIs (موصى به)

### لماذا GenSpark؟
- ✅ **مدمج بالفعل** - لا حاجة لمفاتيح إضافية
- ✅ **مجاني للبدء** - رصيد تجريبي
- ✅ **كل الميزات** - صور + فيديو + صوت
- ✅ **سهل الإعداد** - خطوة واحدة

### 📝 الخطوات:

#### 1. **تسجيل الدخول إلى GenSpark**
```
🌐 الرابط: https://www.genspark.ai
📧 استخدم حسابك الحالي
```

#### 2. **الوصول إلى لوحة API**
```
الخطوات:
1. اذهب إلى: Settings ⚙️
2. اختر: API Keys 🔑
3. اضغط: Create New Key
```

#### 3. **إنشاء مفتاح جديد**
```bash
# معلومات المفتاح:
الاسم: Zizo Ultimate API
الصلاحيات: 
  ✅ Image Generation
  ✅ Video Generation  
  ✅ Audio Generation
  ✅ Chat Completion

# انسخ المفتاح:
gs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 4. **إضافة المفتاح لزيزو**
```bash
# طريقة 1: عبر متغيرات البيئة
export GENSPARK_API_KEY="gs_your_key_here"

# طريقة 2: عبر ملف الإعداد
echo "genspark_api_key: gs_your_key_here" >> ~/.genspark_llm.yaml
```

#### 5. **اختبار المفتاح**
```bash
# اختبر عبر curl:
curl -X POST https://api.genspark.ai/v1/images/generate \
  -H "Authorization: Bearer gs_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset",
    "model": "flux-2-pro"
  }'
```

### 💰 الرصيد المجاني:
- **التسجيل الجديد**: 100 رصيد مجاني
- **الصور**: ~2-5 رصيد لكل صورة
- **الفيديو**: ~10-20 رصيد لكل فيديو
- **الصوت**: ~1-3 رصيد لكل ملف

**إجمالي**: ~10-50 توليد مجاني! 🎉

---

## 🌍 الخيار الثاني: APIs خارجية

إذا أردت استخدام خدمات خارجية، إليك الخيارات:

---

### 🎨 1. توليد الصور

#### **أ) FAL.AI (موصى به)**
```
🌐 الموقع: https://fal.ai
💰 السعر: مجاني للبدء ($5 رصيد)
⚡ السرعة: سريع جداً (2-5 ثوان)
🎨 النماذج: Flux, SDXL, Stability
```

**خطوات التسجيل:**
1. اذهب إلى: https://fal.ai/dashboard
2. اضغط: Sign Up (مجاني)
3. انتقل إلى: API Keys
4. انسخ المفتاح: `fal_xxxxxxxx...`

**كود التكامل:**
```python
import fal_client

# في app.py:
def generate_image_fal(prompt):
    result = fal_client.submit(
        "fal-ai/flux-pro",
        arguments={"prompt": prompt}
    )
    return result['image_url']
```

---

#### **ب) OpenAI DALL-E 3**
```
🌐 الموقع: https://platform.openai.com
💰 السعر: $0.04 لكل صورة (1024×1024)
⚡ السرعة: متوسط (10-30 ثانية)
🎨 الجودة: عالية جداً
```

**خطوات التسجيل:**
1. اذهب إلى: https://platform.openai.com/signup
2. أضف بطاقة ائتمان (مطلوب)
3. اذهب إلى: API Keys
4. أنشئ مفتاح: `sk-xxxxxxxx...`

**كود التكامل:**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-your-key")

def generate_image_dalle(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024"
    )
    return response.data[0].url
```

**الرصيد المجاني:**
- ❌ لا يوجد - يجب إضافة بطاقة
- 💰 $5 كحد أدنى للإيداع
- 🎨 ~125 صورة بـ $5

---

#### **ج) Stability AI**
```
🌐 الموقع: https://platform.stability.ai
💰 السعر: مجاني (25 رصيد شهرياً)
⚡ السرعة: سريع (3-8 ثوان)
🎨 النماذج: SDXL, SD 3.5
```

**خطوات التسجيل:**
1. اذهب إلى: https://platform.stability.ai/account/keys
2. سجّل حساب جديد
3. احصل على 25 رصيد مجاني
4. انسخ API Key: `sk-xxxxxxxx...`

**كود التكامل:**
```python
import requests

def generate_image_stability(prompt):
    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        },
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
        }
    )
    return response.json()["artifacts"][0]["base64"]
```

---

### 🎬 2. توليد الفيديو

#### **أ) Replicate (أسهل)**
```
🌐 الموقع: https://replicate.com
💰 السعر: $0.01-0.10 لكل ثانية
⚡ السرعة: 2-5 دقائق
🎬 النماذج: Runway, Zeroscope, AnimateDiff
```

**خطوات التسجيل:**
1. اذهب إلى: https://replicate.com/signin
2. سجّل بـ GitHub (مجاني)
3. أضف $10 رصيد
4. انسخ API Key من: https://replicate.com/account/api-tokens

**كود التكامل:**
```python
import replicate

def generate_video_replicate(prompt):
    output = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input={"prompt": prompt}
    )
    return output  # video URL
```

---

#### **ب) RunwayML Gen-2**
```
🌐 الموقع: https://runwayml.com
💰 السعر: $0.05 لكل ثانية
⚡ السرعة: 1-3 دقائق
🎬 الجودة: احترافية جداً
```

**خطوات التسجيل:**
1. اذهب إلى: https://app.runwayml.com/signup
2. اختر: API Access Plan ($12/شهر)
3. انتقل إلى: Settings > API Keys
4. انسخ المفتاح

**ملاحظة**: Gen-2 يتطلب اشتراك مدفوع ($12/شهر على الأقل)

---

#### **ج) Pika Labs (جديد)**
```
🌐 الموقع: https://pika.art
💰 السعر: مجاني للبدء
⚡ السرعة: 2-4 دقائق
🎬 الجودة: عالية
```

**خطوات التسجيل:**
1. اذهب إلى: https://pika.art
2. سجّل بـ Discord
3. انضم لـ: Pika Beta
4. احصل على API Access (قيد الطلب)

**ملاحظة**: API قيد التطوير، حالياً عبر Discord Bot

---

### 🎵 3. توليد الصوت

#### **أ) ElevenLabs (الأفضل)**
```
🌐 الموقع: https://elevenlabs.io
💰 السعر: مجاني (10,000 حرف شهرياً)
⚡ السرعة: فوري (1-3 ثوان)
🎵 الجودة: أفضل TTS في السوق
```

**خطوات التسجيل:**
1. اذهب إلى: https://elevenlabs.io/sign-up
2. سجّل مجاناً
3. اذهب إلى: Profile > API Keys
4. انسخ المفتاح: `xi_xxxxxxxx...`

**كود التكامل:**
```python
import requests

def generate_speech_elevenlabs(text):
    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
        headers={"xi-api-key": ELEVENLABS_API_KEY},
        json={
            "text": text,
            "model_id": "eleven_monolingual_v1"
        }
    )
    return response.content  # audio bytes
```

**الرصيد المجاني:**
- ✅ 10,000 حرف شهرياً مجاناً
- 🎵 ~20-30 دقيقة من الصوت
- 💰 ترقية: $5/شهر (30,000 حرف)

---

#### **ب) Google Cloud TTS**
```
🌐 الموقع: https://cloud.google.com/text-to-speech
💰 السعر: مجاني (1M حرف شهرياً)
⚡ السرعة: فوري
🎵 اللغات: 220+ صوت، 40+ لغة
```

**خطوات التسجيل:**
1. اذهب إلى: https://console.cloud.google.com
2. أنشئ مشروع جديد
3. فعّل: Cloud Text-to-Speech API
4. أنشئ Service Account
5. حمّل JSON Key

**كود التكامل:**
```python
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

def generate_speech_google(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ar-XA",  # Arabic
        name="ar-XA-Wavenet-A"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    return response.audio_content
```

---

#### **ج) OpenAI TTS**
```
🌐 الموقع: https://platform.openai.com
💰 السعر: $15/1M حرف
⚡ السرعة: فوري
🎵 الأصوات: 6 أصوات طبيعية
```

**خطوات التسجيل:**
نفس خطوات DALL-E أعلاه

**كود التكامل:**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-your-key")

def generate_speech_openai(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    return response.content
```

---

## 🔧 إضافة المفاتيح لزيزو

### الطريقة 1: عبر ملف الإعداد (موصى به)

```bash
# 1. افتح/أنشئ الملف:
nano ~/.genspark_llm.yaml

# 2. أضف المفاتيح:
openai:
  api_key: "sk-your-openai-key"
  base_url: "https://api.openai.com/v1"

fal_ai:
  api_key: "fal-your-key"

stability:
  api_key: "sk-your-stability-key"

elevenlabs:
  api_key: "xi-your-elevenlabs-key"

replicate:
  api_key: "r8-your-replicate-key"

# 3. احفظ الملف: Ctrl+O ثم Enter
# 4. اخرج: Ctrl+X
```

---

### الطريقة 2: عبر متغيرات البيئة

```bash
# أضف إلى ~/.bashrc أو ~/.zshrc:
export OPENAI_API_KEY="sk-your-key"
export FAL_API_KEY="fal-your-key"
export STABILITY_API_KEY="sk-your-key"
export ELEVENLABS_API_KEY="xi-your-key"
export REPLICATE_API_KEY="r8-your-key"

# فعّل التغييرات:
source ~/.bashrc
```

---

### الطريقة 3: عبر واجهة زيزو (قريباً)

سنضيف واجهة إعدادات داخل زيزو:
```
⚙️ Settings > API Keys
- Add Key
- Test Key
- View Usage
```

---

## 💰 الأسعار والتكاليف

### جدول المقارنة:

| الخدمة | الرصيد المجاني | السعر بعد المجاني | الجودة | السرعة |
|--------|----------------|-------------------|--------|--------|
| **الصور** |||
| GenSpark | 100 رصيد (~20 صورة) | $0.02-0.05/صورة | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| FAL.AI | $5 رصيد (~100 صورة) | $0.03-0.08/صورة | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| DALL-E 3 | ❌ | $0.04/صورة | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ |
| Stability AI | 25 رصيد (~25 صورة) | $0.03/صورة | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| **الفيديو** |||
| GenSpark | 100 رصيد (~5 فيديو) | $0.20-0.50/فيديو | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ |
| Replicate | $10 رصيد (~20 فيديو) | $0.05-0.10/ثانية | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| Runway | ❌ $12/شهر | $0.05/ثانية | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| **الصوت** |||
| GenSpark | 100 رصيد (~50 ملف) | $0.01-0.03/ملف | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| ElevenLabs | 10K حرف مجاناً | $5/شهر (30K) | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| Google TTS | 1M حرف مجاناً | $4/1M حرف | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| OpenAI TTS | ❌ | $15/1M حرف | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |

---

## ✅ خطة البدء الموصى بها

### للبدء المجاني 100%:

```
✅ الصور: 
   الخيار 1: GenSpark (100 رصيد مجاني)
   الخيار 2: Stability AI (25 صورة مجاناً)
   الخيار 3: FAL.AI ($5 رصيد مجاني)

✅ الفيديو:
   الخيار 1: GenSpark (100 رصيد مجاني)
   الخيار 2: Replicate ($10 عند التسجيل)

✅ الصوت:
   الخيار 1: GenSpark (100 رصيد مجاني)
   الخيار 2: ElevenLabs (10K حرف مجاناً)
   الخيار 3: Google Cloud TTS (1M حرف مجاناً)
```

### إجمالي التوليدات المجانية:
- 🎨 **~50-100 صورة**
- 🎬 **~10-20 فيديو**
- 🎵 **~50-100 ملف صوتي**

**كل ذلك بدون دفع قرش واحد!** 🎉

---

## 🚀 البدء السريع (5 دقائق)

### الخطوات السريعة:

1. **سجّل في GenSpark** (دقيقة واحدة)
   ```
   https://www.genspark.ai/signup
   ```

2. **احصل على API Key** (دقيقة واحدة)
   ```
   Settings > API Keys > Create New Key
   ```

3. **أضف المفتاح لزيزو** (دقيقة واحدة)
   ```bash
   echo "genspark_api_key: gs_your_key" >> ~/.genspark_llm.yaml
   ```

4. **أعد تشغيل زيزو** (30 ثانية)
   ```bash
   cd ~/webapp && pkill python3 && python3 app.py &
   ```

5. **جرّب التوليد!** (دقيقة واحدة)
   ```
   افتح: https://5000-...sandbox.novita.ai
   اختر: 🎨 صور
   اكتب: "قط أبيض جميل"
   ```

**جاهز!** 🎉

---

## 📞 الدعم

### إذا واجهت مشاكل:

1. **تحقق من المفتاح**:
   ```bash
   cat ~/.genspark_llm.yaml | grep api_key
   ```

2. **اختبر الاتصال**:
   ```bash
   curl -H "Authorization: Bearer gs_your_key" \
     https://api.genspark.ai/v1/health
   ```

3. **تحقق من السجلات**:
   ```bash
   tail -f ~/webapp/zizo_generation.log
   ```

---

## 📚 موارد إضافية

- 📖 [GenSpark Documentation](https://docs.genspark.ai)
- 💬 [Discord Community](https://discord.gg/genspark)
- 🐛 [Report Issues](https://github.com/aboday2067-dot/sudan/issues)
- 📧 [Support Email](mailto:support@genspark.ai)

---

**صُنع بـ ❤️ من السودان | دليل API Keys v1.0 | آخر تحديث: 2026-02-11**

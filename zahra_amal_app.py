"""
زيزو مخصص لمتجر زهرة أمل
Custom Zizo for Zahra Amal Store

هذا ملف Python لتشغيل زيزو مع معلومات مخصصة لمتجر زهرة أمل
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from autoagent import MetaChain, Agent
import os
from dotenv import load_dotenv
import secrets

# تحميل المتغيرات البيئية
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# السماح لجميع النطاقات (غيّره لموقعك فقط في الإنتاج)
CORS(app)

# إعدادات الذكاء الاصطناعي
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
client = MetaChain(log_path=None)

# معلومات متجر زهرة أمل (خصصها حسب متجرك!)
STORE_INFO = {
    "name": "زهرة أمل",
    "name_en": "Zahra Amal",
    "specialty": "متجر إلكتروني متكامل",
    "categories": [
        "الإلكترونيات (هواتف، لابتوبات، أجهزة لوحية)",
        "الأزياء والملابس (رجالي، نسائي، أطفال)",
        "الأجهزة المنزلية (أدوات مطبخ، أثاث)",
        "مستحضرات التجميل والعناية",
        "الألعاب والهوايات",
        "الكتب والقرطاسية"
    ],
    "contact": {
        "phone": "0123456789",
        "email": "info@zahra-amal.com",
        "whatsapp": "966123456789",
        "address": "الرياض، المملكة العربية السعودية"
    },
    "working_hours": "السبت إلى الخميس: 9 صباحاً - 9 مساءً",
    "shipping": {
        "free_threshold": 200,
        "main_cities": "1-3 أيام",
        "remote_areas": "3-5 أيام",
        "methods": ["توصيل عادي", "توصيل سريع", "استلام من الفرع"]
    },
    "payment_methods": [
        "بطاقات الائتمان (فيزا، ماستركارد)",
        "مدى",
        "تحويل بنكي",
        "الدفع عند الاستلام",
        "Apple Pay",
        "STC Pay"
    ],
    "return_policy": "14 يوم من تاريخ الاستلام",
    "warranty": "من سنة إلى 3 سنوات حسب المنتج",
    "social_media": {
        "instagram": "@zahra_amal",
        "twitter": "@zahra_amal",
        "snapchat": "zahra_amal",
        "tiktok": "@zahra_amal"
    },
    "offers": [
        "خصم 20% على جميع الأجهزة الإلكترونية",
        "شحن مجاني للطلبات فوق 200 ريال",
        "اشترِ 2 واحصل على الثالث مجاناً (ملابس محددة)",
        "برنامج نقاط الولاء: 1 ريال = 1 نقطة"
    ]
}

# المنتجات المميزة (يمكن ربطها بقاعدة بيانات لاحقاً)
FEATURED_PRODUCTS = [
    {
        "id": 1,
        "name": "هاتف ذكي سامسونج جالكسي S24",
        "category": "إلكترونيات",
        "price": 2500,
        "description": "شاشة 6.5 بوصة، كاميرا 48 ميجا بكسل، بطارية 5000 مللي أمبير",
        "stock": "متوفر",
        "warranty": "سنتان"
    },
    {
        "id": 2,
        "name": "لابتوب HP Pavilion",
        "category": "إلكترونيات",
        "price": 4800,
        "description": "معالج Core i7، رام 16 جيجا، SSD 512 جيجا",
        "stock": "متوفر",
        "warranty": "3 سنوات"
    },
    {
        "id": 3,
        "name": "ساعة ذكية Apple Watch Series 9",
        "category": "إلكترونيات",
        "price": 1899,
        "description": "ميزات صحية ورياضية متقدمة، مقاومة للماء",
        "stock": "متوفر",
        "warranty": "سنة"
    },
    {
        "id": 4,
        "name": "سماعات Sony WH-1000XM5",
        "category": "إلكترونيات",
        "price": 1299,
        "description": "عزل نشط للضوضاء، بطارية 30 ساعة",
        "stock": "متوفر",
        "warranty": "سنة"
    },
    {
        "id": 5,
        "name": "كاميرا Canon EOS R6",
        "category": "إلكترونيات",
        "price": 8500,
        "description": "كاميرا احترافية 20 ميجا بكسل، تصوير 4K",
        "stock": "محدود",
        "warranty": "3 سنوات"
    }
]

# بناء تعليمات زيزو المخصصة
def build_zizo_instructions():
    instructions = f"""أنا زيزو 🤖، المساعد الذكي لمتجر {STORE_INFO['name']} ({STORE_INFO['name_en']}).

🌸 معلومات عن متجرنا:
- {STORE_INFO['specialty']}
- نوفر: {', '.join(STORE_INFO['categories'])}
- ساعات العمل: {STORE_INFO['working_hours']}

📞 معلومات التواصل:
- الهاتف: {STORE_INFO['contact']['phone']}
- البريد: {STORE_INFO['contact']['email']}
- واتساب: {STORE_INFO['contact']['whatsapp']}
- العنوان: {STORE_INFO['contact']['address']}

🚚 الشحن والتوصيل:
- توصيل مجاني للطلبات فوق {STORE_INFO['shipping']['free_threshold']} ريال
- المدن الرئيسية: {STORE_INFO['shipping']['main_cities']}
- المناطق النائية: {STORE_INFO['shipping']['remote_areas']}
- طرق التوصيل: {', '.join(STORE_INFO['shipping']['methods'])}

💳 طرق الدفع:
{chr(10).join([f"- {method}" for method in STORE_INFO['payment_methods']])}

🔄 سياسة الإرجاع والضمان:
- الإرجاع: {STORE_INFO['return_policy']}
- الضمان: {STORE_INFO['warranty']}

🎁 العروض الحالية:
{chr(10).join([f"- {offer}" for offer in STORE_INFO['offers']])}

📱 تابعنا على:
- Instagram: {STORE_INFO['social_media']['instagram']}
- Twitter: {STORE_INFO['social_media']['twitter']}
- Snapchat: {STORE_INFO['social_media']['snapchat']}
- TikTok: {STORE_INFO['social_media']['tiktok']}

📦 المنتجات المميزة حالياً:
"""
    
    for product in FEATURED_PRODUCTS[:3]:
        instructions += f"\n- {product['name']}: {product['price']} ريال - {product['description']}"
    
    instructions += """

💼 مهامي الأساسية:
1. الترحيب بالزوار وإرشادهم في الموقع
2. الإجابة على الأسئلة عن المنتجات والأسعار والمواصفات
3. شرح سياسات الشحن والإرجاع والضمان
4. مساعدة العملاء في إتمام الطلبات خطوة بخطوة
5. تقديم العروض والخصومات المتاحة
6. حل المشاكل وتقديم الدعم الفني
7. البحث عن منتجات معينة ومساعدة في الاختيار
8. تتبع الطلبات والإجابة عن استفسارات التوصيل
9. شرح برنامج نقاط الولاء والمكافآت

🎯 أسلوبي في التعامل:
- ودود ومحترف ومتحمس لمساعدة العملاء
- سريع الاستجابة ودقيق في المعلومات
- أجيب بالعربية أو الإنجليزية حسب لغة العميل
- أقدم حلول واضحة ومباشرة مع الأمثلة
- أستخدم الإيموجي المناسبة لجعل المحادثة ممتعة 😊
- أقترح منتجات بديلة إذا لم يكن المطلوب متوفراً
- أشجع العملاء على الشراء بطريقة لطيفة وغير مباشرة

📝 ملاحظات مهمة:
- إذا لم أعرف إجابة سؤال محدد، أوجه العميل للتواصل مع خدمة العملاء
- أتأكد دائماً من فهم سؤال العميل قبل الإجابة
- أقدم روابط مفيدة عند الحاجة
- أحافظ على خصوصية بيانات العملاء
- أتجنب الوعود التي لا يمكن الوفاء بها

🌟 هدفي: تحويل كل زائر إلى عميل سعيد وراضٍ!
"""
    
    return instructions

# إنشاء وكيل زيزو
zizo_agent = Agent(
    name="زيزو - مساعد متجر زهرة أمل",
    model=AI_MODEL,
    instructions=build_zizo_instructions()
)

# الصفحة الرئيسية
@app.route('/')
def home():
    html_template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>زيزو - مساعد متجر زهرة أمل</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                flex-direction: column;
            }
            .header {
                background: white;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .header h1 {
                color: #667eea;
                font-size: 28px;
                margin-bottom: 5px;
            }
            .header p {
                color: #666;
                font-size: 14px;
            }
            .status-bar {
                background: #4ade80;
                color: white;
                padding: 10px 20px;
                text-align: center;
                font-size: 14px;
                font-weight: bold;
            }
            .chat-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                max-width: 800px;
                width: 100%;
                margin: 20px auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f5f5f5;
            }
            .message {
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
            }
            .message.user {
                flex-direction: row-reverse;
            }
            .message-bubble {
                max-width: 70%;
                padding: 12px 18px;
                border-radius: 18px;
                word-wrap: break-word;
            }
            .message.user .message-bubble {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 4px;
            }
            .message.assistant .message-bubble {
                background: white;
                color: #333;
                border-bottom-left-radius: 4px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .avatar {
                width: 35px;
                height: 35px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                margin: 0 10px;
            }
            .input-area {
                padding: 20px;
                background: white;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 10px;
            }
            #messageInput {
                flex: 1;
                padding: 12px 20px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: all 0.3s;
            }
            #messageInput:focus {
                border-color: #667eea;
            }
            #sendButton {
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s;
            }
            #sendButton:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            #sendButton:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .typing {
                display: none;
                padding: 10px 15px;
                background: white;
                border-radius: 18px;
                width: fit-content;
            }
            .typing span {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #667eea;
                margin: 0 2px;
                animation: typing 1.4s infinite;
            }
            .typing span:nth-child(2) { animation-delay: 0.2s; }
            .typing span:nth-child(3) { animation-delay: 0.4s; }
            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 زيزو - مساعد متجر زهرة أمل</h1>
            <p>Zizo AI Assistant for Zahra Amal Store</p>
        </div>
        <div class="status-bar">
            🟢 متصل | Model: {{ model }}
        </div>
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="message assistant">
                    <div class="avatar">🤖</div>
                    <div class="message-bubble">
                        مرحباً بك في متجر زهرة أمل! 🌸<br>
                        أنا زيزو، مساعدك الذكي. كيف يمكنني مساعدتك اليوم؟<br><br>
                        يمكنني المساعدة في:<br>
                        • البحث عن منتجات<br>
                        • الإجابة على الأسئلة<br>
                        • شرح العروض والخصومات<br>
                        • مساعدتك في الطلب<br>
                        • تتبع الطلبات
                    </div>
                </div>
                <div class="typing" id="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div class="input-area">
                <input 
                    type="text" 
                    id="messageInput" 
                    placeholder="اكتب رسالتك هنا..."
                    autocomplete="off"
                >
                <button id="sendButton">إرسال 📤</button>
            </div>
        </div>
        
        <script>
            const messagesDiv = document.getElementById('messages');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const typingIndicator = document.getElementById('typing');
            
            let conversationHistory = [];
            
            function addMessage(role, content) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${role}`;
                messageDiv.innerHTML = `
                    <div class="avatar">${role === 'user' ? '👤' : '🤖'}</div>
                    <div class="message-bubble">${content}</div>
                `;
                messagesDiv.insertBefore(messageDiv, typingIndicator);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;
                
                // إضافة رسالة المستخدم
                addMessage('user', message);
                conversationHistory.push({ role: 'user', content: message });
                
                // تفريغ الحقل وتعطيل الزر
                messageInput.value = '';
                sendButton.disabled = true;
                
                // عرض مؤشر الكتابة
                typingIndicator.style.display = 'block';
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message: message,
                            history: conversationHistory
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        addMessage('assistant', data.response);
                        conversationHistory.push({ role: 'assistant', content: data.response });
                    } else {
                        addMessage('assistant', 'عذراً، حدث خطأ. حاول مرة أخرى.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    addMessage('assistant', 'عذراً، حدث خطأ في الاتصال. حاول مرة أخرى.');
                } finally {
                    typingIndicator.style.display = 'none';
                    sendButton.disabled = false;
                    messageInput.focus();
                }
            }
            
            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
            
            messageInput.focus();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, model=AI_MODEL)

# نقطة النهاية للشات
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        history = data.get('history', [])
        
        if not user_message:
            return jsonify({'status': 'error', 'message': 'لا توجد رسالة'})
        
        # إضافة الرسالة الجديدة
        messages = history + [{"role": "user", "content": user_message}]
        
        # معالجة الرسالة مع زيزو
        response = client.run(
            agent=zizo_agent,
            messages=messages
        )
        
        assistant_reply = response.messages[-1]["content"]
        
        return jsonify({
            'status': 'success',
            'response': assistant_reply,
            'history': messages + [{"role": "assistant", "content": assistant_reply}]
        })
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'حدث خطأ: {str(e)}'
        })

# نقطة فحص الحالة
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'app': f"زيزو - مساعد متجر {STORE_INFO['name']}",
        'model': AI_MODEL,
        'version': '2.0.0 - Zahra Amal Edition'
    })

# نقطة معلومات المتجر
@app.route('/store-info')
def store_info():
    return jsonify(STORE_INFO)

# نقطة المنتجات المميزة
@app.route('/featured-products')
def featured_products():
    return jsonify(FEATURED_PRODUCTS)

if __name__ == '__main__':
    print("=" * 60)
    print(f"🌸 زيزو - مساعد متجر {STORE_INFO['name']} 🌸")
    print("=" * 60)
    print(f"📱 Model: {AI_MODEL}")
    print(f"🌐 Server: http://0.0.0.0:5000")
    print(f"💬 Chat: http://0.0.0.0:5000")
    print(f"❤️ Health: http://0.0.0.0:5000/health")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )

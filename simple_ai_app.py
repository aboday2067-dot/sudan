#!/usr/bin/env python3
"""
زيزو - تطبيق AI خفيف وسريع
Zizo - Simple & Fast AI Application
"""

import os
import sys
from autoagent import MetaChain, Agent
from autoagent.logger import MetaChainLogger

# ===== إعدادات التطبيق =====
APP_NAME = "زيزو 🤖"
VERSION = "1.0.0"

class SimpleAIApp:
    """تطبيق AI بسيط وخفيف"""
    
    def __init__(self, model="gpt-4o-mini"):
        """
        تهيئة التطبيق
        Args:
            model: اسم النموذج (افتراضي: gpt-4o-mini للسرعة)
        """
        self.model = model
        self.client = MetaChain(log_path=None)  # بدون logs للسرعة
        self.agent = self._create_agent()
        
    def _create_agent(self):
        """إنشاء AI agent خفيف"""
        return Agent(
            name="زيزو",
            model=self.model,
            instructions="""أنا زيزو 🤖، مساعدك الذكي السريع والمفيد!

مهامي:
- الإجابة على أسئلتك بوضوح ودقة
- تقديم معلومات مفيدة وموثوقة
- مساعدتك في حل المشاكل
- الرد بسرعة وكفاءة عالية

أتحدث بالعربية إذا كان سؤالك بالعربية، وبالإنجليزية إذا كان بالإنجليزية.
دائماً في خدمتك! 😊""",
            functions=[],  # بدون أدوات إضافية للسرعة
        )
    
    def chat(self, message):
        """
        التحدث مع AI
        Args:
            message: رسالة المستخدم
        Returns:
            رد AI
        """
        messages = [{"role": "user", "content": message}]
        response = self.client.run(
            self.agent, 
            messages, 
            context_variables={},
            debug=False,  # بدون debug للسرعة
            max_turns=1   # دورة واحدة فقط للسرعة
        )
        return response.messages[-1]['content']
    
    def run_interactive(self):
        """وضع تفاعلي - محادثة مستمرة"""
        print(f"\n{'='*60}")
        print(f"  {APP_NAME} v{VERSION}")
        print(f"  النموذج: {self.model}")
        print(f"{'='*60}\n")
        print("💡 اكتب سؤالك أو 'خروج' للإنهاء\n")
        
        conversation_history = []
        
        while True:
            try:
                # استقبال السؤال
                user_input = input("👤 أنت: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['خروج', 'exit', 'quit', 'q']:
                    print("\n👋 مع السلامة!\n")
                    break
                
                # إضافة إلى السجل
                conversation_history.append({
                    "role": "user", 
                    "content": user_input
                })
                
                # الحصول على الرد
                print("🤖 AI: ", end="", flush=True)
                response = self.client.run(
                    self.agent,
                    conversation_history,
                    context_variables={},
                    debug=False,
                    max_turns=1
                )
                
                ai_response = response.messages[-1]['content']
                print(ai_response + "\n")
                
                # إضافة الرد إلى السجل
                conversation_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
                
            except KeyboardInterrupt:
                print("\n\n👋 تم إيقاف البرنامج\n")
                break
            except Exception as e:
                print(f"\n❌ خطأ: {e}\n")
                continue


def main():
    """الدالة الرئيسية"""
    
    # التحقق من وجود API key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  تحذير: لم يتم العثور على API key!")
        print("الرجاء تعيين OPENAI_API_KEY أو ANTHROPIC_API_KEY\n")
        print("مثال:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("  python simple_ai_app.py\n")
        return
    
    # اختيار النموذج الأسرع
    if os.getenv("ANTHROPIC_API_KEY"):
        model = "claude-3-5-haiku-20241022"  # الأسرع من Anthropic
    else:
        model = "gpt-4o-mini"  # الأسرع من OpenAI
    
    # إنشاء التطبيق
    app = SimpleAIApp(model=model)
    
    # بدء الوضع التفاعلي
    app.run_interactive()


if __name__ == "__main__":
    main()

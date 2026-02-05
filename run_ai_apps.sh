#!/bin/bash
# 🚀 تشغيل سريع للتطبيقات

echo "╔════════════════════════════════════════════╗"
echo "║   🤖 تطبيقات AI السريعة - قائمة التشغيل   ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# التحقق من API Keys
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  تحذير: لم يتم العثور على أي API key!"
    echo ""
    echo "الرجاء تعيين واحد من هذه:"
    echo "  export OPENAI_API_KEY='your-key'"
    echo "  export ANTHROPIC_API_KEY='your-key'"
    echo "  export GEMINI_API_KEY='your-key'"
    echo ""
    exit 1
fi

echo "اختر التطبيق:"
echo ""
echo "  1️⃣  تطبيق Terminal (محادثة في سطر الأوامر)"
echo "  2️⃣  تطبيق Web (واجهة في المتصفح)"
echo "  3️⃣  الاثنين معاً"
echo "  4️⃣  إلغاء"
echo ""
read -p "اختيارك (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 جاري تشغيل تطبيق Terminal..."
        echo ""
        python simple_ai_app.py
        ;;
    2)
        echo ""
        echo "🌐 جاري تشغيل تطبيق Web..."
        echo "📍 افتح المتصفح على: http://localhost:5000"
        echo ""
        python web_ai_app.py
        ;;
    3)
        echo ""
        echo "🚀 جاري تشغيل التطبيقين..."
        echo ""
        python web_ai_app.py &
        WEB_PID=$!
        sleep 2
        echo ""
        echo "📍 تطبيق Web يعمل على: http://localhost:5000"
        echo ""
        python simple_ai_app.py
        kill $WEB_PID 2>/dev/null
        ;;
    4)
        echo ""
        echo "👋 تم الإلغاء"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ اختيار غير صحيح"
        exit 1
        ;;
esac

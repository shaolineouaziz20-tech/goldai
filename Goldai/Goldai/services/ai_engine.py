import json
import os
import re
import requests


def analyze_news_and_get_bias(news_text, session_name='Upcoming Session'):
  """تحليل الأخبار والتحيز للجلسات بأسلوب SMC/ICT وكشف أخبار CPI/PPI للذهب XAUUSD."""
  try:
    # 1. فحص كشف الأخبار القوية جداً (CPI, PPI, NFP, FOMC)
    major_news_detected = []
    major_keywords = ['CPI', 'PPI', 'NFP', 'FOMC', 'FED', 'Rate', 'Inflation']

    for keyword in major_keywords:
      if re.search(r'\b' + keyword + r'\b', news_text, re.IGNORECASE):
        major_news_detected.append(keyword.upper())

    major_news_detected = list(set(major_news_detected))
    has_high_impact = len(major_news_detected) > 0

    # 2. إعداد الـ Prompt للذكاء الاصطناعي بأسلوب SMC / ICT
    prompt = f"""
        أنت محلل محترف لأسواق المال متخصص في الذهب (XAUUSD) وتعتمد على مدرسة Smart Money Concepts (SMC) و ICT.
        
        المطلوب: تحليل تحيز الجلسة القادمة ({session_name}) بناءً على الأخبار التالية:
        {news_text}
        
        الأخبار القوية المكتشفة: {", ".join(major_news_detected) if has_high_impact else "لا توجد أخبار كبرى مثل CPI/PPI اليوم"}

        قم بإرجاع النتيجة حصراً بصيغة JSON بالتنسيق التالي دون أي كلام إضافي:
        {{
            "daily_bias": "BULLISH" أو "BEARISH" أو "NEUTRAL",
            "daily_confidence": 85,
            "major_news_alert": {{
                "has_major_news": true/false,
                "news_names": "{", ".join(major_news_detected)}",
                "warning": "تحذير: توجد أخبار عالية الخطورة! يفضل تجنب التداول قبل الخبر بـ 15 دقيقة."
            }},
            "draw_on_liquidity": "تحديد هل السعر يتجه لـ Buy-side Liquidity أم Sell-side Liquidity",
            "fundamental_summary": "ملخص سيناريو الجلسة والسبب الأساسي للحركة المتوقعة",
            "news_impact_breakdown": [
                {{
                    "title": "اسم الخبر",
                    "effect": "إيجابي للذهب / سلبي للذهب / محايد",
                    "reason": "تأثير الرقم الصادر مقارنة بالمتوقع على حركة XAUUSD"
                }}
            ]
        }}
        """

    # 3. محاكات/طلب الـ AI (في حال عدم وجود API Key يرجع تحليلاً ذكياً بناءً على الفحص)
    # يمكن ربطه بمفتاح OpenAI أو Gemini هنا
    if has_high_impact:
      bias = (
          "BEARISH" if "CPI" in major_news_detected else "BULLISH"
      )  # مثال تحليلي
      summary = f"🚨 تنبيه: تم كشف أخبار كبرى ({', '.join(major_news_detected)}). سيؤدي هذا لتذبذب حاد وسحب سيولة قوي في جلسة {session_name}."
      dol = "Sell-side Liquidity (تحت القيعان القريبة)"
    else:
      bias = "NEUTRAL"
      summary = f"جلسة {session_name} هادئة نسبياً لعدم وجود أخبار كبرى مثل CPI أو PPI. الحركة متوقعة داخل نطاق عرضي (Range Bound)."
      dol = "تذبذب بين Fair Value Gaps للجلسة السابقة"

    return {
        "daily_bias": bias,
        "daily_confidence": 80 if has_high_impact else 65,
        "major_news_alert": {
            "has_major_news": has_high_impact,
            "news_names": (
                ", ".join(major_news_detected) if has_high_impact else "None"
            ),
            "warning": (
                "🚨 تحذير: أخبار عالية الخطورة (CPI/PPI/NFP)! تجنب التداول قبل"
                " الصدور بـ 15 دقيقة."
                if has_high_impact
                else "جلسة آمنة من الأخبار الكبرى."
            ),
        },
        "draw_on_liquidity": dol,
        "fundamental_summary": summary,
        "news_impact_breakdown": [{
            "title": (
                f"أخبار {', '.join(major_news_detected)}"
                if has_high_impact
                else "أخبار اعتيادية"
            ),
            "effect": bias,
            "reason": (
                "تأثير مباشر على أزواج الدولار والذهب"
                if has_high_impact
                else "لا توجد فروقات كبيرة"
            ),
        }],
    }

  except Exception as e:
    print(f"Error in AI Engine: {e}")
    return {
        "daily_bias": "NEUTRAL",
        "daily_confidence": 50,
        "major_news_alert": {
            "has_major_news": False,
            "news_names": "None",
            "warning": "خطأ في المعالجة",
        },
        "draw_on_liquidity": "غير محدد",
        "fundamental_summary": f"حدث خطأ أثناء تحليل بيانات الجلسة: {str(e)}",
        "news_impact_breakdown": [],
    }
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, render_template, request
import pytz
import requests
from services.ai_engine import analyze_news_and_get_bias
from services.news_fetcher import fetch_today_usd_news

app = Flask(__name__)

# ----------------------------------------------------
# 🔗 رابط Discord Webhook الخاص بك
# ----------------------------------------------------
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1527788761059164374/rzjVmLae__xFsc54rxyvr-kezV0T53Z7Spntv6RY7Si_4HpVFXV0I5DdVv6rBju6d2Mu"


def send_discord_alert(session_name, result):
  """دالة تنسيق وإرسال التقرير تلقائياً إلى سيرفر Discord"""
  bias = result.get("daily_bias", "NEUTRAL")
  color = (
      0x0ECB81
      if bias == "BULLISH"
      else (0xF6465D if bias == "BEARISH" else 0x848E9C)
  )

  # فحص تنبيه الأخبار الكبرى (CPI/PPI)
  major_alert = result.get("major_news_alert", {})
  alert_text = (
      f"\n🚨 **تنبيه هام:** {major_alert.get('warning')}"
      if major_alert.get("has_major_news")
      else ""
  )

  # تجهيز رسالة التقرير بتنسيق Discord Embed أنيق
  payload = {
      "username": "Gold AI Engine",
      "avatar_url": "https://cdn-icons-png.flaticon.com/512/2822/2822506.png",
      "embeds": [{
          "title": f"🏆 تقرير تحليل جلسة {session_name} (XAUUSD)",
          "description": (
              f"**التحيز اليومي (Bias):** `{bias}`"
              f" ({result.get('daily_confidence', 0)}%)\n**هدف السيولة"
              f" (DOL):**"
              f" `{result.get('draw_on_liquidity', 'غير محدد')}`{alert_text}\n\n**💡"
              f" سيناريو الحركة المتوقعة:**\n{result.get('fundamental_summary', '')}"
          ),
          "color": color,
          "footer": {
              "text": "Gold AI • Smart Money Concepts (SMC/ICT) System"
          },
          "timestamp": datetime.now(pytz.utc).isoformat(),
      }],
  }

  try:
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    if response.status_code in [200, 204]:
      print(f"✅ تم إرسال تقرير جلسة {session_name} إلى Discord بنجاح!")
    else:
      print(
          f"⚠️ فشل الإرسال إلى Discord: {response.status_code} -"
          f" {response.text}"
      )
  except Exception as e:
    print(f"⚠️ خطأ أثناء الإرسال لـ Discord: {e}")


def auto_session_job(session_name):
  """الدالة التي يطلقها المجدول تلقائياً قبل الجلسة بـ 10 دقائق"""
  print(f"⏰ [Scheduler] جاري إعداد تحليل جلسة {session_name}...")
  news_text = fetch_today_usd_news()
  result = analyze_news_and_get_bias(news_text, session_name=session_name)
  send_discord_alert(session_name, result)


# ----------------------------------------------------
# ⏰ إعداد مُجدول المهام (Scheduler) بالتوقيت العالمي UTC
# ----------------------------------------------------
scheduler = BackgroundScheduler(timezone="UTC")

# 1. جلسة آسيا (23:50 UTC)
scheduler.add_job(
    auto_session_job, "cron", hour=23, minute=50, args=["Asia Session"]
)
# 2. جلسة لندن (06:50 UTC)
scheduler.add_job(
    auto_session_job, "cron", hour=6, minute=50, args=["London Session"]
)
# 3. جلسة نيويورك (11:50 UTC)
scheduler.add_job(
    auto_session_job, "cron", hour=11, minute=50, args=["New York Session"]
)

scheduler.start()


# ----------------------------------------------------
# Routes السيرفر والواجهة
# ----------------------------------------------------
@app.route("/")
def home():
  return render_template("index.html")


@app.route("/api/gold-price", methods=["GET"])
def get_gold_price():
  try:
    url = "https://api.gold-api.com/price/XAU"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
      price = response.json().get("price", 0.0)
      return jsonify({"status": "success", "gold_price": f"{price:.2f}"})
  except Exception as e:
    print(f"Error fetching gold price: {e}")
  return jsonify({"status": "fallback", "gold_price": "4014.50"})


@app.route("/api/fetch-and-analyze-auto", methods=["GET"])
def fetch_and_analyze_auto():
  news_text = fetch_today_usd_news()
  analysis_result = analyze_news_and_get_bias(
      news_text, session_name="Upcoming Session"
  )
  analysis_result["fetched_news_text"] = news_text
  return jsonify(analysis_result)


@app.route("/api/analyze-manual", methods=["POST"])
def analyze_manual():
  data = request.get_json()
  news_text = data.get("news", "")
  if not news_text:
    return jsonify({"error": "النص فارغ"}), 400
  analysis_result = analyze_news_and_get_bias(
      news_text, session_name="Manual Analysis"
  )
  return jsonify(analysis_result)


# ----------------------------------------------------
# 🧪 رابط التجربة الفورية لـ Discord
# ----------------------------------------------------
@app.route("/test-discord")
def test_discord():
  test_data = {
      "daily_bias": "BULLISH",
      "daily_confidence": 90,
      "draw_on_liquidity": (
          "Buy-side Liquidity (فوق أقمام الجلسة السابقة)"
      ),
      "major_news_alert": {
          "has_major_news": True,
          "warning": "تنبيه تجريبي: خبر CPI قادم!",
      },
      "fundamental_summary": (
          "هذا إشعار تجريبي للتأكد من ربط Gold AI مع سيرفر Discord بنجاح! 🚀"
      ),
  }
  send_discord_alert("Test Session", test_data)
  return "<h1>✅ تم إرسال الرسالة التجريبية! تحقق من قناة Discord الآن.</h1>"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
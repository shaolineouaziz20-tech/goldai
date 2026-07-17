from datetime import datetime
import requests


def fetch_today_usd_news():
  """جلب الأخبار الاقتصادية المباشرة الخاصة بالدولار الأمريكي (USD) لاليوم الحالي حصراً."""
  try:
    # رابط تقويم Forex Factory المباشر بصيغة JSON
    ff_url = 'https://raw.githubusercontent.com/generalmotive/forex-factory-rss/master/fxeconomiccalendar.json'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(ff_url, headers=headers, timeout=8)

    if response.status_code == 200:
      events = response.json()
      usd_events = []

      # تاريخ اليوم بالصيغة القياسية (YYYY-MM-DD)
      today_str = datetime.now().strftime('%Y-%m-%d')

      for event in events:
        # 1. التحقق من العملة والتأثير (USD + High/Medium)
        currency = event.get('country', event.get('currency', ''))
        impact = event.get('impact', '')

        # 2. التحقق من تاريخ الخبر هل يطابق اليوم الحالي
        event_date_raw = str(event.get('date', ''))
        is_today = today_str in event_date_raw

        if currency == 'USD' and impact in ['High', 'Medium'] and is_today:
          title = event.get('title', 'USD Event')
          actual = event.get('actual', '')
          forecast = event.get('forecast', '')
          previous = event.get('previous', '')

          # صياغة الخبر للذكاء الاصطناعي
          status = f"Actual: {actual if actual else 'لم يصدر بعد'}"
          details = (
              f"Forecast: {forecast if forecast else 'N/A'}, Previous:"
              f" {previous if previous else 'N/A'}"
          )

          usd_events.append(
              f"• USD {title} [{impact} Impact] -> {status} ({details})"
          )

      if usd_events:
        return '\n'.join(usd_events[:8])

  except Exception as e:
    print(f'⚠️ خطأ أثناء جلب الأخبار المباشرة: {e}')

  return (
      'لا توجد أخبار اقتصادية هامة (High/Medium Impact) صادرة اليوم لـ USD حتى'
      ' الآن.'
  )
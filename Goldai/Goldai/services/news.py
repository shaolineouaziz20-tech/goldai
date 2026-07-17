import requests
import xml.etree.ElementTree as ET

def get_today_usd_news():
    """
    جلب الأخبار الاقتصادية المباشرة الخاصة بـ USD عبر Forex Factory RSS Feed
    """
    url = "https://www.forexfactory.com/ff_calendar_thisweek.xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    news_list = []
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            for item in root.findall('event'):
                country = item.find('country')
                title = item.find('title')
                impact = item.find('impact')
                forecast = item.find('forecast')
                previous = item.find('previous')
                
                # نفلترو الأخبار الخاصة بـ USD والتي تأثيرها High أو Medium
                if country is not None and country.text == 'USD':
                    event_title = title.text if title is not None else 'N/A'
                    impact_level = impact.text if impact is not None else 'High'
                    f_val = forecast.text if forecast is not None else 'N/A'
                    p_val = previous.text if previous is not None else 'N/A'
                    
                    news_list.append(f"- Event: {event_title} | Impact: {impact_level} | Forecast: {f_val} | Previous: {p_val}")
                    
    except Exception as e:
        print(f"[NEWS RSS ERROR] {e}")

    if not news_list:
        # إذا كان اليوم عطلة أو لا توجد أخبار كبرى
        return "No high-impact USD economic events scheduled for today."
        
    return "\n".join(news_list[:6]) # أخذ أهم 6 أخبار

if __name__ == "__main__":
    print("Today's News:\n", get_today_usd_news())
import yfinance as yf
import requests

def get_gold_price():
    """
    جلب سعر الذهب الحقيقي المباشر XAUUSD
    """
    try:
        # 1. التجربة عبر yfinance
        gold = yf.Ticker("GC=F")
        data = gold.history(period="1d", interval="1m")
        
        if not data.empty:
            raw_price = float(data['Close'].iloc[-1])
            # تصحيح الفارق بين Futures و Spot OANDA (حوالي -3.3$)
            spot_price = raw_price - 3.30 
            return f"{spot_price:.2f}"
            
    except Exception as e:
        print(f"[YFINANCE ERROR] {e}")

    try:
        # 2. احتياطي سريع عبر API آخر
        res = requests.get("https://api.gold-api.com/price/XAU", timeout=3)
        if res.status_code == 200:
            price = res.json().get("price")
            if price:
                return f"{float(price):.2f}"
    except Exception as e:
        print(f"[GOLD API ERROR] {e}")

    return "N/A"

if __name__ == "__main__":
    print("XAUUSD Price:", get_gold_price())
from flask import Flask, render_template, jsonify, request

from services.gold_price import get_gold_price
from services.news import get_high_impact_news, parse_news
from services.analysis import get_daily_bias
from services.forex_factory import fetch_forex_factory_news
app = Flask(__name__)


# ==========================
# Home Page
# ==========================
@app.route("/")
def home():

    gold_price = get_gold_price()
    news = get_high_impact_news()
    analysis = get_daily_bias(gold_price, news)

    return render_template(
        "index.html",
        gold_price=gold_price,
        news=news,
        analysis=analysis
    )


# ==========================
# API : Gold Price
# ==========================
@app.route("/api/gold-price")
def api_gold_price():

    gold_price = get_gold_price()

    return jsonify({
        "gold_price": gold_price
    })


# ==========================
# API : Live News
# ==========================
@app.route("/api/news")
def api_news():

    news = get_high_impact_news()

    return jsonify(news)


# ==========================
# API : Parse ForexFactory News
# ==========================
@app.route("/api/parse-news", methods=["POST"])
def api_parse_news():

    text = request.json.get("text", "")

    news = parse_news(text)

    return jsonify(news)


# ==========================
# API : Daily Bias
# ==========================
@app.route("/api/analysis")
def api_analysis():

    gold_price = get_gold_price()
    news = get_high_impact_news()

    analysis = get_daily_bias(gold_price, news)

    return jsonify(analysis)

# ==========================
# Test Forex Factory
# ==========================
@app.route("/test")
def test():

    fetch_forex_factory_news()

    return "OK"

    
# ==========================
# Run Flask
# ==========================
if __name__ == "__main__":
    app.run(debug=True)
def get_daily_bias(gold_price, news):

    bias = "🟡 محايد"
    confidence = 50
    reasons = []

    # تحليل السعر
    if gold_price >= 4000:
        bias = "🟢 صاعد"
        confidence = 70
        reasons.append("الذهب يتداول فوق مستوى 4000 دولار.")

    else:
        bias = "🔴 هابط"
        confidence = 60
        reasons.append("الذهب يتداول أسفل مستوى 4000 دولار.")

    # عدد الأخبار المهمة
    if len(news) >= 3:
        confidence += 10
        reasons.append("توجد عدة أخبار اقتصادية قوية اليوم.")

    # تحليل بسيط لعناوين الأخبار
    for item in news:

        title = item.get("title", "")

        if "التضخم" in title:
            reasons.append("اليوم توجد بيانات تضخم قد تسبب تقلبات قوية.")

        if "الفيدرالي" in title:
            reasons.append("تصريحات الاحتياطي الفيدرالي قد تؤثر على اتجاه الذهب.")

        if "الوظائف" in title:
            reasons.append("بيانات الوظائف الأمريكية قد تزيد من تذبذب السوق.")

    # الحد الأقصى للثقة
    if confidence > 90:
        confidence = 90

    # أهداف مبدئية (سنطورها لاحقاً)
    if bias == "🟢 صاعد":
        target1 = round(gold_price + 10, 2)
        target2 = round(gold_price + 20, 2)
        stoploss = round(gold_price - 8, 2)

    elif bias == "🔴 هابط":
        target1 = round(gold_price - 10, 2)
        target2 = round(gold_price - 20, 2)
        stoploss = round(gold_price + 8, 2)

    else:
        target1 = gold_price
        target2 = gold_price
        stoploss = gold_price

    return {
        "bias": bias,
        "confidence": confidence,
        "reasons": reasons,
        "entry": "انتظر انتهاء الخبر الاقتصادي القادم قبل الدخول.",
        "target1": target1,
        "target2": target2,
        "stoploss": stoploss
    }
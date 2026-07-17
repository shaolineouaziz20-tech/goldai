// ===============================
// تحديث سعر الذهب اللحظي
// ===============================
async function updateGoldPrice() {
    try {
        const response = await fetch("/api/gold-price");
        const data = await response.json();

        const priceElement = document.getElementById("gold-price");

        if (priceElement) {
            let price = data.gold_price || data.price;

            if (price && price !== "N/A" && price !== "undefined") {
                priceElement.innerText = "$" + price;
            } else if (priceElement.innerText === "---") {
                priceElement.innerText = "جاري جلب السعر...";
            }
        }

    } catch (error) {
        console.log("Error updating gold price:", error);
    }
}

// تحديث السعر كل 3 ثواني
setInterval(updateGoldPrice, 3000);
updateGoldPrice();


// ===============================
// تحليل الأخبار يدوياً
// ===============================
const analyzeBtn = document.getElementById("analyzeNewsBtn");

if (analyzeBtn) {

    analyzeBtn.addEventListener("click", async () => {

        const text = document.getElementById("newsInput").value;

        if (!text.trim()) {
            alert("الرجاء إدخال نص الأخبار أولاً!");
            return;
        }

        document.getElementById("parsedNews").innerHTML = "<p>⌛ جاري تحليل الأخبار...</p>";

        try {
            const response = await fetch("/api/parse-news", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text })
            });

            const news = await response.json();

            let html = "";

            if (!news || news.length === 0) {
                html = "<p>❌ لم يتم العثور على أخبار مهمة.</p>";
            } else {
                news.forEach(item => {
                    html += `
                    <div class="card" style="margin-top:15px; border-right: 4px solid #ffd700;">
                        <h3>${item.title || 'خبر اقتصادي'}</h3>
                        <p><strong>💵 العملة:</strong> ${item.currency || 'USD'}</p>
                        <p><strong>📊 التأثير:</strong> ${item.effect || 'غير محدد'}</p>
                        <p><strong>📖 السبب:</strong> ${item.reason || 'تحليل ذكاء اصطناعي'}</p>
                        <small>🕒 ${item.time || 'الآن'}</small>
                    </div>
                    `;
                });
            }

            document.getElementById("parsedNews").innerHTML = html;

        } catch (err) {
            console.error("Error analyzing news:", err);
            document.getElementById("parsedNews").innerHTML = "<p>❌ حدث خطأ أثناء التحليل.</p>";
        }

    });

}
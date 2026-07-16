// ===============================
// تحديث سعر الذهب
// ===============================
async function updateGoldPrice() {

    try {

        const response = await fetch("/api/gold-price");
        const data = await response.json();

        const priceElement = document.getElementById("gold-price");

        if (priceElement) {
            priceElement.innerText = "$" + data.gold_price;
        }

    } catch (error) {
        console.log(error);
    }

}

setInterval(updateGoldPrice, 3000);
updateGoldPrice();


// ===============================
// تحليل الأخبار
// ===============================
const analyzeBtn = document.getElementById("analyzeNewsBtn");

if (analyzeBtn) {

    analyzeBtn.addEventListener("click", async () => {

        const text = document.getElementById("newsInput").value;

        const response = await fetch("/api/parse-news", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });

        const news = await response.json();

        let html = "";

        if (news.length === 0) {

            html = "<p>❌ لم يتم العثور على أخبار مهمة.</p>";

        } else {

            news.forEach(item => {

                html += `
                <div class="card" style="margin-top:15px;">

                    <h3>${item.title}</h3>

                    <p><strong>💵 العملة:</strong> ${item.currency}</p>

                    <p><strong>📊 التأثير:</strong> ${item.effect}</p>

                    <p><strong>📖 السبب:</strong> ${item.reason}</p>

                    <p><strong>⭐ الأهمية:</strong> ${"⭐".repeat(item.stars)}</p>

                    <small>🕒 ${item.time}</small>

                </div>
                `;

            });

        }

        document.getElementById("parsedNews").innerHTML = html;

    });

}
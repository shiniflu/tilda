from flask import Flask, request
import requests

# 🔹 Вставьте токен Telegram-бота
TOKEN = "7592616557:AAGfVDs92i94sh8jQPbaLNI1UbkfPmskSyU"

# 🔹 Вставьте API-ключ OpenAI (ChatGPT)
OPENAI_API_KEY = "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"

# 🔹 URL для отправки сообщений в Telegram
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# 🔹 URL ChatGPT API
CHATGPT_URL = "https://api.openai.com/v1/chat/completions"

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json  # Получаем данные от Telegram

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # Отправляем запрос в ChatGPT API
        response = requests.post(
            CHATGPT_URL,
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": text}]}
        )

        # Получаем ответ от ChatGPT
        ai_response = response.json()["choices"][0]["message"]["content"]

        # Отправляем ответ пользователю в Telegram
        requests.get(TELEGRAM_URL, params={"chat_id": chat_id, "text": ai_response})

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

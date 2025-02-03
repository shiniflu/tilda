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
    app.run(port=5000)

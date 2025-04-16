from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI
import os
import threading
from flask import Flask

# Initialize Slack App and OpenAI Client
app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.command("/logdecision")
def log_decision(ack, respond, command):
    ack()
    text = command["text"]
    respond(f"✅ Decision logged: {text}")

@app.command("/trackupdate")
def track_update(ack, respond, command):
    ack()
    respond(f"📈 Project update noted: {command['text']}")

@app.command("/summary")
def summary(ack, respond, command):
    ack()
    dummy_data = """Team met. Funding discussed. Timeline Q4. Coordination with lab approved."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this text."},
                {"role": "user", "content": dummy_data}
            ],
            max_tokens=100
        )
        result = response.choices[0].message.content.strip()
        respond(f"🧠 Summary:\n{result}")
    except Exception as e:
        respond(f"Error generating summary: {str(e)}")

@app.event("app_mention")
def on_mention(event, say):
    say("👋 I'm CBCM Bot! Use `/logdecision`, `/trackupdate`, or `/summary`.")

# Dummy Flask server for Render free plan
dummy_app = Flask(__name__)

@dummy_app.route("/")
def home():
    return "CBCM Bot is alive and running!"

if __name__ == "__main__":
    def start_slack_bot():
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        handler.start()

    threading.Thread(target=start_slack_bot).start()
    dummy_app.run(host="0.0.0.0", port=3000)


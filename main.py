
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai
import os
import threading
from flask import Flask

# Initialize Slack App
app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])
openai.api_key = os.environ.get("OPENAI_API_KEY")

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this text."},
                {"role": "user", "content": dummy_data}
            ],
            max_tokens=100
        )
        result = response.choices[0].message['content'].strip()
        respond(f"🧠 Summary:\n{result}")
    except Exception as e:
        respond(f"Error: {e}")

@app.event("app_mention")
def on_mention(event, say):
    say("👋 I'm CBCM Bot! Use `/logdecision`, `/trackupdate`, or `/summary`.")

# Dummy Flask web server to keep Render happy
dummy_app = Flask(__name__)

@dummy_app.route("/")
def home():
    return "CBCM Bot is alive!"

if __name__ == "__main__":
    # Run Slack bot in a thread
    def start_slack():
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        handler.start()

    threading.Thread(target=start_slack).start()

    # Run dummy Flask server
    dummy_app.run(host="0.0.0.0", port=3000)

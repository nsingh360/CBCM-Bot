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
    respond("🧠 Summary:\nThis is a placeholder summary. Add OpenAI or HF model for full functionality.")

@app.command("/grantstatus")
def grant_status(ack, respond, command):
    ack()
    respond("📄 Grant Summary:\n• Title: NSF Research Fund\n• Status: Pending Review\n• Last Updated: April 10, 2025")
    
@app.command("/teamreminder")
def team_reminder(ack, respond, command):
    ack()
    respond("📢 Reminder sent to @team to update their project logs before Friday.")

@app.command("/decisionlog")
def decision_log(ack, respond, command):
    ack()
    respond("🧾 Last Logged Decisions:\n1. Switch from AWS to GCP for deployment\n2. Include Slack integration in MVP\n3. Submit ethics form before May")

@app.command("/helpcbc")
def help_cbc(ack, respond, command):
    ack()
    respond("""🧠 CBCM Bot Commands:
• `/logdecision [text]` – Log a project decision
• `/trackupdate [text]` – Record project progress
• `/summary` – Summarize key activity
• `/grantstatus` – View grant status
• `/teamreminder` – Nudge your team
• `/decisionlog` – View recent decisions""")

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


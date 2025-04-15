# CBCM Slack Bot 🤖

A context-based configuration management bot for researchers & students. Integrated with Slack, powered by OpenAI (GPT-3.5).

## 🛠 Features
- `/logdecision` – Log important decisions
- `/trackupdate` – Post progress updates
- `/summary` – Summarize recent project actions

## 🚀 Deploy to Render
1. Clone this repo to GitHub
2. Go to https://render.com → Create New → Web Service
3. Connect your GitHub repo
4. Choose **Free Plan**
5. Add these environment variables in the Render dashboard:
   - `SLACK_BOT_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `SLACK_APP_TOKEN`
   - `OPENAI_API_KEY`
6. Click Deploy 🎉

## 📦 Requirements
- Slack App with:
  - Slash commands (`/logdecision`, `/trackupdate`, `/summary`)
  - Events enabled: `app_mention`
  - Socket Mode enabled

## ✅ Tips
- Use GPT-3.5 to maximize free token usage
- Monitor OpenAI credits at https://platform.openai.com/account/usage

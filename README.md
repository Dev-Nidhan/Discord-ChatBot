# 🤖 Maxx Discord Bot

Maxx is a simple Discord bot I built using **Python** and **discord.py**.

I made it to combine a few useful and fun features in one bot — you can chat with an AI, get motivational quotes, fetch random memes, check the bot's latency, and manage messages from Discord itself.

The AI part uses **OpenRouter**, and the bot has multiple models as fallbacks so that if one model doesn't work, it can try another one.

## What can it do?

Here are the commands currently available:

| Command                  | What it does                             |
| ------------------------ | ---------------------------------------- |
| `maxx hello`             | Says hello 👋                            |
| `maxx chat <message>`    | Chat with the AI 🤖                      |
| `maxx chat test`         | Test the AI connection                   |
| `maxx motivate`          | Gives you a random motivational quote 💡 |
| `maxx meme`              | Sends a random meme 😂                   |
| `maxx ping`              | Shows the bot's latency 🏓               |
| `maxx diagnose`          | Checks the OpenRouter API connection     |
| `maxx antispam <number>` | Deletes recent messages 🧹               |

For example:

```text
maxx chat explain inheritance in python
```

The bot sends the question to the AI and replies with the response.

## 🧠 AI Chat

For the AI functionality, I used **OpenRouter**.

The bot tries different models one after another instead of depending on only one model. If a model fails or returns an empty response, it moves on to the next one.

This was mainly done so the AI feature doesn't completely stop working just because one model is unavailable.

## 🔑 API Keys

The bot needs two environment variables:

```env
TOKEN=your_discord_bot_token
DeepseekR1=your_openrouter_api_key
```

The code reads these values from the environment rather than putting the keys directly in the source code.

**Don't put your actual tokens or API keys on GitHub.**

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Install the required packages

```bash
pip install discord.py requests
```

Or install them from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Add your environment variables

Set your Discord bot token and OpenRouter API key:

```env
TOKEN=your_discord_bot_token
DeepseekR1=your_openrouter_api_key
```

### 4. Run the bot

```bash
python main.py
```

If everything is set up correctly, the bot will log in and you'll see a message in the console when it comes online.

## 🛠️ Built With

* Python
* discord.py
* OpenRouter
* Requests
* ZenQuotes API
* Meme API

## 📌 A few things to know

The bot reads Discord message content because the custom commands use messages such as `maxx chat` and `maxx meme`. The Message Content Intent is enabled in the code.

The `maxx antispam` command currently works by deleting a specified number of recent messages and requires the user to have **Manage Messages** permission.

## 🔮 Things I want to improve

There are still a few things I'd like to add or improve in the future:

* Better moderation and anti-spam features
* More Discord commands
* Proper slash-command support
* Better error handling
* More AI features
* Conversation history
* Server-specific settings
* A proper help command

## 📂 Project Structure

For now, the project is pretty small:

```text
Maxx-Discord-Bot/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ❤️ Why I made this

This project was mainly a way for me to learn more about **Python, APIs, Discord bots, and working with AI models**.

It's still a work in progress, and I'm planning to keep adding features as I learn more.

---

**If you like the project, feel free to ⭐ the repository!**

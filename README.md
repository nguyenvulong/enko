# 🌐 Discord Translate Bot (EN ↔ KR)

A Discord slash-command bot that auto-detects English or Korean input and translates it to the other language using the **Gemini API**.

---

## 📁 Project Structure

```
discord-translate-bot/
├── bot.py              # Main bot logic
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md
```

---

## ⚙️ Setup

### 1. Clone / copy the project

```bash
cd discord-translate-bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate.bat     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

| Variable | Where to get it |
|---|---|
| `DISCORD_TOKEN` | [Discord Developer Portal](https://discord.com/developers/applications) → Your App → Bot → Token |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) |

### 5. Discord bot permissions

When inviting the bot to your server, make sure to enable:
- **Bot** scope
- **applications.commands** scope (required for slash commands)
- **Send Messages** + **Embed Links** permissions

In the Developer Portal → Your App → Bot, also enable:
- ✅ **Message Content Intent** (under Privileged Gateway Intents)

### 6. Run the bot

```bash
python bot.py
```

You should see:
```
✅ Logged in as YourBot#1234 — synced 1 slash command(s).
```

> **Note:** Slash commands can take up to 1 hour to propagate globally on Discord. For instant sync during development, you can scope the bot to a specific guild (server) — see the tip below.

---

## 💬 Usage

In any channel where the bot has access, type:

```
/translate text: Hello, how are you?
/translate text: 안녕하세요, 잘 지내세요?
```

The bot will automatically detect the input language and translate to the other one, displaying a formatted embed with both the original and translated text.

---

## 🛠️ Dev tip — instant guild-scoped sync

To skip the global sync delay during testing, add your server ID and replace the sync in `on_ready`:

```python
MY_GUILD = discord.Object(id=YOUR_SERVER_ID_HERE)

@bot.event
async def on_ready():
    bot.tree.copy_global_to(guild=MY_GUILD)
    synced = await bot.tree.sync(guild=MY_GUILD)
    print(f"✅ {bot.user} — synced {len(synced)} command(s) to guild.")
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `discord.py` | Discord API wrapper with slash command support |
| `google-genai` | Gemini API client |
| `python-dotenv` | Load `.env` variables |

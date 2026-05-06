import os
import discord
from discord import app_commands
from discord.ext import commands
from google import genai
from dotenv import load_dotenv

# ── Load environment variables ──────────────────────────────────────────────
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not DISCORD_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Missing DISCORD_TOKEN or GEMINI_API_KEY in your .env file.")

# ── Configure Gemini (google-genai SDK) ──────────────────────────────────────
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# ── Discord bot setup (no message content intent needed for slash commands) ──
intents = discord.Intents.none()
bot = commands.Bot(command_prefix="/", intents=intents)


# ── Helper: detect language and translate ────────────────────────────────────
async def translate_text(text: str) -> tuple[str, str, str]:
    """
    Detects whether the input is English or Korean,
    then translates to the other language.

    Returns:
        (detected_language, target_language, translated_text)
    """
    prompt = f"""You are a professional translator between English and Korean.

First, detect whether the following text is in English or Korean.
Then translate it to the other language.

Respond ONLY in this exact format (no extra explanation):
DETECTED: <English or Korean>
TRANSLATION: <translated text>

Text to translate:
{text}"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    result = response.text.strip()

    # Parse the structured response
    detected = "Unknown"
    translation = result

    for line in result.splitlines():
        if line.startswith("DETECTED:"):
            detected = line.replace("DETECTED:", "").strip()
        elif line.startswith("TRANSLATION:"):
            translation = line.replace("TRANSLATION:", "").strip()

    target = "Korean" if detected == "English" else "English"
    return detected, target, translation


# ── Event: bot is ready ──────────────────────────────────────────────────────
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Logged in as {bot.user} — synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")


# ── Slash command: /translate ────────────────────────────────────────────────
@bot.tree.command(
    name="translate",
    description="Translate text between English and Korean automatically.",
)
@app_commands.describe(text="The text you want to translate (English ↔ Korean)")
async def translate(interaction: discord.Interaction, text: str):
    # Defer the reply so Discord doesn't time out while Gemini is thinking
    await interaction.response.defer(thinking=True)

    try:
        detected, target, translation = await translate_text(text)

        # Build a nice embed response
        flag_from = "🇺🇸" if detected == "English" else "🇰🇷"
        flag_to   = "🇰🇷" if target   == "Korean"  else "🇺🇸"

        embed = discord.Embed(
            title="🌐 Translation",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name=f"{flag_from}",
            value=f"```{text}```",
            inline=False,
        )
        embed.add_field(
            name=f"{flag_to}",
            value=f"```{translation}```",
            inline=False,
        )
        embed.set_footer(text="Powered by Gemini AI • type `/translate` to use")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(
            f"❌ Translation failed: `{e}`\nPlease try again later.",
            ephemeral=True,
        )


# ── Run the bot ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

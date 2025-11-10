"""
Radhe Guardian Bot — Start & Help 
----------------------------------------------
All buttons open new messages instead of editing previous ones.
Smooth callback handling for Heroku & VPS.
"""

from RADHE import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ==========================
# ⚙️ Configurable Section
# ==========================
START_IMG = "https://files.catbox.moe/svssj2.jpg"
CHANNEL_URL = "https://t.me/YourChannel"
SUPPORT_URL = "https://t.me/YourSupportGroup"
BOT_USERNAME = "RadheGuardianBot"


# ==========================
# 🟢 /start Command
# ==========================
@app.on_message(filters.command("start"))
async def start_cmd(_, m):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me In Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("🧩 Support", url=SUPPORT_URL),
            InlineKeyboardButton("📢 Updates", url=CHANNEL_URL),
        ],
        [InlineKeyboardButton("🆘 Help & Commands", callback_data="help_menu")]
    ])

    await m.reply_photo(
        photo=START_IMG,
        caption=(
            "**🕉️ Radhe Guardian Bot**\n\n"
            "A powerful & reliable moderation bot for Telegram groups.\n"
            "Automatically controls spam, links, and abusive content.\n\n"
            "Tap below to explore available commands 👇"
        ),
        reply_markup=buttons,
        quote=True
    )


# ==========================
# 🆘 /help Command
# ==========================
@app.on_message(filters.command("help"))
async def help_cmd(_, m):
    await send_help_menu(m)


# ==========================
# 📚 CALLBACK HANDLERS
# ==========================
@app.on_callback_query(filters.regex("^help_menu$"))
async def help_menu_callback(_, query: CallbackQuery):
    await send_help_menu(query.message)


async def send_help_menu(m):
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔗 BioLink Filter", callback_data="help_biolink"),
            InlineKeyboardButton("🚫 Abuse Filter", callback_data="help_abuse"),
        ],
        [InlineKeyboardButton("🛡️ Admin Tools", callback_data="help_admin")],
        [
            InlineKeyboardButton("📢 Broadcast", callback_data="help_broadcast"),
            InlineKeyboardButton("♻️ Restart", callback_data="help_restart"),
        ],
        [InlineKeyboardButton("← Back", callback_data="back_start")]
    ])

    await m.reply_photo(
        photo=START_IMG,
        caption="**🆘 Help & Commands**\n\nChoose a category below to view available commands 👇",
        reply_markup=buttons,
        quote=True
    )


# ==========================
# 📄 Each Help Section
# ==========================
HELP_TEXTS = {
    "help_biolink": (
        "**🔗 BioLink Filter**\n\n"
        "`/biolink on` — Enable link deletion\n"
        "`/biolink off` — Disable link deletion\n\n"
        "Deletes messages containing Telegram links, websites, or @usernames."
    ),
    "help_abuse": (
        "**🚫 Abuse Filter**\n\n"
        "`/abuse on` — Enable abuse filter\n"
        "`/abuse off` — Disable abuse filter\n\n"
        "Automatically deletes messages containing words from `abuse.txt`."
    ),
    "help_admin": (
        "**🛡️ Admin Commands**\n\n"
        "`/warn` — Warn a user (3 warns = mute)\n"
        "`/unwarn` — Clear warnings\n"
        "`/mute` — Mute a user\n"
        "`/unmute` — Unmute a user\n"
        "`/ban` — Ban a user\n"
        "`/unban` — Unban a user\n\n"
        "🔒 Only admins can use these commands."
    ),
    "help_broadcast": (
        "**📢 Broadcast (Owner Only)**\n\n"
        "`/broadcast` — Reply to a message and send it to all chats.\n\n"
        "⚠️ Only the bot owner can use this command."
    ),
    "help_restart": (
        "**♻️ Restart (Owner Only)**\n\n"
        "`/restart` — Safely restarts the bot and reloads all modules."
    )
}


# Dynamically register callback handlers
for key, text in HELP_TEXTS.items():
    @app.on_callback_query(filters.regex(f"^{key}$"))
    async def help_section(_, query: CallbackQuery, t=text):
        await query.message.reply_text(
            t,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("← Back", callback_data="help_menu")]]),
            quote=True
        )


# ==========================
# ⬅️ Back to Start
# ==========================
@app.on_callback_query(filters.regex("^back_start$"))
async def back_to_start(_, query: CallbackQuery):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me In Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("🧩 Support", url=SUPPORT_URL),
            InlineKeyboardButton("📢 Updates", url=CHANNEL_URL),
        ],
        [InlineKeyboardButton("🆘 Help & Commands", callback_data="help_menu")]
    ])

    await query.message.reply_photo(
        photo=START_IMG,
        caption=(
            "**🕉️ Radhe Guardian Bot**\n\n"
            "A powerful & reliable moderation bot for Telegram groups.\n"
            "Automatically controls spam, links, and abusive content."
        ),
        reply_markup=buttons,
        quote=True
    )

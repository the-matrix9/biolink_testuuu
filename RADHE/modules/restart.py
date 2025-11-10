import os
import sys
import logging
from pyrogram import filters
from RADHE import app

# Setup logging
log = logging.getLogger("RADHE.modules.restart")

OWNER_ID = int(os.getenv("BOT_OWNER"))


# ===============================
# ♻️ /restart (Owner Only)
# ===============================
@app.on_message(filters.command("restart"))
async def restart_cmd(_, m):
    # Allow only private chats & owner
    if m.chat.type != "private":
        return await m.reply_text("⚠️ Restart command can only be used in bot PM.", quote=True)

    if m.from_user.id != OWNER_ID:
        return await m.reply_text("⚠️ Only the bot owner can restart the bot.", quote=True)

    await m.reply_text("♻️ Restarting bot... please wait 3–5 seconds.", quote=True)

    try:
        log.info("♻️ Restart command received — restarting bot process.")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        log.error(f"❌ Restart failed: {e}")
        await m.reply_text(f"❌ Failed to restart bot.\nError: <code>{e}</code>", parse_mode="html")

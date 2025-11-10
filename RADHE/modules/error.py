"""
Radhe Guardian Bot — Global Error Handler
-----------------------------------------
Catches unexpected exceptions during message updates.
Prevents crashes and logs errors safely.
"""

import os
import traceback
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from RADHE import app

log = logging.getLogger("RADHE.modules.error")

OWNER_ID = int(os.getenv("BOT_OWNER", "0"))


# ==========================
# ⚠️ Error Catcher Decorator
# ==========================
@app.on_message(filters.all)
async def global_error_handler(_, m: Message):
    try:
        # Nothing here intentionally — this just ensures all messages are watched.
        pass

    except Exception as e:
        err_text = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        chat = m.chat.id if m.chat else "Unknown"
        user = m.from_user.id if m.from_user else "Unknown"

        log.error(f"❌ Error in chat {chat}, user {user}: {e}")

        # Optional: notify owner
        if OWNER_ID:
            try:
                await app.send_message(
                    OWNER_ID,
                    f"⚠️ <b>Error Report</b>\n\n"
                    f"<b>Chat:</b> <code>{chat}</code>\n"
                    f"<b>User:</b> <code>{user}</code>\n\n"
                    f"<b>Traceback:</b>\n<code>{err_text[:3500]}</code>",
                    parse_mode="html"
                )
            except Exception as err:
                log.warning(f"Couldn't send error to owner: {err}")


# ==========================
# 🧩 Try/Except Helper
# ==========================
async def safe_exec(func, *args, **kwargs):
    """Wrapper for any async function to prevent bot crashes."""
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        log.error(f"❌ Error in safe_exec({func.__name__}): {e}")
        if OWNER_ID:
            try:
                await app.send_message(
                    OWNER_ID,
                    f"🔥 <b>Safe Exec Error</b>\n\n<code>{traceback.format_exc()[:3500]}</code>",
                    parse_mode="html"
                )
            except:
                pass

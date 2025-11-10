"""
Radhe Guardian Bot — BioLink Filter
-----------------------------------
Deletes messages containing Telegram links, websites, or @usernames.
"""

from pyrogram import filters
from pyrogram.types import Message
from RADHE.core.database import db
from RADHE.core.utils import is_admin
import re
from RADHE import app

biolink_settings = db["biolink_settings"] if db is not None else None
auth_users = db["auth_users"] if db is not None else None

LINK_REGEX = re.compile(r"(https?://|t\.me/|@[\w_]+|www\.|\.com|\.in|\.org)", re.IGNORECASE)


# ===============================
# 🔘 Check if BioLink filter is ON
# ===============================
def is_biolink_on(chat_id: int):
    if db is None or biolink_settings is None:
        return False
    data = biolink_settings.find_one({"_id": chat_id})
    return data and data.get("enabled", True)


# ===============================
# 🚫 BioLink Filter Handler
# ===============================
@app.on_message(filters.text & filters.group)
async def biolink_filter(_, m: Message):
    if db is None or biolink_settings is None:
        return
    if not is_biolink_on(m.chat.id):
        return
    if await is_admin(m.chat.id, m.from_user.id):
        return
    if auth_users and auth_users.find_one({"_id": m.from_user.id}):
        return
    if LINK_REGEX.search(m.text):
        try:
            await m.delete()
            await m.reply_text("🚫 Links are not allowed here!", quote=True)
        except Exception:
            pass

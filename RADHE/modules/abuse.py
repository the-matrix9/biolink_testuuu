"""
Radhe Guardian Bot — Abuse Filter
---------------------------------
Deletes abusive messages based on words listed in abuse.txt.
"""

from pyrogram import filters
from RADHE.core.database import db
from RADHE.core.utils import is_admin
from RADHE import app

abuse_settings = db["abuse_settings"] if db is not None else None
auth_users = db["auth_users"] if db is not None else None
abuse_words = set()


# ===============================
# 🔤 Load abuse.txt words
# ===============================
def load_abuse_words():
    global abuse_words
    try:
        with open("abuse.txt", "r", encoding="utf-8") as f:
            for word in f:
                w = word.strip().lower()
                if w:
                    abuse_words.add(w)
        print(f"✅ Loaded {len(abuse_words)} abusive words.")
    except FileNotFoundError:
        print("⚠️ abuse.txt not found. Skipping word load.")
    except Exception as e:
        print(f"❌ Error loading abuse words: {e}")


# ===============================
# 🧩 Check if abuse filter ON
# ===============================
def is_abuse_on(chat_id: int):
    if db is None or abuse_settings is None:
        return False
    data = abuse_settings.find_one({"_id": chat_id})
    return data and data.get("enabled", True)


# ===============================
# 🚫 Filter messages
# ===============================
@app.on_message(filters.text & filters.group)
async def abuse_filter(_, m):
    if db is None or abuse_settings is None:
        return
    if not is_abuse_on(m.chat.id):
        return
    if await is_admin(m.chat.id, m.from_user.id):
        return
    if auth_users and auth_users.find_one({"_id": m.from_user.id}):
        return

    txt = m.text.lower()
    for word in abuse_words:
        if word in txt:
            try:
                await m.delete()
                await m.reply_text("⚠️ Avoid using abusive words.", quote=True)
            except Exception:
                pass
            break


# Load words when file imports
load_abuse_words()

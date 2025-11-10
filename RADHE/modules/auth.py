"""
Radhe Guardian Bot — Auth Module
--------------------------------
Manage authorized users who can bypass filters and restrictions.
"""

from pyrogram import filters
from RADHE.core.database import db
from RADHE.core.utils import is_admin
import os
from RADHE import app

OWNER_ID = int(os.getenv("BOT_OWNER", "0"))
auth_users = db["auth_users"] if db is not None else None


# ===========================
# 🔐 ADD AUTHORIZED USER
# ===========================
@app.on_message(filters.command("auth") & filters.group)
async def add_auth_user(_, m):
    if not (await is_admin(m.chat.id, m.from_user.id) or m.from_user.id == OWNER_ID):
        return await m.reply_text("⚠️ Only admins or the bot owner can authorize users.")
    if not m.reply_to_message:
        return await m.reply_text("Reply to a user's message to authorize them.")
    if db is None or auth_users is None:
        return await m.reply_text("❌ Database not connected.")

    user = m.reply_to_message.from_user
    auth_users.update_one({"_id": user.id}, {"$set": {"name": user.first_name}}, upsert=True)
    await m.reply_text(f"✅ {user.mention} has been authorized!\nThey can now bypass filters.")


# ===========================
# 🔓 REMOVE AUTHORIZED USER
# ===========================
@app.on_message(filters.command("unauth") & filters.group)
async def remove_auth_user(_, m):
    if not (await is_admin(m.chat.id, m.from_user.id) or m.from_user.id == OWNER_ID):
        return await m.reply_text("⚠️ Only admins or the bot owner can unauthorize users.")
    if not m.reply_to_message:
        return await m.reply_text("Reply to a user's message to unauthorize them.")
    if db is None or auth_users is None:
        return await m.reply_text("❌ Database not connected.")

    user = m.reply_to_message.from_user
    auth_users.delete_one({"_id": user.id})
    await m.reply_text(f"❌ {user.mention} removed from authorized list.\nThey will now be affected by filters again.")


# ===========================
# 📜 LIST AUTHORIZED USERS
# ===========================
@app.on_message(filters.command("authlist") & filters.group)
async def list_auth_users(_, m):
    if db is None or auth_users is None:
        return await m.reply_text("❌ Database not connected.")
    data = list(auth_users.find())
    if not data:
        return await m.reply_text("No authorized users found.")
    text = "👑 **Authorized Users:**\n\n"
    for user in data:
        text += f"• `{user['_id']}` - {user.get('name', 'Unknown')}\n"
    await m.reply_text(text)

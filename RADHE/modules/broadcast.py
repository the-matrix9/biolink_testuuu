"""
Radhe Guardian Bot — Broadcast (Owner Only)
-------------------------------------------
Only the BOT_OWNER can broadcast messages to all saved chats.
"""

import os
import logging
from pyrogram import filters
from pyrogram.types import Message
from RADHE import app
from RADHE.core.database import db

log = logging.getLogger("RADHE.modules.broadcast")

OWNER_ID = int(os.getenv("BOT_OWNER", "0"))
chats_col = db["chats"] if db is not None else None


# ===============================
# 🧩 Auto Save New Chat IDs
# ===============================
@app.on_message(filters.new_chat_members)
async def add_chat(_, m: Message):
    if db is None:
        return
    try:
        chats_col.update_one(
            {"_id": m.chat.id},
            {"$set": {"title": m.chat.title or 'Unknown Group'}},
            upsert=True,
        )
        log.info(f"✅ Saved chat: {m.chat.title} ({m.chat.id})")
    except Exception as e:
        log.warning(f"⚠️ Failed to save chat: {e}")


# ===============================
# 📢 /broadcast (Owner Only)
# ===============================
@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast(_, m: Message):
    if m.from_user.id != OWNER_ID:
        return await m.reply_text("⚠️ Only the bot owner can use /broadcast.", quote=True)

    if not m.reply_to_message:
        return await m.reply_text("Reply to a message to broadcast it to all chats.", quote=True)

    if db is None:
        return await m.reply_text("❌ Database not connected.", quote=True)

    msg = m.reply_to_message
    success, failed = 0, 0
    text = msg.text or msg.caption or ""

    chats = list(chats_col.find()) if chats_col is not None else []

    if not chats:
        return await m.reply_text("No chats found to broadcast.", quote=True)

    await m.reply_text(f"🚀 Starting broadcast to `{len(chats)}` chats...", quote=True)

    for chat in chats:
        chat_id = chat["_id"]
        try:
            if msg.text:
                await app.send_message(chat_id, text)
            elif msg.photo:
                await app.send_photo(chat_id, msg.photo.file_id, caption=text)
            elif msg.video:
                await app.send_video(chat_id, msg.video.file_id, caption=text)
            elif msg.document:
                await app.send_document(chat_id, msg.document.file_id, caption=text)
            success += 1
        except Exception as e:
            log.warning(f"❌ Failed to send message to {chat_id}: {e}")
            failed += 1
            continue

    result = (
        f"📢 <b>Broadcast Completed!</b>\n\n"
        f"✅ Sent: <code>{success}</code> chats\n"
        f"❌ Failed: <code>{failed}</code> chats"
    )

    await m.reply_text(result, quote=True, parse_mode="html")
    log.info(f"📢 Broadcast done: {success} success, {failed} failed")

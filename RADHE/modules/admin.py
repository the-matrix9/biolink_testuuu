import datetime
import logging
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions
from RADHE import app
from RADHE.core.database import db
from RADHE.core.utils import is_admin

log = logging.getLogger("RADHE.modules.admin")

# ✅ Fix for Heroku: avoid truth testing on Mongo DB
warns = db["warns"] if db is not None else None
MAX_WARNS = 3  # user muted after 3 warns

# ==============================
# ⚠️ WARN
# ==============================
@app.on_message(filters.command("warn") & filters.group)
async def warn_user(_, m: Message):
    if not m.from_user:
        return
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text("⚠️ Only admins can warn users.", quote=True)
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply_text("Reply to a user's message to warn them.", quote=True)

    user = m.reply_to_message.from_user
    key = {"_id": f"{m.chat.id}_{user.id}"}
    data = warns.find_one(key) if warns else None
    count = (data["count"] + 1) if data else 1

    if warns:
        warns.update_one(key, {"$set": {"count": count}}, upsert=True)

    if count >= MAX_WARNS:
        try:
            await app.restrict_chat_member(
                m.chat.id,
                user.id,
                ChatPermissions(can_send_messages=False)
            )
            if warns:
                warns.delete_one(key)
            await m.reply_text(
                f"🔇 <b>{user.first_name}</b> has been muted for exceeding {MAX_WARNS} warnings.",
                quote=True,
                parse_mode="html"
            )
            log.info(f"Muted {user.id} in {m.chat.id} for 3 warns.")
        except Exception as e:
            log.warning(f"Failed to mute {user.id}: {e}")
    else:
        await m.reply_text(
            f"⚠️ <b>{user.first_name}</b> has been warned! ({count}/{MAX_WARNS})",
            quote=True,
            parse_mode="html"
        )


# ==============================
# ♻️ UNWARN
# ==============================
@app.on_message(filters.command("unwarn") & filters.group)
async def unwarn_user(_, m: Message):
    if not m.from_user:
        return
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text("⚠️ Only admins can use this command.", quote=True)
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply_text("Reply to a user's message to clear warnings.", quote=True)

    user = m.reply_to_message.from_user
    key = {"_id": f"{m.chat.id}_{user.id}"}

    if warns:
        warns.delete_one(key)

    await m.reply_text(
        f"✅ <b>{user.first_name}</b>'s warnings have been cleared.",
        quote=True,
        parse_mode="html"
    )


# ==============================
# 🔇 MUTE
# ==============================
@app.on_message(filters.command("mute") & filters.group)
async def mute_user(_, m: Message):
    if not m.from_user:
        return
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text("⚠️ Only admins can mute users.", quote=True)
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply_text("Reply to a user's message to mute them.", quote=True)

    user = m.reply_to_message.from_user
    try:
        await app.restrict_chat_member(
            m.chat.id,
            user.id,
            ChatPermissions(can_send_messages=False)
        )
        await m.reply_text(
            f"🔇 <b>{user.first_name}</b> has been muted.",
            quote=True,
            parse_mode="html"
        )
        log.info(f"Muted {user.id} in {m.chat.id}")
    except Exception as e:
        await m.reply_text(f"❌ Failed to mute user: <code>{e}</code>", parse_mode="html")


# ==============================
# 🔊 UNMUTE
# ==============================
@app.on_message(filters.command("unmute") & filters.group)
async def unmute_user(_, m: Message):
    if not m.from_user:
        return
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text("⚠️ Only admins can unmute users.", quote=True)
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply_text("Reply to a user's message to unmute them.", quote=True)

    user = m.reply_to_message.from_user
    try:
        await app.restrict_chat_member(
            m.chat.id,
            user.id,
            ChatPermissions(can_send_messages=True)
        )
        await m.reply_text(
            f"🔊 <b>{user.first_name}</b> has been unmuted.",
            quote=True,
            parse_mode="html"
        )
        log.info(f"Unmuted {user.id} in {m.chat.id}")
    except Exception as e:
        await m.reply_text(f"❌ Failed to unmute user: <code>{e}</code>", parse_mode="html")


# ==============================
# 🚫 BAN
# ==============================
@app.on_message(filters.command("ban") & filters.group)
async def ban_user(_, m: Message):
    if not m.from_user:
        return
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text("⚠️ Only admins can ban users.", quote=True)
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply_text("Reply to a user's message to ban them.", quote=True)

    user = m.reply_to_message.from_user
    try:
        await app.ban_chat_member(m.chat.id, user.id)
        await m.reply_text(
            f"🚫 <b>{user.first_name}</b> has been banned from this group.",
            quote=True,
            parse_mode="html"
        )
        log.info(f"Banned {user.id} in {m.chat.id}")
    except Exception as e:
        await m.reply_text(f"❌ Failed to ban user: <code>{e}</code>", parse_mode="html")


# ==============================
# ✅ UNBAN
# ==============================
@app.on_message(filters.command("unban") & filters.group)
async def unban_user(_, m: Message):
    if not m.from_user:
        return
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply_text("⚠️ Only admins can unban users.", quote=True)
    if len(m.command) < 2 and not m.reply_to_message:
        return await m.reply_text("Usage: `/unban <user_id>` or reply to a user.", quote=True)

    if m.reply_to_message and m.reply_to_message.from_user:
        user_id = m.reply_to_message.from_user.id
    else:
        try:
            user_id = int(m.command[1])
        except ValueError:
            return await m.reply_text("❌ Invalid user ID.", quote=True)

    try:
        await app.unban_chat_member(m.chat.id, user_id)
        await m.reply_text(
            f"✅ User <code>{user_id}</code> has been unbanned.",
            quote=True,
            parse_mode="html"
        )
        log.info(f"Unbanned {user_id} in {m.chat.id}")
    except Exception as e:
        await m.reply_text(f"❌ Failed to unban: <code>{e}</code>", parse_mode="html")

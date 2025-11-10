import builtins
from RADHE import app

async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await builtins.app.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

import os
import builtins
import logging
from pyrogram import Client
from dotenv import load_dotenv
from RADHE.modules import load_all_modules

# ============================
# Load Environment
# ============================
load_dotenv()

# ============================
# Logging Setup
# ============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger("RadheGuardian")

# ============================
# Initialize Bot
# ============================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "radhe_guardian",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
builtins.app = app

# ============================
# Load All Modules
# ============================
try:
    load_all_modules()
    log.info("✅ All RADHE modules loaded successfully.")
except Exception as e:
    log.error(f"❌ Failed to load modules: {e}")

# ============================
# Run Bot
# ============================
if __name__ == "__main__":
    log.info("🚀 Starting Radhe Guardian Bot...")
    app.run()

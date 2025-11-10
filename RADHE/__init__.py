import logging
import os
from pyrogram import Client
import importlib

# ============================
# 🧠 Custom Logging Formatter
# ============================
class RadheFormatter(logging.Formatter):
    def format(self, record):
        # remove default module name/time
        emoji = "✅" if record.levelno == logging.INFO else "❌"
        return f"{emoji} {record.getMessage()}"

# Create handler
handler = logging.StreamHandler()
handler.setFormatter(RadheFormatter())

log = logging.getLogger("Radhe")
log.setLevel(logging.INFO)
log.addHandler(handler)

# ============================
# 🔥 Create app instance
# ============================
app = Client(
    "radheguardian",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# ============================
# 📦 Module Auto Loader
# ============================
def load_all_modules():
    modules_dir = os.path.join(os.path.dirname(__file__), "modules")
    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"RADHE.modules.{filename[:-3]}"
            try:
                importlib.import_module(module_name)
                log.info(f"Loaded module: {module_name}")
            except Exception as e:
                log.error(f"Failed to load {module_name}: {e}")

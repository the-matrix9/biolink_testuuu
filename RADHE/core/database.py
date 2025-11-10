import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
log = logging.getLogger("RADHE.core.database")

# ======================
# ⚙️ MongoDB Connection
# ======================
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "radhe_db")

if not MONGO_URI:
    log.error("❌ MONGO_URI is missing! Please set it in your environment variables.")
    mongo = None
    db = None
else:
    try:
        mongo = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        mongo.server_info()  # Test connection
        db = mongo[DB_NAME]
        log.info(f"✅ Connected to MongoDB database: {DB_NAME}")
    except Exception as e:
        log.error(f"❌ Failed to connect to MongoDB: {e}")
        mongo = None
        db = None

import logging
from RADHE import app

log = logging.getLogger("RADHE.core")

try:
    from .database import db
    from .utils import is_admin
    log.info("✅ Core modules loaded successfully: database, utils")
except Exception as e:
    log.error(f"❌ Failed to load core modules: {e}")

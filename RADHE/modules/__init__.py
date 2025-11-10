"""
Radhe Guardian Bot — Module Loader
----------------------------------
Safely auto-loads all modules in RADHE/modules/
with detailed logging and import error handling.
"""

import os
import importlib
import logging

log = logging.getLogger("RADHE.modules")


def load_all_modules():
    """Auto-load all modules inside RADHE/modules directory."""
    modules_dir = os.path.dirname(__file__)
    module_files = [
        f[:-3] for f in os.listdir(modules_dir)
        if f.endswith(".py") and not f.startswith("__")
    ]

    total = len(module_files)
    success = 0

    for name in module_files:
        module_path = f"RADHE.modules.{name}"
        try:
            importlib.import_module(module_path)
            log.info(f"✅ Loaded module: {module_path}")
            success += 1
        except Exception as e:
            log.error(f"❌ Failed to load {module_path}: {e}")

    log.info(f"📦 Module load complete: {success}/{total} modules loaded successfully.")


# Optional: Auto-run only if executed directly
if __name__ == "__main__":
    load_all_modules()

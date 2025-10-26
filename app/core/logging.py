
import logging, os
LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LEVEL, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("carbot")

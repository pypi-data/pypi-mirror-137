import logging
import sys

from znipy.core.loader import NotebookLoader

__all__ = [NotebookLoader.__name__]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Formatter for advanced logging
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter("%(asctime)s %(module)s (%(levelname)s): %(message)s")

channel = logging.StreamHandler(sys.stdout)
channel.setLevel(logging.DEBUG)
channel.setFormatter(formatter)

logger.addHandler(channel)

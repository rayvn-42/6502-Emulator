# Import module testing libraries
import logging # for module logging purposes, not necessary for computer runtime
import datetime #
#################

from . import Cpu
from . import Memory

__all__ = ["Cpu", "Memory"]
__author__ = 'Rayan Berrabah'
__email__ = 'rayanexpro7@gmail.com'
__version__ = '0.1.0'
__date__ = 'dd-mm-yy'

''' Code used for logging purposes, not needed for typical use.

logging .basicConfig(
    level=logging.INFO,
    filename='Computer.log'
)

logger = logging.getLogger(__name__)

logger.info(f"Computer has been intialized at: {datetime.datetime.now()}")
'''
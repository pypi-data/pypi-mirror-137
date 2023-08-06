"""
More info at ProjectKaren.Ai
"""

from .templates import GenericContainer, GenericDevice
from .skillmanager import GenericSkill

VERSION = (0, 8, 0)

__app_name__ = "karen"
__app_title__ = "K-REN"
__version__ = ".".join([str(x) for x in VERSION])

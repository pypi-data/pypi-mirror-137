"""
discord.io
~~~~~~~~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021-present VincentRPS
:license: MIT
"""

__title__: str = "discord.io"
__author__: str = "VincentRPS"
__license__: str = "MIT"
__copyright__: str = "Copyright 2021-present VincentRPS"
__version__: str = "0.6.1"

import logging
import typing

from .api import *
from .apps import *
from .audio import *
from .cache import *
from .color import *
from .colour import *
from .components import *
from .events import *
from .intents import *
from .interactions import *
from .internal.exceptions import *
from .internal.warnings import *
from .modules import *
from .snowflake import *
from .state import *
from .traits import *
from .types import *
from .ui import *
from .util import *
from .webhooks import *


class VersionInfo(typing.NamedTuple):
    major: str
    minor: str
    micro: str
    releaselevel: typing.Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=6, micro=1, releaselevel="final", serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__: typing.List[str] = [
    "__title__",
    "__author__",
    "__license__",
    "__copyright__",
    "__version__",
    "VersionInfo",
    "version_info",
]

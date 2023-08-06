# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
"""
The ConnectionState Caches most things during connection.
"""
import asyncio
from collections import OrderedDict
from typing import Any, Callable, Coroutine, List, Tuple, TypeVar, Union

from discord.types.dict import Dict

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]


class Hold:
    """A hold of cache, easily swapable with a db."""

    def __init__(self):
        self.__cache = OrderedDict()

    def view(self) -> List[Dict]:
        return [value for value in self.__cache.values()]

    def list(self):
        return self.__cache.items()

    def new(self, name: str, data: Union[str, int, Dict, Any]):
        self.__cache[name] = data

    def edit(self, name: str, data: Union[str, int, Dict, Any]):
        self.__cache.update({name: data})

    def get(self, name: str):
        return self.__cache.get(name)

    def pop(self, name: str):
        return self.__cache.pop(name)

    def reset(self) -> None:
        del self.__cache


class ConnectionState:
    """The Connection State

    .. versionadded:: 0.4.0

    .. note::

        The connection state is responsible for caching
        everything, meaning most classes will depend on it.

    .. note::

        .. data:: ConnectionState._speaking

        is planned to be deprecated soon.

    Attributes
    ----------
    _bot_intents :class:`int`
        The cached bot intents, used for Gateway

    _session_id :class:`int`
        The Gateway, session id

    _voice_session_id :class:`int`
        The Voice Gateway Session ID

    _seq :class:`int`
        The Gateway seq number, can be None.

    app :class:`Client`
        The bot app

        .. versionadded:: 0.5.0

    _voice_seq :class:`int`
        The Voice Gateway seq

        .. versionadded:: 0.5.0

    _voice_user_data :class:`dict`
        The Voice User Data given by the Voice Gateway.

        .. versionadded:: 0.5.0

    _speaking :class:`bool`
        If the bot is currently speaking, defaults False

        .. versionadded:: 0.5.0

    _said_hello :class:`bool`
        If the Gateway got a hello or not.

    loop :class:`asyncio.AbstractEventLoop`
        The current loop

    _bot_presences :class:`list`
        A list of the bots presences

    _bot_status :class:`str`
        The bot status, e.g. online

    _bot_presence_type :class:`int`
        The bot presence type, defaults to 0

    listeners :class:`dict`
        The bot listeners

    shard_count :class:`int`
        the number of shards.

        .. versionadded:: 0.6.0
    """

    def __init__(self, **options):
        self._guilds_cache = options.get("guild_cache_hold") or Hold()
        self._sent_messages_cache = options.get("sent_messages_cache_hold") or Hold()
        self._edited_messages_cache = (
            options.get("edited_messages_cache_hold") or Hold()
        )
        self._deleted_messages_cache = (
            options.get("deleted_messages_cache_hold") or Hold()
        )
        self._ready: asyncio.Event = asyncio.Event()

        self._bot_intents: int = options.get("intents", 0)
        """The cached bot intents, used for Gateway"""

        self._bot_id: int = None

        self._voice_session_id: int = None

        self._seq: int = None
        """The seq number"""

        self.app = options.get("bot", None)
        """The bot app"""

        self._voice_seq: int = None
        """The Voice Gateway seq"""

        self._voice_user_data: Dict = {}
        """The Voice User Data given by the Voice Gateway."""

        self._speaking: bool = False
        """If the bot is currently speaking"""

        self._said_hello: bool = False
        """If the Gateway got a hello or not."""

        self.loop: asyncio.AbstractEventLoop = options.get("loop", None)
        """The current loop"""

        self._bot_presences: list[str, Any] = []
        """The precenses"""

        self._bot_status: str = "online"
        """The status"""

        self._bot_presence_type: int = 0
        """Precense type"""

        self.listeners: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        """The listeners"""

        self.shard_count: int = options.get("shard_count")
        """The shard count"""

        self.components = {}

        self.prefixed_commands: dict[str, List[CoroFunc]] = {}

        self.application_commands: dict[str, List[CoroFunc]] = {}

        self.prefix = options.get("prefix")

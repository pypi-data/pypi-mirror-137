"""
The MIT License (MIT)

Copyright (c) 2022-2022 Caeden

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from disnake import Forbidden, InvalidArgument, Member, Message
from disnake.ext.commands import Bot

from .errors import AmbigiousArgumentError
from .constants import AUTO_KICK
from typing import Any, Dict, List, Optional


class Config:
    """
    Represents the database config.

    Parameters
    ----------
    lock_database: `bool`
        Determines whether or not the database server should be locked
        and no members can join the server
    force_lock: `bool`
        Determines whether to force kick everyone in the database server
    whitelisted_members: `List[int]`
        List of user ids that are allowed inside the database server
    """

    lock_database: bool
    force_lock: bool
    whitelisted_members: List[int]

    @classmethod
    def from_dict(cls, dict: Dict[str, str]):
        cls = Config
        if "lock_database" in dict:
            cls.lock_database = dict["lock_database"]
        if "force_lock" in dict:
            cls.force_lock = dict["force_lock"]
        if "whitelisted_members" in dict:
            cls.whitelisted_members = dict["whitelisted_members"]
        return cls


class Field:
    """
    Represents a database field.

    Parameters
    ----------

    table: Table
        The parent table class that
        the field is inside.
    """

    table: Table


class Table:
    """
    Represents a database table.

    Parameters
    ----------
    name: str
        The name of the table.
    id: int
        The id of the table.
    fields: List[Field]
        The fields within the table.
    """

    name: str
    id: int
    fields: List[Field]


class Database:
    """
    Represents a database connection
    This class is used to interact with the Discord Database server

    Parameters
    ----------
    database_server: `int`
        The discord server to read, write and edit data from.

        .. versionadded:: 0.1
    """

    def __init__(self, *, database_server: int):
        self._database_server = database_server
        self._tables = {}

    def find_table(self, *, id: int = None, name: str = None) -> Optional[Table]:
        """
        Search cache for table with either id or name.

        Parameters
        ----------
        id: int
            id to find table by.
        name: str
            name to find table by.

        Returns
        -------
        Optional[Table]
            Returns a table if found.
        """

        if not id or name:
            raise InvalidArgument("You need to specify an int or name to search for")

        if id:
            tables = [table for table in list(self._tables.keys) if table.id == id][0]
            if tables:
                return tables
        if name:
            tables = [table for table in list(self._tables.keys) if table.name == name]
            if len(tables) >= 2:
                raise AmbigiousArgumentError(
                    f"There are multiple tables with name {name}"
                )
            if tables:
                return tables[0]
        return None

    async def _cache_messages(self) -> None:
        """
        |coro|

        Caches all the messages into parsable data for easy
        response times under load.
        """

        for channel in self.database_server.text_channels:
            if channel.topic == ":: TABLE ::":
                if channel not in self._tables:
                    self._tables[channel] = []

    async def _lock_down(self):
        """
        |coro|

        Locks down a database server so that no unauthorized
        members can view and access data.
        """

        for member in self.database_server.members:
            if member.id not in self.whitelisted_members:
                try:
                    await member.kick(reason=AUTO_KICK)
                except Forbidden:
                    pass

    async def _on_member_join(self, member: Member) -> None:
        """
        |coro|

        Automatically kicks a member from database server
        if the database is locked.

        Parameters
        ----------
        member: `disnake.Member`
            The member to kick.
        """

        if member.guild.id != self.database_server.id:
            return
        if member.id in self.allowed_members:
            await member.kick(reason=AUTO_KICK)

    async def _on_message(self, message: Message) -> None:
        """
        |coro|

        Automatically deletes a message if its not from the
        bot and it is in a table channel.
        """

    async def start(self, bot: Bot, *, config: Config) -> None:
        """
        |coro|

        Connects the database to discord to cache
        data and messages.

        Parameters
        ----------
        bot: `disnake.ext.commands.Bot`
            The global bot to use to read messages and cache data.
        config: `Config`
            The configuration to use for the server.
        """

        self.bot = bot
        self.database_server = bot.get_guild(self._database_server)
        self.whitelisted_members = getattr(config, "whitelisted_members", [])

        if config.lock_database:
            bot.add_listener(self._on_member_join, "on_member_join")
        if config.force_lock:
            await self._lock_down()
        await self._cache_messages()

    async def create_table(self, name: str) -> Table:
        """
        |coro|

        Creates a table to store data in.

        Parameters
        ----------
        name: str
            The name to create the table as.
        data_types: List[Any]
            The data types to store within the table
            A new field will be created for each

        Returns
        -------
        Table:
            The table that is created.
        """

        await self.database_server.create_text_channel(name=name, topic=":: TABLE ::")

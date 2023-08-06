"""
MIT License

Copyright (c) 2020 Gabriel Huber
Copyright (c) 2022 Anggara Yama Putra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from .common import BufferExhaustedError, \
    DEFAULT_TIMEOUT, DEFAULT_ENCODING, \
    ByteReader, \
    DataclsMeta, \
    TYPE_ADDRESS, BaseResponseFragment, GoldSrcResponseFragment;
from .connection import request, request_async, BaseStreamMutator, GenericStreamMutator, BaseQueryProtocol;



A2S_INFO_RESPONSE = 0x49;
A2S_INFO_RESPONSE_LEGACY = 0x6D;


class SourceInfo (metaclass=DataclsMeta):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#Response_Format
    """
    protocol: int;
    """Protocol version used by the server."""

    server_name: str;
    """Display name of the server."""

    map_name: str;
    """The currently loaded map."""

    folder: str;
    """Name of the game directory."""

    game: str;
    """Name of the game."""

    app_id: int;
    """App ID of the game required to connect."""

    player_count: int;
    """Number of players currently connected."""

    max_players: int;
    """Number of player slots available."""

    bot_count: int;
    """Number of bots on the server."""

    server_type: str;
    """Type of the server:
    'd': Dedicated server.
    'l': Non-dedicated server.
    'p': SourceTV relay (proxy)."""

    platform: str;
    """Operating system of the server
    'l': Linux.
    'w': Windows.
    'm' or 'o' (Deprecated): macOS (the code changed after L4D1)."""

    password_protected: bool;
    """Server requires a password to connect."""

    vac_enabled: bool;
    """Server has VAC enabled."""

    version: str;
    """Version of the server software."""

    edf: int = 0;
    """Optional:
    Extra data field, used to indicate if extra values are
    included in the response."""

    port: int;
    """Port of the game server."""

    steam_id: int;
    """Steam ID of the server."""

    stv_port: int;
    """Port of the SourceTV server."""

    stv_name: str;
    """Name of the SourceTV server."""

    keywords: str;
    """Tags that describe the gamemode being played."""

    game_id: int;
    """Game ID for games that have an app ID too high for 16bit."""

    ping: float;
    """Client determined values:
    Round-trip delay time for the request in seconds."""

    @property
    def has_port (self):
        return bool( self.edf & 0x80 );

    @property
    def has_steam_id (self):
        return bool( self.edf & 0x10 );

    @property
    def has_stv (self):
        return bool( self.edf & 0x40 );

    @property
    def has_keywords (self):
        return bool( self.edf & 0x20 );

    @property
    def has_game_id (self):
        return bool( self.edf & 0x01 );


class GoldSrcInfo (metaclass=DataclsMeta):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#Obsolete_GoldSource_Response
    """
    address: str;
    """IP Address and port of the server."""

    server_name: str;
    """Display name of the server."""

    map_name: str;
    """The currently loaded map."""

    folder: str;
    """Name of the game directory."""

    game: str;
    """Name of the game."""

    player_count: int;
    """Number of players currently connected."""

    max_players: int;
    """Number of player slots available."""

    protocol: int;
    """Protocol version used by the server."""

    server_type: str;
    """Type of the server:
    'D': Dedicated server.
    'L': Non-dedicated server.
    'P': HLTV server."""

    platform: str;
    """Operating system of the server
    'L': Linux.
    'W': Windows."""

    password_protected: bool;
    """Server requires a password to connect."""

    is_mod: bool;
    """Server is running a Half-Life mod instead of the base game."""

    vac_enabled: bool;
    """Server has VAC enabled."""

    bot_count: int;
    """Number of bots on the server."""

    mod_website: str;
    """Optional:
    URL to the mod website."""

    mod_download: str;
    """URL to download the mod."""

    mod_version: int;
    """Version of the mod installed on the server."""

    mod_size: int;
    """Size in bytes of the mod."""

    multiplayer_only: bool = False;
    """Mod supports multiplayer only."""

    uses_custom_dll: bool = False;
    """Mod uses a custom DLL.
    0: uses the Half-Life DLL
    1: uses its own DLL"""

    ping: float;
    """Client determined values: Round-trip delay time for the request in seconds."""


def info (address: TYPE_ADDRESS, timeout: float=DEFAULT_TIMEOUT, encoding: str=DEFAULT_ENCODING, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator) -> (SourceInfo | GoldSrcInfo):
    return request( address, timeout, encoding, A2SInfoProtocol, fragment_cls=fragment_cls, mutator_cls=mutator_cls );


async def ainfo (address, timeout=DEFAULT_TIMEOUT, encoding: str=DEFAULT_ENCODING, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator) -> (SourceInfo | GoldSrcInfo):
    return await request_async( address, timeout, encoding, A2SInfoProtocol, fragment_cls=fragment_cls, mutator_cls=mutator_cls );


class A2SInfoProtocol (BaseQueryProtocol):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#A2S_INFO
    """
    @classmethod
    def validate_response_type (cls, response_type: int) -> bool:
        return response_type in (A2S_INFO_RESPONSE, A2S_INFO_RESPONSE_LEGACY);

    @classmethod
    def serialize_request (cls, challenge: int) -> bytes:
        if challenge:
            return b"\x54Source Engine Query\0" + challenge.to_bytes(4, "little");
        else:
            return b"\x54Source Engine Query\0";

    @classmethod
    def deserialize_response (cls, reader: ByteReader, response_type: int, ping: float):
        if response_type == A2S_INFO_RESPONSE:
            resp = parse_source( reader );
        elif response_type == A2S_INFO_RESPONSE_LEGACY:
            resp = parse_goldsrc( reader );
        else:
            raise Exception( str(response_type) );
        resp.ping = ping;
        return resp;


def parse_source (reader: ByteReader):
    resp = SourceInfo();
    resp.protocol = reader.read_uint8();
    resp.server_name = reader.read_cstring();
    resp.map_name = reader.read_cstring();
    resp.folder = reader.read_cstring();
    resp.game = reader.read_cstring();
    resp.app_id = reader.read_uint16();
    resp.player_count = reader.read_uint8();
    resp.max_players = reader.read_uint8();
    resp.bot_count = reader.read_uint8();
    resp.server_type = reader.read_char().lower();
    resp.platform = reader.read_char().lower();
    if resp.platform == "o": # Deprecated mac value
        resp.platform = "m";
    resp.password_protected = reader.read_bool();
    resp.vac_enabled = reader.read_bool();
    resp.version = reader.read_cstring();
    try:
        resp.edf = reader.read_uint8();
    except BufferExhaustedError:
        pass;
    if resp.has_port:
        resp.port = reader.read_uint16();
    if resp.has_steam_id:
        resp.steam_id = reader.read_uint64();
    if resp.has_stv:
        resp.stv_port = reader.read_uint16();
        resp.stv_name = reader.read_cstring();
    if resp.has_keywords:
        resp.keywords = reader.read_cstring();
    if resp.has_game_id:
        resp.game_id = reader.read_uint64();
    return resp;


def parse_goldsrc (reader: ByteReader):
    resp = GoldSrcInfo();
    resp.address = reader.read_cstring();
    resp.server_name = reader.read_cstring();
    resp.map_name = reader.read_cstring();
    resp.folder = reader.read_cstring();
    resp.game = reader.read_cstring();
    resp.player_count = reader.read_uint8();
    resp.max_players = reader.read_uint8();
    resp.protocol = reader.read_uint8();
    resp.server_type = reader.read_char().upper();
    resp.platform = reader.read_char().upper();
    resp.password_protected = reader.read_bool();
    resp.is_mod = reader.read_bool();
    # Some games don't send this section
    if resp.is_mod and len(reader.peek()) > 2:
        resp.mod_website = reader.read_cstring();
        resp.mod_download = reader.read_cstring();
        reader.read( 1 ); # Skip a NULL byte
        resp.mod_version = reader.read_uint32();
        resp.mod_size = reader.read_uint32();
        resp.multiplayer_only = reader.read_bool();
        resp.uses_custom_dll = reader.read_bool();
    resp.vac_enabled = reader.read_bool();
    resp.bot_count = reader.read_uint8();
    return resp;

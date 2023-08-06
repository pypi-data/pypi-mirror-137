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
from .common import DEFAULT_TIMEOUT, DEFAULT_ENCODING, \
    ByteReader, \
    DataclsMeta, \
    TYPE_ADDRESS, BaseResponseFragment, GoldSrcResponseFragment;
from .connection import request, request_async, BaseStreamMutator, GenericStreamMutator, BaseQueryProtocol;



A2S_PLAYER_RESPONSE = 0x44;


class PlayerInfo (metaclass=DataclsMeta):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#Response_Format_2
    """
    index: int;
    """Index of player chunk starting from 0."""

    name: str;
    """Name of the player."""

    score: int;
    """Player's score (usually "frags" or "kills")."""

    duration: float;
    """Time (in seconds) player has been connected to the server."""


def players (address: TYPE_ADDRESS, timeout: float=DEFAULT_TIMEOUT, encoding: str=DEFAULT_ENCODING, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator) -> list[PlayerInfo]:
    return request( address, timeout, encoding, A2SPlayerProtocol, fragment_cls=fragment_cls, mutator_cls=mutator_cls );


async def aplayers (address: TYPE_ADDRESS, timeout: float=DEFAULT_TIMEOUT, encoding: str=DEFAULT_ENCODING, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator) -> list[PlayerInfo]:
    return await request_async( address, timeout, encoding, A2SPlayerProtocol, fragment_cls=fragment_cls, mutator_cls=mutator_cls );


class A2SPlayerProtocol (BaseQueryProtocol):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#A2S_PLAYER
    """
    @classmethod
    def validate_response_type (cls, response_type: int) -> bool:
        return response_type == A2S_PLAYER_RESPONSE;

    @classmethod
    def serialize_request (cls, challenge: int) -> bytes:
        return b"\x55" + challenge.to_bytes( 4, "little" );

    @classmethod
    def deserialize_response (cls, reader: ByteReader, response_type: int, ping: float):
        player_count = reader.read_uint8();
        resp = [
            PlayerInfo(
                index=reader.read_uint8(),
                name=reader.read_cstring(),
                score=reader.read_int32(),
                duration=reader.read_float(),
            ) for _ in range( player_count )
        ];
        return resp;

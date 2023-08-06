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
    TYPE_ADDRESS, BaseResponseFragment, GoldSrcResponseFragment;
from .connection import request, request_async, BaseStreamMutator, GenericStreamMutator, BaseQueryProtocol;



A2S_RULES_RESPONSE = 0x45;


def rules (address: TYPE_ADDRESS, timeout: float=DEFAULT_TIMEOUT, encoding: str=DEFAULT_ENCODING, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator) -> dict:
    return request( address, timeout, encoding, A2SRulesProtocol, fragment_cls=fragment_cls, mutator_cls=mutator_cls );


async def arules (address: TYPE_ADDRESS, timeout: float=DEFAULT_TIMEOUT, encoding: str=DEFAULT_ENCODING, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator) -> dict:
    return await request_async( address, timeout, encoding, A2SRulesProtocol, fragment_cls=fragment_cls, mutator_cls=mutator_cls );


class A2SRulesProtocol (BaseQueryProtocol):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#A2S_RULES
    """
    @classmethod
    def validate_response_type (cls, response_type: int) -> bool:
        return response_type == A2S_RULES_RESPONSE;

    @classmethod
    def serialize_request (cls, challenge: int) -> bytes:
        return b"\x56" + challenge.to_bytes( 4, "little" );

    @classmethod
    def deserialize_response (cls, reader: ByteReader, response_type: int, ping: float):
        rule_count = reader.read_int16();
        # Have to use tuples to preserve evaluation order
        resp = dict(
            (
                reader.read_cstring(),
                reader.read_cstring(),
            ) for _ in range( rule_count )
        );
        return resp;

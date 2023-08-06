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
import socket;
import time;
import io;

from .common import LOGGER, HEADER_SIMPLE, HEADER_MULTI, RESPONSE_CHALLENGE_ID, \
    BrokenMessageError, \
    GoldSrcResponseFragment, BaseResponseFragment, \
    DEFAULT_RETRIES, \
    ByteReader, \
    TYPE_ADDRESS, BaseQueryStream, BaseStreamMutator, GenericStreamMutator;
from .protocol import BaseQueryProtocol;



class A2SStream (BaseQueryStream):
    def __init__ (self, address: TYPE_ADDRESS, timeout: float, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator):
        super().__init__( fragment_cls, mutator_cls );
        self.address = address;
        self._socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM );
        self._socket.settimeout( timeout );

    def __del__ (self):
        self.close();

    def __enter__ (self):
        return self;

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.close();

    def send (self, data: bytes):
        LOGGER.debug( "Sending packet: %r", data );
        packet = self.mutator_cls.pre_send( data );
        self._socket.sendto( packet, self.address );

    def recv (self):
        packet = self.mutator_cls.pre_recv( self._socket.recv(65535) );
        header = packet[:4];
        data = packet[4:];
        if header == HEADER_SIMPLE:
            LOGGER.debug( "Received single packet: %r", data );
            return data;
        elif header == HEADER_MULTI:
            fragments = [self.fragment_cls.from_bytes(data)];
            while len(fragments) < fragments[0].fragment_count:
                packet = self._socket.recv( 4096 );
                fragments.append( self.fragment_cls.from_bytes(packet[4:]) );
            fragments.sort( key=lambda f: f.fragment_id );
            reassembled = b"".join( fragment.payload for fragment in fragments );
            # Sometimes there's an additional header present
            if reassembled.startswith(b"\xFF\xFF\xFF\xFF"):
                reassembled = reassembled[4:];
            LOGGER.debug(
                "Received %s part packet with content: %r",
                len(fragments),
                reassembled,
            );
            return reassembled;
        else:
            raise BrokenMessageError( "Invalid packet header: " + repr(header) );

    def request (self, payload: bytes):
        self.send( payload );
        return self.recv();

    def close (self):
        self._socket.close();


def request (address: TYPE_ADDRESS, timeout: float, encoding: str, a2s_proto: BaseQueryProtocol, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator):
    with A2SStream(address, timeout, fragment_cls=fragment_cls, mutator_cls=mutator_cls) as conn:
        return _request_impl( conn, encoding, a2s_proto );


def _request_impl (conn: A2SStream, encoding: str, a2s_proto: BaseQueryProtocol, challenge: int=0, retries: int=0, ping: float=None):
    send_time = time.monotonic();
    resp_data = conn.request( a2s_proto.serialize_request(challenge) );
    recv_time = time.monotonic();
    # Only set ping on first packet received
    if retries == 0:
        ping = recv_time - send_time;
    reader = ByteReader(
        io.BytesIO(resp_data),
        endian="<",
        encoding=encoding,
    );
    response_type = reader.read_uint8();
    if response_type == RESPONSE_CHALLENGE_ID:
        if retries >= DEFAULT_RETRIES:
            raise BrokenMessageError( "Server keeps sending challenge responses" );
        challenge = reader.read_uint32();
        return _request_impl(
            conn,
            encoding,
            a2s_proto,
            challenge,
            retries + 1,
            ping
        );
    if not a2s_proto.validate_response_type(response_type):
        raise BrokenMessageError( "Invalid response type: " + hex(response_type) );
    return a2s_proto.deserialize_response( reader, response_type, ping );

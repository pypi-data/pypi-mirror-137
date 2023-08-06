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
import asyncio;
import time;
import io;

from .common import LOGGER, HEADER_SIMPLE, HEADER_MULTI, RESPONSE_CHALLENGE_ID, \
    BrokenMessageError, \
    GoldSrcResponseFragment, BaseResponseFragment, \
    DEFAULT_RETRIES, \
    ByteReader, \
    TYPE_ADDRESS, BaseQueryStream, BaseStreamMutator, GenericStreamMutator;
from .protocol import BaseQueryProtocol;



class A2SAsyncDatagramProtocol (asyncio.DatagramProtocol):
    def __init__ (self, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator):
        self.fragment_cls = fragment_cls;
        self.mutator_cls = mutator_cls;
        self.recv_queue = asyncio.Queue();
        self.error_event = asyncio.Event();
        self.error = None;
        self.fragment_buf = [];

    def connection_made (self, transport: asyncio.DatagramTransport):
        self.transport = transport;

    def datagram_received (self, packet: bytes, addr):
        packet = self.mutator_cls.pre_recv( packet );
        header = packet[:4];
        payload = packet[4:];
        if header == HEADER_SIMPLE:
            LOGGER.debug( "Received single packet: %r", payload );
            self.recv_queue.put_nowait( payload );
        elif header == HEADER_MULTI:
            self.fragment_buf.append( self.fragment_cls.from_bytes(payload) );
            if len(self.fragment_buf) < self.fragment_buf[0].fragment_count:
                return; # Wait for more packets to arrive
            self.fragment_buf.sort( key=lambda f: f.fragment_id );
            reassembled = b"".join( fragment.payload for fragment in self.fragment_buf );
            # Sometimes there's an additional header present
            if reassembled.startswith(b"\xFF\xFF\xFF\xFF"):
                reassembled = reassembled[4:];
            LOGGER.debug(
                "Received %s part packet with content: %r",
                len(self.fragment_buf),
                reassembled,
            );
            self.recv_queue.put_nowait( reassembled );
            self.fragment_buf = [];
        else:
            self.error = BrokenMessageError( "Invalid packet header: " + repr(header) );
            self.error_event.set();

    def error_received (self, exc: OSError):
        self.error = exc;
        self.error_event.set();

    def raise_on_error (self):
        error = self.error;
        self.error = None;
        self.error_event.clear();
        raise error;


class A2SStreamAsync (BaseQueryStream):
    def __init__ (self, transport: asyncio.DatagramTransport, protocol: A2SAsyncDatagramProtocol, timeout: float, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator):
        super().__init__( fragment_cls, mutator_cls );
        self.transport = transport;
        self.protocol = protocol;
        self.timeout = timeout;

    def __del__ (self):
        self.close();

    def __enter__ (self):
        return self;

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.close();

    @classmethod
    async def create (cls, address: TYPE_ADDRESS, timeout: float, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator):
        loop = asyncio.get_running_loop();
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: A2SAsyncDatagramProtocol(fragment_cls, mutator_cls),
            remote_addr=address
        );
        return cls( transport, protocol, timeout, fragment_cls=fragment_cls, mutator_cls=mutator_cls );

    def send (self, data: bytes):
        LOGGER.debug( "Sending packet: %r", data );
        packet = self.mutator_cls.pre_send( data );
        self.transport.sendto( packet );

    async def recv (self):
        queue_task = asyncio.create_task( self.protocol.recv_queue.get() );
        error_task = asyncio.create_task( self.protocol.error_event.wait() );
        done, pending = await asyncio.wait(
            {queue_task, error_task},
            timeout=self.timeout,
            return_when=asyncio.FIRST_COMPLETED,
        );
        for task in pending:
            task.cancel();
        if error_task in done:
           self.protocol.raise_on_error();
        if not done:
            raise asyncio.TimeoutError();
        return queue_task.result();

    async def request (self, payload: bytes):
        self.send( payload );
        return await self.recv();

    def close (self):
        self.transport.close();


async def request_async (address: TYPE_ADDRESS, timeout: float, encoding: str, a2s_proto: BaseQueryProtocol, fragment_cls: BaseResponseFragment=GoldSrcResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator):
    with await A2SStreamAsync.create(address, timeout, fragment_cls=fragment_cls, mutator_cls=mutator_cls) as conn:
        return await _request_async_impl( conn, encoding, a2s_proto );


async def _request_async_impl( conn:A2SStreamAsync, encoding: str, a2s_proto: BaseQueryProtocol, challenge: int=0, retries: int=0, ping: float=None):
    send_time = time.monotonic();
    resp_data = await conn.request( a2s_proto.serialize_request(challenge) );
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
        return await _request_async_impl(
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

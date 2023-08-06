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
from typing import Any;
import io;
import bz2

from .byteio import ByteReader;



class BaseResponseFragment ():
    def __init__ (self, message_id: int, fragment_count: int, fragment_id: int, payload: bytes=b""):
        self.message_id = message_id;
        self.fragment_count = fragment_count;
        self.fragment_id = fragment_id;
        self.payload = payload;
    @classmethod
    def from_bytes (cls, data: bytes) -> Any:
        raise NotImplemented();


class GoldSrcResponseFragment (BaseResponseFragment):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#Goldsource_Server
    """
    @classmethod
    def from_bytes (cls, data: bytes):
        reader = ByteReader(
            io.BytesIO( data ),
            endian="<",
            encoding="utf-8",
        );
        msg_id = reader.read_uint32();
        fragment_byte = reader.read_uint8();
        fragment_count = fragment_byte & 0xF;
        fragment_id = (fragment_byte >> 4) & 0xF;
        return cls(
            message_id=msg_id,
            fragment_count=fragment_count,
            fragment_id=fragment_id,
            payload = reader.read(),
        );


class SourceResponseFragment (BaseResponseFragment):
    """
    https://developer.valvesoftware.com/wiki/Server_queries#Source_Server
    """
    def __init__ (self, message_id: int, fragment_count: int, fragment_id: int, mtu: int,
                  decompressed_size: int=0, crc: int=0, payload: bytes = b""):
        super().__init__( message_id, fragment_count, fragment_id, payload );
        self.mtu = mtu;
        self.decompressed_size = decompressed_size;
        self.crc = crc;

    @property
    def is_compressed (self):
        return bool( self.message_id & (1 << 15) );

    @classmethod
    def from_bytes (cls, data: bytes):
        reader = ByteReader(
            io.BytesIO( data ),
            endian="<",
            encoding="utf-8",
        );
        frag = cls(
            message_id=reader.read_uint32(),
            fragment_count=reader.read_uint8(),
            fragment_id=reader.read_uint8(),
            mtu=reader.read_uint16(),
        );
        if frag.is_compressed:
            frag.decompressed_size = reader.read_uint32();
            frag.crc = reader.read_uint32();
            frag.payload = bz2.decompress( reader.read() );
        else:
            frag.payload = reader.read();
        return frag;

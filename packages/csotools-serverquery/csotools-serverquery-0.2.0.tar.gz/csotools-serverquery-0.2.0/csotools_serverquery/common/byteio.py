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
import struct;
import io;

from .exception import BufferExhaustedError;



class ByteReader ():
    def __init__ (self, stream: io.RawIOBase, endian: str="=", encoding: str=None):
        self.stream = stream;
        self.endian = endian;
        self.encoding = encoding;

    def read (self, size: int=-1):
        data = self.stream.read( size );
        if size > -1 and len(data) != size:
            raise BufferExhaustedError();
        return data;

    def peek (self, size: int=-1):
        cur_pos = self.stream.tell();
        data = self.stream.read( size );
        self.stream.seek( cur_pos, io.SEEK_SET );
        return data;

    def unpack (self, fmt: str):
        fmt = self.endian + fmt;
        fmt_size = struct.calcsize( fmt );
        return struct.unpack( fmt, self.read(fmt_size) );

    def unpack_one (self, fmt: str):
        values = self.unpack( fmt );
        assert len(values) == 1;
        return values[0];

    def read_int8 (self) -> int:
        return self.unpack_one( "b" );

    def read_uint8 (self) -> int:
        return self.unpack_one( "B" );

    def read_int16 (self) -> int:
        return self.unpack_one( "h" );

    def read_uint16 (self) -> int:
        return self.unpack_one( "H" );

    def read_int32 (self) -> int:
        return self.unpack_one( "l" );

    def read_uint32 (self) -> int:
        return self.unpack_one( "L" );

    def read_int64 (self) -> int:
        return self.unpack_one( "q" );

    def read_uint64 (self) -> int:
        return self.unpack_one( "Q" );

    def read_float (self) -> float:
        return self.unpack_one( "f" );

    def read_double (self) -> float:
        return self.unpack_one( "d" );

    def read_bool (self):
        return bool( self.unpack_one("b") );

    def read_char (self):
        char: bytes = self.unpack_one( "c" );
        if self.encoding is not None:
            return char.decode( self.encoding, errors="replace" );
        else:
            return char;

    def read_cstring (self, charsize=1):
        string: bytes = b"";
        while True:
            c = self.read( charsize );
            if int.from_bytes(c, "little") == 0:
                break;
            else:
                string += c;
        if self.encoding is not None:
            return string.decode( self.encoding, errors="replace" );
        else:
            return string;


class ByteWriter():
    def __init__ (self, stream: io.RawIOBase, endian: str="=", encoding: str=None):
        self.stream = stream;
        self.endian = endian;
        self.encoding = encoding;

    def write (self, *args):
        return self.stream.write( *args );

    def pack (self, fmt: str, *values):
        fmt = self.endian + fmt;
        #fmt_size = struct.calcsize( fmt );
        return self.stream.write( struct.pack(fmt, *values) );

    def write_int8 (self, val: int):
        self.pack( "b", val );

    def write_uint8 (self, val: int):
        self.pack( "B", val );

    def write_int16 (self, val: int):
        self.pack( "h", val );

    def write_uint16 (self, val: int):
        self.pack( "H", val );

    def write_int32 (self, val: int):
        self.pack( "l", val );

    def write_uint32 (self, val: int):
        self.pack( "L", val );

    def write_int64 (self, val: int):
        self.pack( "q", val );

    def write_uint64 (self, val: int):
        self.pack( "Q", val );

    def write_float (self, val: float):
        self.pack( "f", val );

    def write_double (self, val: float):
        self.pack( "d", val );

    def write_bool (self, val: bool):
        self.pack( "b", val );

    def write_char (self, val: str):
        if self.encoding is not None:
            self.pack( "c", val.encode(self.encoding) );
        else:
            self.pack( "c", val );

    def write_cstring (self, val: str):
        if self.encoding is not None:
            self.write( val.encode(self.encoding) + b"\x00" );
        else:
            self.write( val + b"\x00" );

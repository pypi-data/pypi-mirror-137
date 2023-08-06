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
from ..common import *;
from .constant import *;



class BaseStreamMutator ():
    @classmethod
    def pre_send (cls, data: bytes) -> bytes:
        raise NotImplemented();

    @classmethod
    def pre_recv (cls, packet: bytes) -> bytes:
        raise NotImplemented();


class GenericStreamMutator (BaseStreamMutator):
    @classmethod
    def pre_send (cls, data: bytes) -> bytes:
        return HEADER_SIMPLE + data;

    @classmethod
    def pre_recv (cls, packet: bytes) -> bytes:
        return packet;


class CSOStreamMutator (GenericStreamMutator):
    @classmethod
    def pre_send (cls, data: bytes) -> bytes:
        return CSO_REQUEST_HEADER + super().pre_send( data );

    @classmethod
    def pre_recv (cls, packet: bytes) -> bytes:
        packet = super().pre_recv( packet );
        if packet.startswith( CSO_RESPONSE_HEADER ):
            packet = packet[len(CSO_RESPONSE_HEADER):];
        return packet;


class BaseQueryStream ():
    def __init__ (self, fragment_cls: BaseResponseFragment, mutator_cls: BaseStreamMutator=GenericStreamMutator):
        self.fragment_cls = fragment_cls;
        self.mutator_cls = mutator_cls;

    def __del__ (self):
        self.close();

    def close (self):
        raise NotImplementedError();

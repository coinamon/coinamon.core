"""
This module provides utility functions to manipulate with binary data (:py:func:`bytes`).
"""

import binascii
import struct

from . import hashutils


_BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base58_encode(data: bytes) -> bytes:
    """
    Encode raw binary data with Bitcoin's base58 encoding.

    :param data: Raw binary data.
    :return: Base58 encoded data.
    """

    # https://bitcoin.org/en/developer-reference#address-conversion
    bigint = int.from_bytes(data, 'big')

    # Encoding as big integer division
    buffer = []
    while bigint > 0:
        bigint, remainder = divmod(bigint, 58)
        buffer.append(_BASE58_ALPHABET[remainder])

    # Preserve leading zeros
    zero_char = _BASE58_ALPHABET[0]
    for byte in data:
        if byte == 0:
            buffer.append(zero_char)
        else:
            break

    return bytes(reversed(buffer))


def base58check_encode(data: bytes) -> bytes:
    """
    Encode raw binary data with Bitcoin's Base58Check encoding.

    :param data: Raw binary data.
    :return: Base58Check encoded data.
    """
    return base58_encode(data + hashutils.hash256(data)[0:4])


def base58_decode(data: bytes) -> bytes:
    """
    Decode raw binary data in Bitcoin's base58 encoding.

    :param data: Base58 encoded data.
    :return: Raw binary data.
    :raise: :py:exc:`ValueError` if data is invalid.
    """
    if not data:
        return b""

    bigint = 0
    for char in data:
        bigint *= 58
        value = _BASE58_ALPHABET.find(char)
        if value < 0:
            raise ValueError("Character '{}' is not in Base58 alphabet.".format(char))
        elif value:
            bigint += value

    buffer = bigint.to_bytes((bigint.bit_length() + 7) // 8, 'big')

    zero_char = _BASE58_ALPHABET[0]
    padding = 0
    for char in data:
        if char == zero_char:
            padding += 1
        else:
            break

    return b'\00' * padding + buffer


def base58check_decode(data: bytes) -> bytes:
    """
    Decode raw binary data in Bitcoin's Base58Check encoding.

    :param data: Base58Check encoded data.
    :return: Raw binary data.
    :raise: :py:exc:`ValueError` if data is invalid.
    """
    data_and_checksum = base58_decode(data)
    decoded_data = data_and_checksum[:-4]
    if hashutils.hash256(decoded_data)[0:4] != data_and_checksum[-4:]:
        raise ValueError("Checksum error")
    return decoded_data


class BinReader:
    """
    Utility class to read binary data, especially integers of various size
    and Bitcoin's compact integer.
    """
    def __init__(self, buffer: bytes, offset: int = 0):
        """
        :param buffer: The source data to read.
        :param offset: The offset to start reading from.
        """
        self.buffer = buffer
        self.offset = offset
        self.size = len(buffer)

    def read_byte(self) -> int:
        """
        Read a single (unsigned) byte.

        :return: A value in range <0; 255>
        """
        value = self.buffer[self.offset]
        self.offset += 1
        return value

    def read_int8(self) -> int:
        """
        Read a 8bit signed integer.

        :return: A value in range <−128; 127>
        """
        value = struct.unpack_from("<b", self.buffer, self.offset)[0]
        self.offset += 1
        return value

    def read_uint8(self) -> int:
        """
        Read a 8bit unsigned integer.

        :return: A value in range <0; 255>
        """
        value = struct.unpack_from("<B", self.buffer, self.offset)[0]
        self.offset += 1
        return value

    def read_int16(self) -> int:
        """
        Read a 16bit signed integer.

        :return: A value in range <−32,768; 32,767>
        """
        value = struct.unpack_from("<h", self.buffer, self.offset)[0]
        self.offset += 2
        return value

    def read_uint16(self) -> int:
        """
        Read a 16bit unsigned integer.

        :return: A value in range <0; 65,535>
        """
        value = struct.unpack_from("<H", self.buffer, self.offset)[0]
        self.offset += 2
        return value

    def read_int32(self) -> int:
        """
        Read a 32bit signed integer.

        :return: A value in range < −2,147,483,648; 2,147,483,647>
        """
        value = struct.unpack_from("<i", self.buffer, self.offset)[0]
        self.offset += 4
        return value

    def read_uint32(self) -> int:
        """
        Read a 32bit unsigned integer.

        :return: A value in range <0; 4,294,967,295>
        """
        value = struct.unpack_from("<I", self.buffer, self.offset)[0]
        self.offset += 4
        return value

    def read_int64(self) -> int:
        """
        Read a 64bit signed integer.

        :return: A value in range <−9,223,372,036,854,775,808; 9,223,372,036,854,775,807>
        """
        value = struct.unpack_from("<q", self.buffer, self.offset)[0]
        self.offset += 8
        return value

    def read_uint64(self) -> int:
        """
        Read a 64bit unsigned integer.

        :return: A value in range <0; 18,446,744,073,709,551,615>
        """
        value = struct.unpack_from("<Q", self.buffer, self.offset)[0]
        self.offset += 8
        return value

    def read_compact_uint(self) -> int:
        """
        Read a Bitcoin's compact size unsigned integer.

        :return: A value in range <0; 18,446,744,073,709,551,615>
        """
        value = self.read_uint8()
        if value <= 252:
            return value
        elif value == 0xfd:
            return self.read_uint16()
        elif value == 0xfe:
            return self.read_uint32()
        elif value == 0xff:
            return self.read_uint64()

    def read_bytes(self, count: int = 1) -> bytes:
        """
        Read *count* bytes from buffer.

        :param count: The numebr of bytes to read.
        :return: Requested byte string.
        """
        value = self.buffer[self.offset:self.offset + count]
        self.offset += count
        return value

    def read_bytes_reversed(self, count: int = 1) -> bytes:
        """
        Read *count* bytes from buffer.

        :param count: The numebr of bytes to read.
        :return: Requested byte string.
        """
        value = self.buffer[self.offset + count - 1:self.offset - 1:-1]
        self.offset += count
        return value

    def read_hex(self, count: int = 1) -> bytes:
        """
        Read *count* bytes encoded as hexadecimal byte string.

        :param count: The number of bytes to read.
        :return: Requested binary data encoded as a hexadecimal byte string.
        """
        return binascii.hexlify(self.read_bytes(count))

    def read_hex_reversed(self, count: int = 1) -> bytes:
        """
        Read *count* bytes in reversed order encoded as hexadecimal byte string.

        :param count: The number of bytes to read.
        :return: Requested binary data encoded as a hexadecimal byte string.
        """
        return binascii.hexlify(self.read_bytes_reversed(count))

    def __len__(self) -> int:
        return self.size - self.offset

    def __bool__(self) -> bool:
        return bool(self.__len__())

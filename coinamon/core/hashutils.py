"""
This module provides shortcuts to commonly used hash functions (:py:func:`sha256` and :py:func:`ripemd160`)
as well as compound hash functions used in Bitcoin protocol (:py:func:`hash256` and :py:func:`hash160`).
"""

import hashlib


def sha256(data: bytes) -> bytes:
    """
    Calculate SHA 256 hash.

    :param data: The data to hash.
    :return: The resulting hash.
    """
    return hashlib.sha256(data).digest()


def ripemd160(data: bytes) -> bytes:
    """
    Calculate RIPEMD 160 hash.

    :param data: The data to hash.
    :return: The resulting hash.
    """
    return hashlib.new('ripemd160', data).digest()


def hash256(data: bytes) -> bytes:
    """
    Calculate Bitcoin 256 hash (double sha256).

    :param data: The data to hash.
    :return: The resulting hash.
    """
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def hash160(data: bytes) -> bytes:
    """
    Calculate Bitcoin 160 hash (SHA 256 and RIPEMD 160)

    :param data: The data to hash.
    :return: The resulting hash.
    """
    return ripemd160(sha256(data))

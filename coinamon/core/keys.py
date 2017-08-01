"""
This module contains classes of public and private keys.
"""

import secrets

import secp256k1


PRIVATE_KEY_BITS = 256
PRIVATE_KEY_BYTES = PRIVATE_KEY_BITS // 8
PRIVATE_KEY_MAX = int(1.158e77) - 2
PUBLIC_KEY_COMPRESSED_BYTES = 33
PUBLIC_KEY_UNCOMPRESSED_BYTES = 65

class PrivateKey:
    @classmethod
    def create(cls, compressed : bool = True) -> "PrivateKey":
        """
        Create random private key.

        :param compressed: Whether this key is to generate compressed public keys.
        """

        key_candidate = None
        while not key_candidate or key_candidate > PRIVATE_KEY_MAX:
            key_candidate = secrets.randbits(PRIVATE_KEY_BITS)
            return cls.from_raw_bytes(key_candidate.to_bytes(PRIVATE_KEY_BYTES, "big"), compressed)

    @classmethod
    def from_raw_bytes(cls, raw_bytes: bytes, compressed: bool = True) -> "PrivateKey":
        """
        Load key from raw binary data.

        :param raw_bytes: Raw binary key data,
        :param compressed: Whether this key is to generate compressed public keys.
        """
        n_bits = len(raw_bytes) * 8
        assert n_bits == PRIVATE_KEY_BITS, "Private key must be %d bits long." % PRIVATE_KEY_BITS
        number = int.from_bytes(raw_bytes, "big")
        assert 0 < number < PRIVATE_KEY_MAX, "Private key is out of range."
        key = secp256k1.PrivateKey(raw_bytes, raw=True)
        return cls(key, compressed)
    
    def __init__(self, key: secp256k1.PrivateKey, compressed: bool = True):
        """
        :param key: SECP256k1 private key.
        :param compressed: Whether this key is to generate compressed public keys.

        :var key: SECP256k1 private key.
        :vartype key: secp256k1.PrivateKey
        :var compressed: Whether this key is to generate compressed public keys.
        :vartype compressed: bool
        :var public_key: Corresponding public key.
        :vartype public_key: PublicKey
        """
        self.compressed = compressed
        self.key = key
        self.public_key = PublicKey(self.key.pubkey, compressed, self)

    def as_raw_bytes(self) -> bytes:
        """
        Export this key as raw binary data.
        """
        return self.key.private_key

    def serialize(self) -> bytes:
        """
        Serialize key as hexadecimal byte string.
        """
        return self.key.serialize()

    def __repr__(self) -> str:
        return "<%s>" % self.__class__.__name__


class PublicKey:
    @classmethod
    def from_hex_bytes(cls, serialized_bytes: bytes) -> "PublicKey":
        """
        Load key from hexadecimal byte string.

        :param serialized_bytes: The key serialized as hexadecimal byte string.
        """
        n_bytes = len(serialized_bytes)
        assert n_bytes in (PUBLIC_KEY_COMPRESSED_BYTES, PUBLIC_KEY_UNCOMPRESSED_BYTES), "Wrong key size %d." % n_bytes
        compressed = n_bytes == PUBLIC_KEY_COMPRESSED_BYTES
        key = secp256k1.PublicKey(serialized_bytes, raw=False)
        return cls(key, compressed)

    def __init__(self, key: secp256k1.PublicKey, compressed: bool = True, private_key: PrivateKey = None):
        """
        :param key: SECP256k1 public key.
        :param compressed: Whether the public key is in compressed format.
        :param private_key: Corresponding private key if available.

        :var key: SECP256k1 public key.
        :vartype key: secp256k1.PublicKey
        :var compressed: Whether this key is compressed.
        :vartype compressed: bool
        :var private_key: Corresponding private key.
        :vartype private_key: PrivateKey
        """
        self.compressed = compressed
        self.key = key
        self.private_key = private_key

    def serialize(self) -> bytes:
        """
        Serialize key as hexadecimal byte string.
        """
        return self.key.serialize(self.compressed)

    def __repr__(self) -> str:
        return "<%s>" % self.__class__.__name__

if __name__ == "__main__":
    privkey = PrivateKey.create()
    print(privkey, privkey.key)
    pubkey = privkey.public_key
    ser = pubkey.serialize()
    print(len(ser), ser)

    ser = PrivateKey.create(True).public_key.serialize()
    print(len(ser), ser)
    ser = PrivateKey.create(False).public_key.serialize()
    print(len(ser), ser)


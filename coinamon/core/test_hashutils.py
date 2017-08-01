from . import hashutils


DATA = b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed doeiusmod tempor incididunt ut labore."


def test_sha256():
    assert hashutils.sha256(DATA).hex() == "8ea0797d87adb082280adb9beaf4ce1eee5c32602616a7f2f09781d74074bdf0"


def test_ripemn160():
    assert hashutils.ripemd160(DATA).hex() == "adcc4acaf5cd1df442ba39dd358252ecf74873bc"


def test_hash256():
    assert hashutils.hash256(DATA).hex() == "7d3e7c52a90baf4db264d8ef710e30fd541c03408c66c44e995c526e55b54481"


def test_hash160():
    assert hashutils.hash160(DATA).hex() == "dd93da718a7b4d60a2919f10cbcd326f612a5a88"

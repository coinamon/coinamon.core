import binascii

from . import hashutils
from . import binutils


DATA_BIN = b"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed doeiusmod tempor incididunt ut labore."
DATA_HEX = (
    b"4c6f72656d20697073756d20646f6c6f722073697420616d65742c20636f"
    b"6e7365637465747572206164697069736963696e6720656c69742c207365"
    b"6420646f656975736d6f642074656d706f7220696e6369646964756e7420"
    b"7574206c61626f72652e")


BASE58_DATA = (
    ("800C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D507A5B8D",
     b"5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"),
    ("801EA211D9DF964EA5FD1F14436293529E58E59A10872DC38E6504E4903B9C04568D2CDCC2",
     b"5J3n4affALXzDfeBDaho4kgDwPxqeyX86ZRL7UfaVNgU412vheh")
)


def test_base58_encode():
    for data, result in BASE58_DATA:
        if isinstance(data, str):
            data = bytes.fromhex(data)
        assert binutils.base58_encode(data) == result


def test_base58_decode():
    for result, data in BASE58_DATA:
        if isinstance(result, str):
            result = bytes.fromhex(result)
        assert binutils.base58_decode(data) == result


BASE58_CHECK_DATA = (
    (b"\x00" + hashutils.hash160(bytes.fromhex(
        "0202a406624211f2abbdc68da3df929f938c3399dd79fac1b51b0e4ad1d26a47aa")),
     b"1PRTTaJesdNovgne6Ehcdu1fpEdX7913CK"),
    ("80" + "0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D",
     b"5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"),
    ("801e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd",
     b"5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn"),
    ("801e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd01",
     b"KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ"),
)


def test_base58check_encode():
    for data, result in BASE58_CHECK_DATA:
        if isinstance(data, str):
            data = bytes.fromhex(data)
        assert binutils.base58check_encode(data) == result


def test_base58check_decode():
    for result, data in BASE58_CHECK_DATA:
        if isinstance(result, str):
            result = bytes.fromhex(result)
        assert binutils.base58check_decode(data) == result


RAW_TX = b"""\
0100000008ce5687c19912aee42bf9cc071c6a3d4e11e45f577a175a0ecbdf31d82c76cdf8010000006b\
483045022057497862187df3ee335d2f40b09093c06f0928049a370b34a134500dea16e22f022100bd32\
2fc371cca92d65339d052ef1eceff50237df9ab40061ce0a2e6daa6ca6ce0121022ce74ba31c4eb3941d\
309df86b247589f62ad883992b1cb635515006f458272bffffffff782f8952d0ef4c7280819f71e73d50\
07e3f2e6e288b3d7899c81ba13e360ee00000000006a473044022017fdcfe5dd8daf984d03eff6e3e5d1\
beee8aff48d5efd68b40e427758c95a434022034d9d0ab44f633b694211224abefe0280ea7ea0048be4b\
5799a1c8242c1e0ca401210218ea5c4b4c06e1a0cb84b50f4e95705481b086ae1379ad4035eb0f4536cd\
f1adffffffff0b4335f4f1b150d8941e99c84ccb2f9d6811a2ae44496ce5cd264cce12a09b7306000000\
6a47304402207f7a2ab27003962228e5a5b83358f45d60743a9ff8f90b006a1c9254e15bdfe502201433\
23617d17107e1e7c39ff2829d57b2526b798d9372fa7d98800aa31818f590121022ce74ba31c4eb3941d\
309df86b247589f62ad883992b1cb635515006f458272bffffffff8171bb15d388969b1f21357b4ab405\
b15c13cd4635910c5af043395ea986d0cc060000006b483045022065efc24b4c6368dc1bdca68befb5b8\
fb10f962f8b995c6362574e204cdedfa99022100a567011d3fb54cb3a8de57374993c554c6335af0b918\
21cc677a4c133859fc760121022ce74ba31c4eb3941d309df86b247589f62ad883992b1cb635515006f4\
58272bffffffff2803d50d0289b02cfaa6afa96621d1c709e24724dadba0a4e4e7b840a0b8f5d3050000\
006a47304402202b2156ddad8bda2b6d291d19d993465003d86011a7e34024421db9af34d13e6d022053\
fb4749519b17ec29422782b88723fdb51ace6c455a6d1f6bde7efa699986090121022ce74ba31c4eb394\
1d309df86b247589f62ad883992b1cb635515006f458272bffffffff8378f6a73331be80211d56ee0599\
9a4dfb365b86084f7d669874c12ede6903aa050000006b483045022059a039ed6104f99ea028a65b1a2b\
d450acd802019b1af4b28cfbf162cd02c368022100e358cbd823001b0c9bbe7dbf9100b2d7b2c251e7f7\
1316bb4ff3024b394173070121022ce74ba31c4eb3941d309df86b247589f62ad883992b1cb635515006\
f458272bffffffff634d486b3def7bb2630987f9645116d944699f171165c6ac604eb7833c8e374a0100\
00006b4830450221009fc7571375c071d92c3e47e4dcd6c1411be302388ced2a781c21ab1cbc9ffa8502\
205f8b6c4012703097252cea34438ff5a7f5a9b35fe78c7c64a34104969f9bd71c012103c2804d8880ac\
4b3a65c1c5d4dbc592b60015027f4f5ed65a1d0c6d266b4e0c46ffffffffcff5317959c58612df6a4aa2\
1ab96a52aaa2cef2871dd0b4132b5e2991330016000000006b483045022100ff4064d3d185661deb9e57\
e6f492a811c09d7826545dd3956efbc7363c8f2f8f02204f8c5faa471d90227c5ad72b0b91839598a9e6\
83b176635af6102336bc60b96701210218ea5c4b4c06e1a0cb84b50f4e95705481b086ae1379ad4035eb\
0f4536cdf1adffffffff017c85a800000000001976a914e8a7c9b03caabeafa5a99d98663c7bd7d587ad\
9e88ac00000000\
"""


def test_bin_reader():
    reader = binutils.BinReader(binascii.unhexlify(RAW_TX))
    assert reader.read_uint32() == 1,  "version"
    assert reader.read_compact_uint() == 8, "n_tx_in"

    assert reader.read_hex_reversed(32) == b"f8cd762cd831dfcb0e5a177a575fe4114e3d6a1c07ccf92be4ae1299c18756ce", \
        "previous_hash"
    assert reader.read_uint32() == 1, "previous_n"
    assert reader.read_compact_uint() == 107, "len_script_sig"
    assert reader.read_hex(107) == (
        b"483045022057497862187df3ee335d2f40b09093c06f0928049a370b34a134500dea16e22f022100bd322fc371cca92d65339d052ef"
        b"1eceff50237df9ab40061ce0a2e6daa6ca6ce0121022ce74ba31c4eb3941d309df86b247589f62ad883992b1cb635515006f458272b"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_hex_reversed(32) == b"00ee60e313ba819c89d7b388e2e6f2e307503de7719f8180724cefd052892f78", \
        "previous_hash"
    assert reader.read_uint32() == 0, "previous_n"
    assert reader.read_compact_uint() == 106, "len_script_sig"
    assert reader.read_hex(106) == (
        b"473044022017fdcfe5dd8daf984d03eff6e3e5d1beee8aff48d5efd68b40e427758c95a434022034d9d0ab44f633b694211224abefe"
        b"0280ea7ea0048be4b5799a1c8242c1e0ca401210218ea5c4b4c06e1a0cb84b50f4e95705481b086ae1379ad4035eb0f4536cdf1ad"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_hex_reversed(32) == b"739ba012ce4c26cde56c4944aea211689d2fcb4cc8991e94d850b1f1f435430b", \
        "previous_hash"
    assert reader.read_uint32() == 6, "previous_n"
    assert reader.read_compact_uint() == 106, "len_script_sig"
    assert reader.read_hex(106) == (
        b"47304402207f7a2ab27003962228e5a5b83358f45d60743a9ff8f90b006a1c9254e15bdfe50220143323617d17107e1e7c39ff2829d"
        b"57b2526b798d9372fa7d98800aa31818f590121022ce74ba31c4eb3941d309df86b247589f62ad883992b1cb635515006f458272b"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_hex_reversed(32) == b"ccd086a95e3943f05a0c913546cd135cb105b44a7b35211f9b9688d315bb7181", \
        "previous_hash"
    assert reader.read_uint32() == 6, "previous_n"
    assert reader.read_compact_uint() == 107, "len_script_sig"
    assert reader.read_hex(107) == (
        b"483045022065efc24b4c6368dc1bdca68befb5b8fb10f962f8b995c6362574e204cdedfa99022100a567011d3fb54cb3a8de5737499"
        b"3c554c6335af0b91821cc677a4c133859fc760121022ce74ba31c4eb3941d309df86b247589f62ad883992b1cb635515006f458272b"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_hex_reversed(32) == b"d3f5b8a040b8e7e4a4a0dbda2447e209c7d12166a9afa6fa2cb089020dd50328", \
        "previous_hash"
    assert reader.read_uint32() == 5, "previous_n"
    assert reader.read_compact_uint() == 106, "len_script_sig"
    assert reader.read_hex(106) == (
        b"47304402202b2156ddad8bda2b6d291d19d993465003d86011a7e34024421db9af34d13e6d022053fb4749519b17ec29422782b8872"
        b"3fdb51ace6c455a6d1f6bde7efa699986090121022ce74ba31c4eb3941d309df86b247589f62ad883992b1cb635515006f458272b"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_hex_reversed(32) == b"aa0369de2ec17498667d4f08865b36fb4d9a9905ee561d2180be3133a7f67883", \
        "previous_hash"
    assert reader.read_uint32() == 5, "previous_n"
    assert reader.read_compact_uint() == 107, "len_script_sig"
    assert reader.read_hex(107) == (
        b"483045022059a039ed6104f99ea028a65b1a2bd450acd802019b1af4b28cfbf162cd02c368022100e358cbd823001b0c9bbe7dbf910"
        b"0b2d7b2c251e7f71316bb4ff3024b394173070121022ce74ba31c4eb3941d309df86b247589f62ad883992b1cb635515006f458272b"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_hex_reversed(32) == b"4a378e3c83b74e60acc66511179f6944d9165164f9870963b27bef3d6b484d63", \
        "previous_hash"
    assert reader.read_uint32() == 1, "previous_n"
    assert reader.read_compact_uint() == 107, "len_script_sig"
    assert reader.read_hex(107) == (
        b"4830450221009fc7571375c071d92c3e47e4dcd6c1411be302388ced2a781c21ab1cbc9ffa8502205f8b6c4012703097252cea34438"
        b"ff5a7f5a9b35fe78c7c64a34104969f9bd71c012103c2804d8880ac4b3a65c1c5d4dbc592b60015027f4f5ed65a1d0c6d266b4e0c46"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_hex_reversed(32) == b"16003391295e2b13b4d01d87f2cea2aa526ab91aa24a6adf1286c5597931f5cf", \
        "previous_hash"
    assert reader.read_uint32() == 0, "previous_n"
    assert reader.read_compact_uint() == 107, "len_script_sig"
    assert reader.read_hex(107) == (
        b"483045022100ff4064d3d185661deb9e57e6f492a811c09d7826545dd3956efbc7363c8f2f8f02204f8c5faa471d90227c5ad72b0b9"
        b"1839598a9e683b176635af6102336bc60b96701210218ea5c4b4c06e1a0cb84b50f4e95705481b086ae1379ad4035eb0f4536cdf1ad"
    ), "script_sig"
    assert reader.read_uint32() == 4294967295, "sequence"

    assert reader.read_compact_uint() == 1, "n_tx_out"
    assert reader.read_int64() == 11044220, "value"
    assert reader.read_compact_uint() == 25, "size pk_script"
    assert reader.read_hex(25) == b"76a914e8a7c9b03caabeafa5a99d98663c7bd7d587ad9e88ac", "pk_script"

    assert reader.read_uint32() == 0, "lock time"
    assert not reader, "reader empty"

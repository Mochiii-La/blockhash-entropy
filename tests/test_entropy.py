import pytest
from blockhash_entropy.entropy import entropy_from_block, tagged_hash

def test_genesis_block_known_vector():
    block_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"

    result = entropy_from_block(block_hash, 100)

    assert result == 66

def test_entropy_is_the_same():
    block_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    result1 = entropy_from_block(block_hash, 100)
    result2 = entropy_from_block(block_hash, 100)

    assert result1 == result2

def test_modulus_above_limit_is_rejected():
    block_hash = "00" * 32

    with pytest.raises(ValueError):
        entropy_from_block(block_hash, 2**256 + 1)

def test_entropy_is_inside_range():
    block_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    result = entropy_from_block(block_hash, 100)

    assert 0 <= result < 100

def test_different_tags_give_different_results():
    block_hash = "00" * 32

    result1 = tagged_hash("test a", bytes.fromhex(block_hash))
    result2 = tagged_hash("test b", bytes.fromhex(block_hash))

    assert result1 != result2

def test_modulus_below_one_is_rejected():
    block_hash = "00" * 32

    with pytest.raises(ValueError):
        entropy_from_block(block_hash, 0)

    with pytest.raises(ValueError):
        entropy_from_block(block_hash, -1)


def test_wrong_length_hash_is_rejected():
    with pytest.raises(ValueError):
        entropy_from_block("ab", 100)    

def test_entropy_retries_when_number_is_too_large(monkeypatch):
    calls = []

    def fake_tagged_hash(tag, data):
        calls.append(data)

        if len(calls) == 1:
            return (2**256 - 1).to_bytes(32, byteorder="big")

        return (0).to_bytes(32, byteorder="big")

    monkeypatch.setattr(
        "blockhash_entropy.entropy.tagged_hash",
        fake_tagged_hash,
    )

    result = entropy_from_block("00" * 32, 100)

    assert result == 0
    assert len(calls) == 2

def test_invalid_hex_is_rejected():
    with pytest.raises(ValueError):
        entropy_from_block("zz" * 32, 100)

def test_invalid_modulus_type_is_rejected():
    block_hash = "00" * 32

    with pytest.raises(ValueError):
        entropy_from_block(block_hash, True)

    with pytest.raises(ValueError):
        entropy_from_block(block_hash, False)

    with pytest.raises(ValueError):
        entropy_from_block(block_hash, 10.5)

    with pytest.raises(ValueError):
        entropy_from_block(block_hash, "10")
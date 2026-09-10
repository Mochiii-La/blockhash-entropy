import pytest
from blockhash_entropy.entropy import entropy_from_block

def test_entropy_is_the_same():
    block_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    result1 = entropy_from_block(block_hash, 100)
    result2 = entropy_from_block(block_hash, 100)

    assert result1 == result2


def test_entropy_is_inside_range():
    block_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    result = entropy_from_block(block_hash, 100)

    assert 0 <= result < 100

def test_different_tags_give_different_results():
    block_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    result1 = entropy_from_block(block_hash, 100, "test a")
    result2 = entropy_from_block(block_hash, 100, "test b")

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

import hashlib


def tagged_hash(tag, data):
    tag_hash = hashlib.sha256(tag.encode()).digest()

    return hashlib.sha256(
        tag_hash + tag_hash + data
    ).digest()


def entropy_from_block(block_hash, modulus, tag="blockhash-entropy"):
    if modulus < 1:
        raise ValueError("modulus must be >= 1")

    block_hash_bytes = bytes.fromhex(block_hash)

    if len(block_hash_bytes) != 32:
        raise ValueError("block_hash must be 32 bytes (64 hex chars)")

    result = tagged_hash(tag, block_hash_bytes)

    number = int.from_bytes(result, byteorder="big")

    return number % modulus
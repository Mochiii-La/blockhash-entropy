import hashlib


def entropy_from_block(block_hash, modulus, tag="blockhash-entropy"):
    if modulus < 1:
        raise ValueError("modulus must be >= 1")

    block_hash_bytes = bytes.fromhex(block_hash)

    if len(block_hash_bytes) != 32:
        raise ValueError("block_hash must be 32 bytes (64 hex chars)")

    tag_hash = hashlib.sha256(tag.encode()).digest()

    data = tag_hash + tag_hash + block_hash_bytes

    result = hashlib.sha256(data).digest()

    number = int.from_bytes(result, byteorder="big")

    return number % modulus
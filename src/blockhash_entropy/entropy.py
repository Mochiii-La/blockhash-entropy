import hashlib

def entropy_from_block(block_hash, modulus, tag ="blockhash-entropy"):
    block_hash_bytes = bytes.fromhex(block_hash)

    tag_hash = hashlib.sha256(tag.encode()).digest()

    data = tag_hash + tag_hash + block_hash_bytes

    result = hashlib.sha256(data).digest()

    number = int.from_bytes(result, byteorder="big")

    return number % modulus
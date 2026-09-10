import hashlib

def entropy_from_block(block_hash, modulus):
    block_hash_bytes = bytes.fromhex(block_hash)
    
    result = hashlib.sha256(block_hash_bytes).digest()

    number = int.from_bytes(result, byteorder="big")

    return number % modulus
import urllib.error
import urllib.request


def get_block_hash(height):
    if not isinstance(height, int) or height < 0:
        raise ValueError("height must be a non-negative integer")

    url = f"https://mempool.space/api/block-height/{height}"

    try:
        with urllib.request.urlopen(url) as response:
            block_hash = response.read().decode()

        if len(block_hash) != 64:
            raise RuntimeError("Bitcoin API returned an invalid block hash")

        try:
            bytes.fromhex(block_hash)
        except ValueError:
            raise RuntimeError("Bitcoin API returned an invalid block hash")

        return block_hash

    except urllib.error.HTTPError as error:
        raise RuntimeError(
            f"Bitcoin API returned HTTP {error.code}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Could not connect to Bitcoin API"
        ) from error
import urllib.error

import pytest

from blockhash_entropy.bitcoin import get_block_hash


def test_get_block_hash():
    result = get_block_hash(0)

    assert len(result) == 64

def test_invalid_height_is_rejected():
    with pytest.raises(ValueError):
        get_block_hash(-1)

    with pytest.raises(ValueError):
        get_block_hash("100")

def test_api_http_error(monkeypatch):
    def fake_urlopen(url):
        raise urllib.error.HTTPError(
            url,
            404,
            "Not Found",
            None,
            None,
        )

    monkeypatch.setattr(
        "blockhash_entropy.bitcoin.urllib.request.urlopen",
        fake_urlopen,
    )

    with pytest.raises(RuntimeError):
        get_block_hash(999999999)


def test_api_connection_error(monkeypatch):
    def fake_urlopen(url):
        raise urllib.error.URLError("connection failed")

    monkeypatch.setattr(
        "blockhash_entropy.bitcoin.urllib.request.urlopen",
        fake_urlopen,
    )

    with pytest.raises(RuntimeError):
        get_block_hash(0)


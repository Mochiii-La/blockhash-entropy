# blockhash-entropy

A small Python project that uses Bitcoin block hashes to generate deterministic values that anyone can verify.

The idea is to use a future Bitcoin block as a public input for generating entropy.

I'm building this as a study project to learn more about Python, Bitcoin, hashing, and publicly verifiable randomness. Feel free to audit or to leave feedback.

## Status

Work in progress.

## How it works

The current implementation takes a Bitcoin block hash and uses it as input to a tagged SHA-256 hash.

The result is converted to an integer and reduced to the requested range using rejection sampling, avoiding modulo bias.

The current process is:

```text
block hash
    ↓
block hash + counter
    ↓
tagged SHA-256
    ↓
256-bit integer
    ↓
rejection sampling
    ↓
entropy value
```

The counter starts at `0` and is encoded as 4 bytes in big-endian order. If the generated integer is outside the accepted range, the counter is incremented and the process is repeated.

Given the same block hash, modulus, and tag, the current implementation will always produce the same value.

## Bitcoin

The project also includes a small Bitcoin API module for retrieving block hashes from the mempool.space API.

This is currently a convenience for obtaining block data. It is not intended to replace verification against your own Bitcoin node.

## Tests

The project uses `pytest`.

Run the test suite with:

```bash
pytest
```

## Project structure

```text
src/
└── blockhash_entropy/
    ├── entropy.py
    └── bitcoin.py

tests/
├── test_entropy.py
└── test_bitcoin.py
```

## About

This is a learning project and is still being developed.

The goal is to keep the implementation small, understandable, and easy to audit.

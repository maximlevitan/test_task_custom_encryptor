# Custom Text Encryption / Decryption

Python project for encoding and decoding text using a custom encryption system with a set of rules.

## Features

- Character substitution (vowels → ASCII, consonants → next letter)
- Substring rearrangement (for words > 5 letters)
- Index-based encoding
- Special symbol insertion (`#`)
- Number encoding (multiply by 3, reverse)
- Internal token structure with macros `{{NNN}}` for letters
- Fully reversible encryption/decryption
- Console application with verbose logging
- Unit tests for all rules and engine

## Requirements

- Python 3.11+  

No external libraries required.

## Installation

Prepare environment:
```bash
export PYTHONPATH="$PWD"
```

## Usage

Encrypt text:
```bash
python cli/cli.py encrypt "Hello World! 123" --verbose
```

Decrypt text:
```bash
python cli/cli.py decrypt "I10#2op#115# X11#2up#i! 396" --verbose
```

## Testing

Run all tests with:
```bash
pytest tests/
```

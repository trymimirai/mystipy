# mystipy

This is an extremely simple command-line utility for obfuscating and deobfuscating data.

## Features

- Data is automatically compressed using gzip.
- Customizable encryption key (XOR) and salt size.
- Prompt mode for interactive input.
- Hexadecimal encoding is used on the output by default, but a `--binary` override is available.

## Installation

The program is a single file, so you can just download/run it manually: `python mystipy.py`

For the sake of convenience (and to be added to your `$PATH`), it is also available on PyPI.

```bash
pip install --upgrade mystipy
```

## Usage

### Basic Commands

- Obfuscate a file:

  ```bash
  mystipy input_file output_file
  ```

- Deobfuscate a file:
  ```bash
  mystipy input_file output_file --reverse
  ```

### Options

- `-p, --prompt`: Prompt mode. If provided, you will be prompted for any arguments you don't explicitly set.
- `-r, --reverse`: Deobfuscate the input file.
- `-k, --key`: XOR key for encryption/deencryption. Must be a valid byte string. (Default: "mystipy")
- `-s, --salt`: Number of bytes to use in salt. (Default: 16)
- `--binary`: Disable exadecimal encoding/decoding. The data will be (or is) compressed binary data.

### Examples

- Obfuscate a file with a custom key and default settings:

  ```bash
  mystipy myfile.txt obfuscated.myst -k "hunter2"
  ```

- Deobfuscate a binary encoded file:

  ```bash
  mystipy obfuscated.myst deobfuscated.txt -r --binary
  ```

- Use prompt mode for interactive input:

  ```bash
  mystipy -p
  ```

- Use it in your own program:

  ```python
  import mystipy

  # Define your key and data
  key = "hunter2".encode()
  data = b"I would tell you a joke about UDP, but I'm not sure if you'd get it."

  # Obfuscate the data
  obfuscated_data = mystipy.obfuscate(data, key)
  print(f"Obfuscated data: {obfuscated_data}")

  # Deobfuscate the data
  deobfuscated_data = mystipy.deobfuscate(obfuscated_data, key)
  print(f"Deobfuscated data: {deobfuscated_data.decode()}")
  ```

### Function Aliases

The script includes function aliases to remove ambiguity if you're using it in your own code:

- `mystipy` for `obfuscate`
- `demystipy` for `deobfuscate`

```python
import mystipy
print(mystipy.mystipy == mystipy.obfuscate)       # True
print(mystipy.demystipy == mystipy.deobfuscate)   # True
```

So if you'd prefer to use the aliases, you'd import the obfuscation/deobfuscation functions like this:

```python
from mystipy import mystipy, demystipy
```

import os
import argparse
import base64
import gzip
from io import BytesIO

default_key = "mystipy"
default_salt_sz = 16

def xor(data, key):
    return bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))

def obfuscate(input_data, key, salt_sz = default_salt_sz, hex = True):
    salt = os.urandom(salt_sz)
    input_data = salt + input_data
    encoded_content = base64.b64encode(input_data)
    xored_content = xor(encoded_content, key)
    reversed_content = xored_content[::-1]
    buffer = BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb') as gzipped_file:
        gzipped_file.write(reversed_content)
    gzipped_data = buffer.getvalue()
    if hex:
        return gzipped_data.hex().encode()
    return gzipped_data

def deobfuscate(input_data, key, salt_sz = default_salt_sz, hex = True):
    if hex:
        input_data = bytes.fromhex(input_data.decode())
    buffer = BytesIO(input_data)
    with gzip.GzipFile(fileobj=buffer, mode='rb') as gzipped_file:
        reversed_content = gzipped_file.read()
    xored_content = reversed_content[::-1]
    encoded_content = xor(xored_content, key)
    decoded_data = base64.b64decode(encoded_content)
    return decoded_data[salt_sz:]

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

# function aliases
mystipy = obfuscate
demystipy = deobfuscate

def main():
    parser = argparse.ArgumentParser(description = "Obfuscate or deobfuscate the contents of the file in a very simple way.")
    parser.add_argument("input", type = str, nargs = "?", help = "Input file path.")
    parser.add_argument("output", type = str, nargs = "?", help = "Output file path.")
    parser.add_argument("-p", "--prompt", action = "store_true", help = "Prompt mode. If provided, you will be prompted for the arguments you don't explicitly set.")
    parser.add_argument("-r", "--reverse", action = "store_true", help = "If provided, the protection will be reversed. (Deobfuscate)")
    parser.add_argument("-k", "--key", type = str, default = default_key, help = "XOR key for encryption/decryption. Must be a valid byte string.")
    parser.add_argument("-s", "--salt", type = int, default = default_salt_sz, help = "Number of bytes to use in salt. (Default: 16)")
    parser.add_argument("--binary", action = "store_true", help = "Disable hexadecimal encoding/decoding, meaning the data will be (or is) compressed binary data.")

    args = parser.parse_args()

    input_path, output_path = args.input, args.output
    reverse, binary, key, = args.reverse, args.binary, args.key

    if input_path and not output_path and not args.prompt:
        # only specified the input file, not in prompt mode
        if reverse:
            # they're deobfuscating it, so ask for output path
            output_path = input("Output file path: ")
        else:
            # they're obfuscating it, just add an extension to the file
            output_path = input_path + (".myst.bin" if binary else ".myst")
    elif not input_path and not output_path:
        # they didn't specify either input/output path, so prompt for both
        input_path = input("Input file path: ")
        output_path = input("Output file path: ")

    if args.prompt:
        # prompt mode - prompt for any values they didn't explicitly set
        input_path = input_path if input_path else input("Input file path: ")
        output_path = output_path if output_path else input("Output file path: ")
        if not reverse:
            _reverse = input("Are you reversing the obfuscation? [y/n, default = n]: ").lower()
            reverse = len(_reverse) > 0 and _reverse[:1].lower() == "y"
        if not binary:
            _binary = input("Should the output be hex encoded? [y/n, default = y]: ").lower()
            binary = len(_binary) > 0 and _binary[:1].lower() == "n"
        if key == default_key:
            _key = input("Enter a custom encryption key, or leave blank to use default: ")
            key = _key if len(_key) else key
    
    key = key.encode()
    input_data = read_file(input_path)

    verb = ("de" if reverse else "") + "obfuscate"
    try:
        if reverse:
            output_data = deobfuscate(input_data, key, args.salt, not binary)
        else:
            output_data = obfuscate(input_data, key, args.salt, not binary)
        write_file(output_path, output_data)
        print(f"File has been {verb}d.")
    except Exception as ex:
        print(f"Failed to {verb} data.\n{ex}")

if __name__ == "__main__":
    main()

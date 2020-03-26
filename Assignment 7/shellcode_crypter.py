# Filename: shellcode_crypter.py
# Author: Upayan a.k.a. slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: This is a Python3 script to encrypt a shellcode using a target hostname
# which alongwith the shellcode hex string is fed into the program and it spits out
# an encrypted shellcode encrypted for the target environment.
# Usage: python3 shellcode_crypter.py
# Note: PyNaCl library has been used for encryption. Also note that the 
# hostname is used as a passphrase to encrypt the shellcode.
# Testing: python3 shellcode_decrypter_loader.py


import socket
import nacl.secret
import nacl.utils
import nacl.pwhash
import base64


salt = b"\xb5\xbe\x95\x7fL\x84%\xd70\xbb\xe7\x19]\xf8\x9cT" # Generate a random 16 bytes salt


def main():
    # Display author
    print("Author: Upayan a.k.a slaeryan\n")
    # Display purpose
    print("Purpose: This is a Python3 script to encrypt a shellcode using a target hostname which alongwith the shellcode is fed into the program and it spits out an encrypted shellcode encrypted for the target environment.\n")
    # Obtain the passphrase
    hostname = input("[+] Enter the target hostname: ")
    print("\n")
    passphrase = hostname.encode("utf-8")
    # Key Derivation Function
    kdf = nacl.pwhash.argon2i.kdf
    # Generate the key
    key = kdf(nacl.secret.SecretBox.KEY_SIZE, passphrase, salt)
    # Input the plaintext from the user
    plaintext = input("[+] Enter the Original Shellcode hex string: ")
    # Create a SecretBox for encryption
    box = nacl.secret.SecretBox(key)
    # Encode the plaintext for encryption
    plaintext_byte = plaintext.encode("utf-8")
    # Encrypt the plaintext message
    ciphertext_byte = box.encrypt(plaintext_byte)
    # Cipher text will be 40 bytes longer than plaintext - MAC + Nonce
    assert len(ciphertext_byte) == len(plaintext_byte) + box.NONCE_SIZE + box.MACBYTES
    # Decode the cipher text for display
    ciphertext = base64.b64encode(ciphertext_byte).decode("utf-8")
    # Display the cipher text
    print("\n")
    print("[+] Encrypted Shellcode: ", ciphertext)
    print("\n")


main()
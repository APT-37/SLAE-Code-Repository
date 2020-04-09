# Name: encoder_proto.py
# Author: Upayan a.k.a slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: The script takes a shellcode hex string as input from user and
# converts it into a ROT-13 encoded shellcode byte string and prints 
# it to stdout in a format suitable for the decoder NASM stub.
# Testing: 31c050682f2f7368682f62696e89e35089e25389e1b00bcd80 (execve /bin/sh)
# Run with:
# python3 encoder_proto.py
# Note: The original shellcode cannot contain null-bytes(0x00)


def main():
	shellcode_hex = input("Enter the shellcode hex string: ")
	counter = 1
	byte = ''
	encoded_shellcode = ''
	for i in shellcode_hex:
		if (counter % 2 == 0):
			byte = byte + i
			byte = int(byte, 16)
			byte = hex(byte+13)
			if(len(byte)==3):
				byte = byte[:2] + '0' + byte[2:]
			byte = byte + ","
			encoded_shellcode = encoded_shellcode + byte
			byte = ''
		else:
			byte = byte + i
		counter += 1
	encoded_shellcode = encoded_shellcode + "0x0d"
	print("\n")
	print("The ROT-13 encoded shellcode byte string is:", encoded_shellcode)


main()
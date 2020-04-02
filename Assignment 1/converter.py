# Name: converter.py
# Author: Upayan a.k.a slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: The program takes an ELF executable name as input from user and
# converts it into a shellcode hex string & byte string and prints it to 
# stdout alongwith the shellcode length.
# Testing: objdump -d ./demo | grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-7 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^//'|sed 's/$//g'
# Run with:
# python3 converter.py


import os
import subprocess


def main():
	elf_name = input("Enter the name of the ELF binary: ")
	base_command = "objdump -d ./"
	command = base_command + elf_name + " " + "| grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-7 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^//'|sed 's/$//g'"
	result = subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
	shellcode_byte = result.stdout.read().decode()
	shellcode_hex = ''
	for character in shellcode_byte:
		if (ord(character) != 92) and (character != "x") and (character != ' '):
			shellcode_hex = shellcode_hex + character
	shellcode_hex = shellcode_hex.strip()
	print("[+] The shellcode length is: " + str((int)(len(shellcode_hex)/2)))
	print("\n")
	print("[+] The shellcode in hex string is:", shellcode_hex)
	print("\n")
	shellcode_byte_string = ''
	counter = 1
	byte = ''
	for i in shellcode_hex:
		if (counter % 2 == 0):
			byte = "\\x" + byte + i
			shellcode_byte_string = shellcode_byte_string + byte
			byte = ''
		else:
			byte = byte + i
		counter += 1
	print("[+] The shellcode in byte string is:", shellcode_byte_string)
	print("\n")


main()
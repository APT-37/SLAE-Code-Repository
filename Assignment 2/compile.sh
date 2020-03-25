#!/bin/bash
# Name: compile.sh
# Author: Upayan a.k.a slaeryan
# SLAE: 1525
# Contact: upayansaha@icloud.com
# Purpose: The program takes a nasm source file as console input from user and 
# compiles it with nasm and links the object file spit out by nasm with ld to 
# finally spit out the ELF executable.
# Run with:
# ./compile.sh <nasmsourcefile>
# To use libc change ld to gcc and in nasm source file change entrypoint to main

echo '[+] Assembling with nasm ... '
nasm -f elf32 -o $1.o $1.nasm

echo '[+] Linking with ld ...'
ld -s -o $1 $1.o

echo '[+] Done!'




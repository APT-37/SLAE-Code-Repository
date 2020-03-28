; Filename: mkdir_polymorphic.nasm
; Author: Upayan a.k.a. slaeryan
; SLAE: 1525
; Contact: upayansaha@icloud.com
; Purpose: This is a x86 Linux null-free polymorphic shellcode for creating a 
; directory with name "HACK" making the dir readable, writable and executable for 
; everyone(chmod 777) and then exiting gracefully.
; Testing: ./mkdir_polymorphic
; Compile with: ./compile.sh mkdir_polymorphic
; Size of shellcode: 25 bytes


global _start

section .text
_start:

	xor eax, eax                             ; Clearing out EAX register
	push eax                                 ; PUSH for NULL termination
	push dword 0x4b434148                    ; PUSH dir name HACK
	mov al, 0x27                             ; Load 0x27 syscall val for mkdir in AL 
	mov ebx, esp                             ; Store address of TOS in EBX
	int 0x80                                 ; Executing mkdir syscall
	mov al, 0xf                              ; Load 0x0f syscall val for chmod in AL
	mov cx, 0x1ff                            ; Load permission to CX
	int 0x80                                 ; Executing chmod syscall
	inc eax                                  ; Incrementing val of EAX to 1 - exit
	int 0x80                                 ; Executing exit syscall

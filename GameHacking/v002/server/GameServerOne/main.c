//
//  main.c
//  GameServerOne
//
//  Created by iHuggsy on 26/04/2024.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>         // Added for close()
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <errno.h>

#include "net_messages.h"

#define BUFFER_SIZE 4096
#define PORT        5000

#define TIME_TO_WIN 30

void* handle_client_message(void* arg);

typedef struct client_information
{
    int socket_fd;
    struct sockaddr_in client_info;
} client_information;

int main(int argc, char** argv)
{
    int sockfd, connfd;
    struct sockaddr_in servaddr, cliaddr;
    socklen_t clilen;
    pthread_t thread;

    // Create a TCP socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
    {
        perror("socket creation failed");
        exit(1);
    }

    // Set address and port number for the server
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(PORT);
    inet_pton(AF_INET, "0.0.0.0", &servaddr.sin_addr);

    // Bind the socket to the address and port
    if (bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
    {
        perror("bind failed");
        close(sockfd);
        exit(1);
    }

    // Listen for incoming connections
    if (listen(sockfd, 5) < 0)
    {
        perror("listen failed");
        close(sockfd);
        exit(1);
    }

    printf("TCP server listening on port %d...\n", PORT);

    while (1)
    {
        clilen = sizeof(cliaddr);

        // Accept a new connection
        connfd = accept(sockfd, (struct sockaddr *)&cliaddr, &clilen);
        if (connfd < 0)
        {
            perror("accept failed");
            continue;
        }

        // Allocate memory for client information
        client_information* info = malloc(sizeof(client_information));
        if (!info)
        {
            perror("malloc failed");
            close(connfd);
            continue;
        }

        info->client_info = cliaddr;
        info->socket_fd = connfd;

        // Create a new thread to handle the client
        if (pthread_create(&thread, NULL, handle_client_message, (void*) info) != 0)
        {
            perror("pthread_create failed");
            free(info);
            close(connfd);
            continue;
        }
        
        pthread_detach(thread); // Detach the thread to reclaim resources when it exits
    }

    close(sockfd);
    return 0;
}

uint8_t error_check(ssize_t received)
{
    if (received <= 0)
    {
        if (received == 0)
        {
            printf("Client disconnect\n");
            return 1;
        }
        else
        {
            perror("recv failed");
            return 1;
        }
    }
    
    return 0;
}

int parse_data_frame(void)
{
    return -1;
}

__int128 handle_game_start(int connfd)
{
    unsigned __int128 g_start = 0; // Sucks ?
    recv(connfd, &g_start, sizeof(g_start), 0);
    
    printf("Received g_start : %llx\n", g_start & 0xFFFFFFFFFFFFFFFF);
    
    send(connfd, GAME_START_ACK, sizeof(GAME_START_ACK), 0);
    
    return g_start;
}

__int128 handle_game_end(int connfd)
{
    unsigned __int128 g_start = 0; // Sucks ?
    recv(connfd, &g_start, sizeof(g_start), 0);
    
    printf("Received g_start : %llx\n", g_start & 0xFFFFFFFFFFFFFFFF);
    
    send(connfd, GAME_END_ACK, sizeof(GAME_END_ACK), 0);
    
    return g_start;
}


void handle_ping(int connfd)
{
    send(connfd, PING_ACK, sizeof(PING_ACK), 0);
}


void* handle_client_message(void* arg)
{
    client_information* info   = (client_information*) arg;
    int connfd                 = info->socket_fd;
    struct sockaddr_in cliaddr = info->client_info;
    unsigned __int128 c_start  = 0;
    unsigned __int128 c_end    = 0;
    
    // Get the client's IP address and port number
    char cli_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &cliaddr.sin_addr, cli_ip, sizeof(cli_ip));
    int cli_port = ntohs(cliaddr.sin_port);

    printf("Client %s:%d connected\n", cli_ip, cli_port);

    // Handle client handshake
    uint32_t client_command = 0;
    ssize_t recv_len = recv(connfd, &client_command, sizeof(client_command), 0);
    if (recv_len <= 0)
    {
        perror("recv failed");
        close(connfd);
        free(info);
        return NULL;
    }

    client_command = ntohl(client_command);

    if (client_command != 0xFAF002FF) // Game, version 0.02
    {
        printf("Client sent %#x\n", client_command);
        send(connfd, NOK_CLIENT_VERSION, strlen(NOK_CLIENT_VERSION), 0);
        close(connfd);
        free(info);
        return NULL;
    }

    printf("Success! Client sent command %#x\n", client_command);
    send(connfd, OK_CLIENT_VERSION, strlen(OK_CLIENT_VERSION), 0);

    // Handle client requests
    while (1)
    {
        uint8_t frame_id = 0;
        
        printf("Waiting for client frame ");
        ssize_t received = recv(connfd, &frame_id, sizeof(frame_id), 0);

        if (error_check(received))
            goto cleanup;

        printf("Received %zd bytes\n", received);
        printf("Frame id: %u\n", frame_id);
        
        switch (frame_id) {
            case 1:
                handle_ping(connfd);
                break;
            case 2:
                // Allows for the client to redefine its game start if sending another "game start" packet.
                // Leaving this as-is so that's a solve too
                c_start = handle_game_start(connfd);
                break;
            case 3:
                c_end = handle_game_end(connfd);
                break;
            case 4:
                if ((c_start + (1000000 * TIME_TO_WIN) >= c_end)  // 30s
                    && (c_start && c_end))                        // Not 0 ;)
                {
                    send(connfd, GAME_FLAG, sizeof(GAME_FLAG), 0);
                }
                else
                {
                    send(connfd, GAME_NO_FLAG, sizeof(GAME_NO_FLAG), 0);
                }
                
                goto cleanup;
            default:
                break;
        }

    }

cleanup:
    close(connfd);
    free(info);

    return NULL;
}

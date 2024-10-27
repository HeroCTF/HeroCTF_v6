//
//  main.c
//  GameServerThree
//
//  Created by iHuggsy on 17/10/2024.
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
#include <math.h>

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

typedef struct enemy
{
    uint8_t id;
    uint8_t hp;
    uint8_t damage;
} enemy;

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

int handle_client_position(int connfd,
                           float *c_x,
                           float *c_y,
                           uint8_t *knocked_back,
                           time_t *sand_start,
                           time_t *sand_stop)
{
    float x, y = 0;
    recv(connfd, &x, sizeof(x), 0);
    recv(connfd, &y, sizeof(y), 0);
    
    printf("Received x %f, y %f\n", x, y);
    printf("Diff x : %f, diff y %f", fabs((*c_x) - (x)), fabs((*c_y) - (y)));
    
    // Absolute value of current position - previous position > 1 ?
    // Also, has position ever been set ?
    // This might allow you to TP right after spawn
    // Or TP from the (0,0) position.
    // Fix: to handle knockback, have to authorize > 1 movement
    //      right after taking damage though
    // Not expecting the user to actually find this
    if ((fabs((*c_x) - (x)) > 1 || fabs((*c_y) - (y)) > 1)
        && (*c_x && *c_y))
                                                         
    {
        if (*knocked_back)
        {
            *knocked_back = 0;
        }
        else
        {
            send(connfd, CLIENT_POS_NOK, sizeof(CLIENT_POS_NOK), 0);
            return 1;
        }
    }
    
    *c_x = x;
    *c_y = y;
    
    // Approx the y where sand starts
    if (y > 71)
    {
        // I'm too nice
        if (x < 12 || x > 137)
            goto send_ack;
        
        if (!*sand_start)
        {
            printf("SAND START\n");
            time(sand_start);
        }
    }
    else
    {
        if (!*sand_stop && *sand_start)
        {
            printf("SAND STOP\n");
            time(sand_stop);
        }
    }
send_ack:
    send(connfd, CLIENT_POS_ACK, sizeof(CLIENT_POS_ACK), 0);
    
    return 0;
}

int handle_client_damage(int connfd, uint8_t *user_hp, uint8_t *knocked_back)
{
    uint8_t damage = 0;
    recv(connfd, &damage, sizeof(damage), 0);
    
    if ((*user_hp - damage) > *user_hp) // Did we overflow ?
        return 1;
    else
        *user_hp = (*user_hp - damage);
    printf("New hp : %u (dmg %u)\n", *user_hp, damage);
    
    // Temporarly authorize more than 1 px move
    *knocked_back = 1;
    
    return 0;
}

// Created inplace from values given by the client
// User can overwrite these in the client binary.
int handle_client_enemy_creation(int connfd, enemy enemies[])
{
    
    for (uint8_t i = 0; i < 13; i++)
    {
        enemy current_enemy = {0};
        recv(connfd, &current_enemy.id, 1, 0);
        recv(connfd, &current_enemy.hp, 1, 0);
        recv(connfd, &current_enemy.damage, 1, 0);
        
        enemies[i] = current_enemy;
        
        printf("Created enemy : id #%u hp %u dmg %u\n", current_enemy.id, current_enemy.hp, current_enemy.damage);
    }
    
    return 9;
}

void handle_damage(int connfd,
                   enemy *enemies,
                   uint8_t *user_damage)
{
    uint8_t to = 0;
    recv(connfd, &to, sizeof(to), 0);
    
    // I h8 hackrz
    if (to >= 13)
    {
        close(connfd);
        return;
    }
    
    if (enemies[to].hp < *user_damage)
    {
        enemies[to].hp = 0;
    }
    else
    {
        enemies[to].hp -= *user_damage;
    }
    
    send(connfd, &enemies[to].hp, 1, 0);
    
    printf("Enemy : ID %u, hp %u, dmg %u", enemies[to].id, enemies[to].hp, enemies[to].damage);
    
}

void handle_treasure(int connfd, enemy *treasure)
{
    treasure->hp = 0;
    send(connfd, DMG_ACK, sizeof(DMG_ACK), 0);
}

unsigned int handle_flag(int connfd, enemy *treasure, enemy *enemies, time_t *sand_time)
{
    uint8_t enemies_alive = 0;
    
    for (unsigned int i = 0; i < 13; ++i)
    {
        if (enemies[i].hp)
        {
            ++enemies_alive;
        }
    }
    
    if (treasure->hp)
        ++enemies_alive;
    
    return enemies_alive && (*sand_time > 10);
}

void* handle_client_message(void* arg)
{
    client_information* info   = (client_information*) arg;
    int connfd                 = info->socket_fd;
    struct sockaddr_in cliaddr = info->client_info;
    
    // Game data
    unsigned __int128 c_start  = 0;
    unsigned __int128 c_end    = 0;
    float last_x               = 0;
    float last_y               = 0;
    uint8_t knocked_back       = 0;
    
    uint8_t user_hp            = 100;
    uint8_t user_dmg           = 1;
    
    enemy* enemies             = malloc(sizeof(enemy) * 13);
    enemy* treasure            = malloc(sizeof(enemy));
    
    treasure->hp               = 1;
    treasure->id               = 0;
    treasure->damage           = 0;
    
    time_t sand_time           = 0;
    time_t start_sand          = 0;
    time_t stop_sand           = 0;
    
    
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

    if (client_command != 0xFAF004FF) // Game, version 0.04
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
        printf("\n-------------------------------\n");
        printf("Waiting for client frame ... \n");
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
                
                if (handle_client_position(connfd, &last_x, &last_y, &knocked_back, &start_sand, &stop_sand))
                {
                    close(connfd);
                }
                
                if (start_sand && stop_sand)
                {
                    printf("Start time : %li\n", start_sand);
                    printf("stop time : %li\n", stop_sand);
                    
                    sand_time += difftime(stop_sand, start_sand);
                    start_sand = 0;
                    stop_sand = 0;
                }
                
                printf("got sand time : %li\n", sand_time);
                
                break;
            case 5:
                printf("HP request : %u\n", user_hp);
                send(connfd, &user_hp, sizeof(user_hp), 0);
                break;
            case 6:
                if (handle_client_damage(connfd, &user_hp, &knocked_back))
                {
                    goto cleanup;
                }
                break;
            case 7:
                handle_client_enemy_creation(connfd, enemies);
            case 8:
                handle_damage(connfd, enemies, &user_dmg);
            case 9:
                handle_treasure(connfd, treasure);
            case 10:
                if (handle_flag(connfd, treasure, enemies, &sand_time))
                {
                    send(connfd, GAME_NO_FLAG, sizeof(GAME_NO_FLAG), 0);
                }
                else
                {
                    send(connfd, GAME_FLAG, sizeof(GAME_FLAG), 0);
                }
            default:
                break;
        }

    }

cleanup:
    close(connfd);
    free(info);

    return NULL;
}

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <string.h>

// gcc -o state -s -Wall -Wextra state.c

#define FLAG_LEN 30
#define N 256

void swap(unsigned char *a, unsigned char *b) {
    unsigned char tmp = *a;
    *a = *b;
    *b = tmp;
}

void KSA(unsigned char *S, unsigned char *key, int keylen) {
    int i, j = 0;
    for (i = 0; i < N; ++i) S[i] = i;
    for (i = 0; i < N; ++i) {
        j = (j + S[i] + key[i % keylen]) % N;
        swap(&S[i], &S[j]);
    }
}

void PRGA(unsigned char *S, unsigned char *data, int datalen) {
    int i = 0, j = 0, x;
    for (x = 0; x < datalen; x++) {
        i = (i + 1) % N;
        j = (j + S[i]) % N;
        swap(&S[i], &S[j]);
        data[x] ^= S[(S[i] + S[j]) % N];
    }
}

void dump_stack() {
    FILE *maps_file, *out_file;
    unsigned long start, end;
    char line[256];

    if ((maps_file = fopen("/proc/self/maps", "r")) == NULL) {
        perror("fopen maps");
        exit(EXIT_FAILURE);
    }

    while (fgets(line, sizeof(line), maps_file)) {
        if (strstr(line, "[stack]")) {
            if (sscanf(line, "%lx-%lx", &start, &end) != 2) {
                fprintf(stderr, "Failed to parse stack range\n");
                fclose(maps_file);
                exit(EXIT_FAILURE);
            }
            break;
        }
    }
    fclose(maps_file);

    if ((out_file = fopen("stack.bin", "wb")) == NULL) {
        perror("fopen stack.bin");
        exit(EXIT_FAILURE);
    }

    fwrite((void*) start, 1, end - start, out_file);

    fclose(out_file);
}


int main() {
    int key_fd, flag_fd;
    unsigned char *key = malloc(16);
    unsigned char *buf = malloc(FLAG_LEN);
    unsigned char S[N];

    if ((key_fd = open("/dev/urandom", O_RDONLY)) < 0 || read(key_fd, key, 16) != 16 ||
        (flag_fd = open("flag.txt", O_RDONLY)) < 0 || read(flag_fd, buf, FLAG_LEN) != FLAG_LEN)
        return 1;

    close(key_fd);
    close(flag_fd);

    KSA(S, key, 16);
    PRGA(S, buf, FLAG_LEN);

    for (int i = 0; i < FLAG_LEN; i++)
        printf("%02hhx", buf[i]);
    printf("\n");

    dump_stack();

    free(key);
    free(buf);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    const char *new_root = "/jail/";
    if (chroot(new_root) != 0) {
        perror("chroot");
        exit(EXIT_FAILURE);
    }
    if (chdir("/") != 0) {
        perror("chdir");
        exit(EXIT_FAILURE);
    }
    char *shell = "/bin/sh";
    char *args[] = {shell, NULL};

    if (execv(shell, args) != 0) {
        perror("execv");
        exit(EXIT_FAILURE);
    }

    return 0;
}

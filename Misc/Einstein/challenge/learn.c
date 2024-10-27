#include <stdio.h>
#include <unistd.h>

int main() {
    // Welcome message
    printf("Welcome to this physics course! All information on this course is not copied from the internet without fact check and is completely riginal.\n");
    printf("\n===================================\n\n");
    
    // Execute cat command
    setreuid(geteuid(), geteuid()); // Because system() runs sh that resets euid to uid if they don't match
                                    // Otherwise we could not read /home/einstein/theory.txt
    char command[30] = "cat /home/einstein/theory.txt";
    if (system(command) == -1) {
        perror("system");
        return 1;
    }

    return 0;
}
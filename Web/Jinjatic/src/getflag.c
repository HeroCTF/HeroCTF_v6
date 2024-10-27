#include <stdio.h>
#include <stdlib.h>

int main() {
    const char *file_path = "/root/flag.txt";
    
    FILE *file = fopen(file_path, "r");
    if (file == NULL) {
        perror("Erreur lors de l'ouverture du fichier");
        return EXIT_FAILURE;
    }

    char ch;
    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    fclose(file);

    return EXIT_SUCCESS;
}
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define SIZE 4

int skyscrapersLeft[SIZE] = {2, 2, 3, 1};
int skyscrapersRight[SIZE] = {3, 2, 1, 2};
int skyscrapersTop[SIZE] = {3, 1, 2, 2};
int skyscrapersBottom[SIZE] = {1, 3, 2, 2}; 

void printBoard(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%d ", board[i][j]);
        }
        printf("\n");
    }
}

void printFlag() {
    const char* env_var_name = "FLAG";
    char* env_value = getenv(env_var_name);

    if (env_value != NULL) {
        printf("%s\n", env_value);
    } else {
        puts("Flag is undefined!");
    }
}

void makeMove(int board[SIZE][SIZE], int row, int col, int value) {
    board[row][col] = value;
}

bool isBoardFull(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == 0) {
                return false;
            }
        }
    }
    return true;
}

bool areCoordinatesValid(int row, int col) {
    return row >= 0 && row < SIZE && col >= 0 && col < SIZE;
}

bool isValueValid(int value) {
    return value >= 1 && value <= SIZE;
}

bool checkNoDuplicates(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE - 1; j++) {

            // Check for duplicates in the same row
            for (int k = 0; k < SIZE; k++) {
                if (j == k) continue;
                if (board[i][j] == board[i][k]) return false;
            }

            // Check for duplicates in the same column
            for (int k = 0; k < SIZE; k++) {
                if (i == k) continue;
                if (board[i][j] == board[k][j]) return false;
            }

        }
    }

    return true;
}

bool checkSkyscrapersLeft(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        int count = 0;
        int max = 0;

        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] > max) {
                max = board[i][j];
                count++;
            }
        }

        if (count != skyscrapersLeft[i]) {
            return false;
        }
    }
    return true;
}

bool checkSkyscrapersRight(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        int count = 0;
        int max = 0;

        for (int j = SIZE - 1; j >= 0; j--) {
            if (board[i][j] > max) {
                max = board[i][j];
                count++;
            }
        }

        if (count != skyscrapersRight[i]) {
            return false;
        }
    }
    return true;
}

bool checkSkyscrapersTop(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        int count = 0;
        int max = 0;

        for (int j = 0; j < SIZE; j++) {
            if (board[j][i] > max) {
                max = board[j][i];
                count++;
            }
        }

        if (count != skyscrapersTop[i]) {
            return false;
        }
    }
    return true;
}

bool checkSkyscrapersBottom(int board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        int count = 0;
        int max = 0;

        for (int j = SIZE - 1; j >= 0; j--) {
            if (board[j][i] > max) {
                max = board[j][i];
                count++;
            }
        }

        if (count != skyscrapersBottom[i]) {
            return false;
        }
    }
    return true;
}

bool checkSkyscrapersCount(int board[SIZE][SIZE]) {
    return checkSkyscrapersLeft(board) && checkSkyscrapersRight(board) && checkSkyscrapersTop(board) && checkSkyscrapersBottom(board);
}

bool checkWin(int board[SIZE][SIZE]) {
    return isBoardFull(board) && checkNoDuplicates(board) && checkSkyscrapersCount(board);
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    int board[SIZE][SIZE] = {0};
    int row, col, value;
    char action;

    while (true) {
        // printBoard(board);
        printf("Enter an action: ");
        scanf(" %c", &action);

        if (action == 'q' || action == 'Q') {
            puts("Quitting...");
            break;
        } else if (action == 'w' || action == 'W') {
            if (checkWin(board)) {
                printFlag();
                break;
            } else {
                puts("Not today!");
            }
        } else if (action == 's' || action == 'S') {
            printf("Enter row, column and value: ");
            scanf("%d %d %d", &row, &col, &value);

            if (areCoordinatesValid(row, col) && isValueValid(value)) {
                makeMove(board, row, col, value);
            } else {
                puts("Invalid value or coordinates!");
            }
        }
    }

    return 0;
}

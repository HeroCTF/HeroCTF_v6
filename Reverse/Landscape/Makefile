CC = gcc
CFLAGS = -Wall -Wextra

SOURCE = game.c
OUTPUT = game

all: $(OUTPUT)

$(OUTPUT): $(SOURCE)
	$(CC) $(CFLAGS) -o $(OUTPUT) $(SOURCE)

clean:
	rm -f $(OUTPUT)

.PHONY: all clean

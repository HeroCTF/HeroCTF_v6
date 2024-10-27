# Landscape

### Category

Reverse

### Description

You just discovered a new game, but it seems the developer omitted to include a user interface. Although it responds to player inputs, there's no concluding message or feedback.

To understand the game's mechanics and solve it, reverse engineer the binary.

You can reverse the challenge locally and deploy an instance to validate the flag on : **https://deploy.heroctf.fr**<br>

Format : **Hero{flag}**<br>
Author : **xanhacks**

### Files

- [landscape.zip](landscape.zip)

### Write Up

The `game` binary is an implementation of the game [Skyscrapers](https://www.puzzle-skyscrapers.com/) with a 4x4 grid.

The rules are of the game are simple.

The objective is to place skyscrapers in all cells on the grid according to the rules:

1. The height of the skyscrapers is from 1 to the size of the grid i.e. 1 to 4 for a 4x4 puzzle.
2. You cannot have two skyscrapers with the same height on the same row or column.
3. The numbers on the sides of the grid indicate how many skyscrapers would you see if you look in the direction of the arrow.

Place numbers in each cell to indicate the height of the skyscrapers.

You can quicky identify the `checkWin` function which is right before the `printFlag` one. You can extract the rules of the game from it and find the name of the game.

Then, you can create a script like [solve.py](./solve.py) to solve the challenge.

> The source code of the challenge is available in the [game.c](./game.c) file.

### Flag

- Hero{L4nd5c4p3_0f_Sky5cr4p3r5}
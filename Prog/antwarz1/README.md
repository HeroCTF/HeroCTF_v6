# Antwarz PVE - Easy

### Category

Prog

### Description

In this challenges, you will have to code your own bot, that will control an ant colony.

In the two first challenges (easy and medium), you will compete against my bots. If you succeed, you will enter the PVP arena, to compete against other players.

10min before the CTF's end, scoring will stop, and the team with the most points will be awarded a flag worth 10 points. It might not be much, but it could mean the different between a second or first place ;)

Find out more about the game in the documentation section of the dedicated plateform!

It's worth noting that the goal of the challenges is not to exploit the plateform, but to create the best bot possible. Anyone finding a security failure is welcome to report it, but any challenge solved through such a vulnerability would be rendered void.

You can find the source code of the game engine with the first challenge of the series, would you want to it up locally.

> `nc antwarz.heroctf.fr 8080`

Format : **Hero{flag}**<br>
Author : **Log_s**

### Files

- [antwarz.zip](./antwarz.zip)
- [base64_code](./base64_code.py)

### Write Up

The easy bot has 2 main features :
- All ants move at random, and directly go back to the base if they walk on a sugar cube
- They avoid at all cost collisions with friendly and ennemy ants

One strategy to beat it, is to use the strategy used by the medium bot :
- Avoid collisions
- Have a searcher ant
- Once a sugar cube is located, have all ants empty it as fast as possible

This beats by far the randomness of the first bot.

You can find the code of the medium bot here: [player.py](src/engine/player.py)

### Flag

Hero{00ace8b68a3879022ed7b05349276445}
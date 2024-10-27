# Antwarz PVE - Medium

### Category

Prog

### Description

In this challenges, you will to code your own bot, that will control an ant colony.

In the two first challenges (easy and medium), you will compete against my bots. If you succeed, you will enter the PVP arena, to compete against other players.

10min before the CTF's end, scoring will stop, and the team with the most points will be awarded a flag worth 10 points. It might not be much, but it could mean the different between a second or first place ;)

Find out more about the game in the documentation section of the dedicated plateform!

It's worth noting that the goal of the challenges is not to exploit the plateform, but to create the best bot possible. Anyone finding a security failure is welcome to report it, but any challenge solved through such a vulnerability would be rendered void.

You can find the source code of the game engine with the first challenge of the series, would you want to it up locally.

> `nc antwarz.heroctf.fr 8080`

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write Up

The medium bot is a bit more complexe :
- It has a searcher ant, that recons the grid to find a new sugar cube
- Once a sugar cube is located, the colonny will empty it, following a circular route, to avoid blocking one another
- While emptying the cube, they are carefull not to step on ANY ant

One strategy to beat it, is to use the strategy used by the medium bot :
- while you have your own strategy to collect cubes, you should send one ant on the path of the ennemy colonny collect path to stop them
- if your ant get's killed, buy another one as soon as you have enough sugar

This beats by far the randomness of the first bot.

The code for this bot has not being developped, but a community list of community solution will be linked below, since there are many ways to achieve a better bot.

```
INCOMING
```

### Flag

Hero{4a2f05023630b7501944632bad98c103}

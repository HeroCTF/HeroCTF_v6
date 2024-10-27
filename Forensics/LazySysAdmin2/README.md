# Lazy SysAdmin 2

## Presentation

## Solve

```
$ unzip server-SX03.zip
$ sudo mkdir /mnt/server-SX03
$ sudo mount -o loop server-SX03.iso /mnt/server-SX03
```

quick-win : 

* hunt for persistency
* check writable directory :> /tmp



```
$ sudo ls /mnt/server-SX03
snap-private-tmp
systemd-private-348526c591fc4c6daf7854122ed5d559-colord.service-K1yBYk
systemd-private-348526c591fc4c6daf7854122ed5d559-ModemManager.service-qxPu3A
systemd-private-348526c591fc4c6daf7854122ed5d559-polkit.service-aJ9Bgg
systemd-private-348526c591fc4c6daf7854122ed5d559-power-profiles-daemon.service-j7judX
systemd-private-348526c591fc4c6daf7854122ed5d559-switcheroo-control.service-rUsVHb
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-logind.service-Pfep5n
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-oomd.service-gGR3oq
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-resolved.service-IIGfmC
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-timesyncd.service-jjkCdJ
systemd-private-348526c591fc4c6daf7854122ed5d559-upower.service-L8E8ug

$ sudo ls -a /mnt/server-SX03
.
..
.font-unix
.ICE-unix
.script.sh
snap-private-tmp
systemd-private-348526c591fc4c6daf7854122ed5d559-colord.service-K1yBYk
systemd-private-348526c591fc4c6daf7854122ed5d559-ModemManager.service-qxPu3A
systemd-private-348526c591fc4c6daf7854122ed5d559-polkit.service-aJ9Bgg
systemd-private-348526c591fc4c6daf7854122ed5d559-power-profiles-daemon.service-j7judX
systemd-private-348526c591fc4c6daf7854122ed5d559-switcheroo-control.service-rUsVHb
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-logind.service-Pfep5n
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-oomd.service-gGR3oq
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-resolved.service-IIGfmC
systemd-private-348526c591fc4c6daf7854122ed5d559-systemd-timesyncd.service-jjkCdJ
systemd-private-348526c591fc4c6daf7854122ed5d559-upower.service-L8E8ug
.wrapper_script.sh
.X0-lock
.X1024-lock
.X1025-lock
.X11-unix
.X1-lock
.XIM-unix
```

hmmn, wrapper_script.sh and script.sh

```
$ cat /mnt/clean/tmp/.wrapper_script.sh 
#!/bin/bash

while true; do
  # Your main script code here
  /tmp/.script.sh

  # Wait for 15 seconds before running again
  sleep 15
done
```

```
$ cat /mnt/clean/tmp/.script.sh 
#!/bin/bash

# get a random number
RANDOM_NUMBER=$(shuf -i 1-13 -n 1)

# retrieve content remotly from a pastebin
INSUTLS=$(curl -s https://pastebin.com/raw/59mL2V9i)

#select the n-th line (n being chosen randomly)
temp=$(echo "$INSUTLS" | sed -n "${RANDOM_NUMBER}p" )

#decode the content base64-encoded
tempp= echo "$temp" | base64 -id

# display to all terminal the content
wall $tempp
```


what is the content retrieve ?

```
$ curl -s https://pastebin.com/raw/59mL2V9i
WW91IHN1Y2sgIQ==
RnVja2luZyBpZGlvdCA=
WW91IHN1Y2sgIQ==
U2VyaW91c2x5LCBXaG8gdGhlIGZ1Y2sgaXMgVm96ZWs/
WW91IHN1Y2sgIQ==
WW91IHN1Y2sgIQ==
WW91IHN1Y2sgIQ==
WFhYX0Q0cmtfcm9ndWUgaXMgdGhlIGJlc3QgISA=
SEVST3tBbHdhWXMtQ2gzY2tfV2hhdF91LUMwUHktUDRzdGV9
WW91IHN1Y2sgIQ==
RGlkIHlvdSByZWFsbHkgYmVsaWV2ZSBpdCB3YXMgcG9zc2libGUgdG8gZG93bmxvYWQgUkFNLCB5b3UgZHVtYmFzcyB4RA==
WW91IHN1Y2sgIQ==
WW91IHN1Y2sgIQ==
```

```
$ for line in $(curl -s https://pastebin.com/raw/59mL2V9i); do echo $line | base64 -di; echo  ; done
You suck !
Fucking idiot 
You suck !
Seriously, Who the fuck is Vozek?
You suck !
You suck !
You suck !
XXX_D4rk_rogue is the best ! 
HERO{AlwaYs-Ch3ck_What_u-C0Py-P4ste}
You suck !
Did you really believe it was possible to download RAM, you dumbass xD
You suck !
You suck !
```


**Flag** : HERO{AlwaYs-Ch3ck_What_u-C0Py-P4ste}

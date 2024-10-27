# Buafllet

### Category

Pwn

### Description

You have one bullet, use it wisely...

Format : **Hero{flag}**<br>
Author : **ghizmo**

### Files

- buafllet.ko
- config
- Image
- initramfs.cpio.gz
- run.sh


### Write Up

#### TL;DR

- 1 UAF of size between 0x490 and 0x3000
- bypass RANDOM_KMALLOC_CACHES


#### Analysis

Few files are provided to emulate in local and 2 ports are open.
One connects to a docker in order to push our exploit, the other connects on a qemu-system-aarch64.

We can see in config file that lot of mitigations around SLUB are activated.
```
CONFIG_SLAB_FREELIST_RANDOM=y
CONFIG_SLAB_FREELIST_HARDENED=y
CONFIG_RANDOM_KMALLOC_CACHES=y

CONFIG_USERFAULTFD=n
CONFIG_FUSE_FS=n
```

And in the run.sh, KASLR, PXN, PAN and KPTI are activated.
The environment is a linux-6.6.57 running on AARCH64.

The challenge is to exploit `buafflet.ko` and by reversing it we can clearly see that we have the symbols.

It's simple Linux Kernel Module with 4 ioctls:
- ioctl_get_builet
- ioctl_shoot
- ioctl_read
- ioctl_write

The ioctl_get_bullet (0x10) allows us to perform a kzalloc of a size between 0x490 and 0x3000.

The ioctl_shoot (0x11) does a kfree, but doesn't null the bullet pointer, leading to a UAF.

The ioctl_read (0x12) and ioctl_write(0x13) let us read/write 0x400 in the bullet pointer.

So the challenge is clear, we have to exploit an UAF to become Root and read the flag.
The problem is that the kernel mitigations such as `CONFIG_RANDOM_KMALLOC_CACHES` are on, which aimes to make exploiting slab heap corruption more difficult. More information about this mitigation can be found at https://sam4k.com/exploring-linux-random-kmalloc-caches/.

By playing with the module, we can see that our UAF is (almost) never allocated by our spray. But the only thing in this challenge that we can "manipulate" is the allocation size.

#### Exploitation

Let's have a look to kmalloc source code:

```c
// /include/linux/slab.h

#define KMALLOC_SHIFT_HIGH	(PAGE_SHIFT + 1)
#define KMALLOC_MAX_CACHE_SIZE	(1UL << KMALLOC_SHIFT_HIGH)

static __always_inline __alloc_size(1) void *kmalloc(size_t size, gfp_t flags)
{
	if (__builtin_constant_p(size) && size) {
		unsigned int index;

		if (size > KMALLOC_MAX_CACHE_SIZE) // <-------- Interesting (1)
			return kmalloc_large(size, flags);

		index = kmalloc_index(size);
		return kmalloc_trace(
				kmalloc_caches[kmalloc_type(flags, _RET_IP_)][index],
				flags, size);  // <-------- Not Interesting (2)
	}
	return __kmalloc(size, flags);
}
```

We can see in (2) that this is the part where the RANDOM_KMALLOC_CACHE takes place, since it will allocate on a random cache.
But, just before, in (1) we have this little snippet which does a kmalloc_large and doesn't seems to take random cache in count.





### Flag

Hero{0neBu773t_To_R0Ot_Th3m_4LL192038_a8239320132489328912302839132421}


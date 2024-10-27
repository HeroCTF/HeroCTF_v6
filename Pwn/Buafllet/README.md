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

We can see in (2) that this is the part where the RANDOM_KMALLOC_CACHE takes place, since it will allocate on a random cache, using `_RET_IP_`.

```c
static __always_inline enum kmalloc_cache_type kmalloc_type(gfp_t flags, unsigned long caller)
{
	if (likely((flags & KMALLOC_NOT_NORMAL_BITS) == 0))
#ifdef CONFIG_RANDOM_KMALLOC_CACHES
		/* RANDOM_KMALLOC_CACHES_NR (=15) copies + the KMALLOC_NORMAL */
		return KMALLOC_RANDOM_START + hash_64(caller ^ random_kmalloc_seed,
						      ilog2(RANDOM_KMALLOC_CACHES_NR + 1));
#else
		return KMALLOC_NORMAL;

	// [...]
}
```

But, just before, in (1), we have this little snippet which does a kmalloc_large and doesn't seems to take random cache in count. This part of the code is reached if `size > KMALLOC_MAX_CACHE_SIZE`.

```c
void *kmalloc_large(size_t size, gfp_t flags)
{
	void *ret = __kmalloc_large_node(size, flags, NUMA_NO_NODE);

	trace_kmalloc(_RET_IP_, ret, size, PAGE_SIZE << get_order(size),
		      flags, NUMA_NO_NODE);
	return ret;
}
```

```c
/*
 * To avoid unnecessary overhead, we pass through large allocation requests
 * directly to the page allocator. We use __GFP_COMP, because we will need to
 * know the allocation order to free the pages properly in kfree.
 */

static void *__kmalloc_large_node(size_t size, gfp_t flags, int node)
{
	struct page *page;
	void *ptr = NULL;
	unsigned int order = get_order(size);

	if (unlikely(flags & GFP_SLAB_BUG_MASK))
		flags = kmalloc_fix_flags(flags);

	flags |= __GFP_COMP;
	page = alloc_pages_node(node, flags, order);
	if (page) {
		ptr = page_address(page);
		mod_lruvec_page_state(page, NR_SLAB_UNRECLAIMABLE_B,
				      PAGE_SIZE << order);
	}

	ptr = kasan_kmalloc_large(ptr, size, flags);
	/* As ptr might get tagged, call kmemleak hook after KASAN. */
	kmemleak_alloc(ptr, size, 1, flags);
	kmsan_kmalloc_large(ptr, size, flags);

	return ptr;
}
```

With this in hand, we can try something.

First, kmalloc more than 0x2000 to go in the interesting part, using `ioctl_get_builet`.
Next, kfree it, with `ioctl_shoot`.
Now, you can spray with any object it will ends in the chunk.
The rest is straightfoward, using a "good" object, we leak kaslr, heap address and gain arbitrary read/write to patch creds, or using modprobe_path.

The object choosen in the PoC [exploit.c](prod/exploit/exploit.c) is tty_struct, since it's very simple. But any objects works as well.




### Flag

Hero{0neBu773t_To_R0Ot_Th3m_4LL192038_a8239320132489328912302839132421}


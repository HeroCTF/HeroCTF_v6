#include <linux/module.h>
#include <linux/interrupt.h>
#include <linux/kernel.h>
#include <linux/spinlock.h>
#include <linux/miscdevice.h>
#include <linux/platform_device.h>
#include <linux/poll.h>
#include <linux/sched.h>
#include <linux/bitops.h>
#include <linux/io.h>
#include <linux/goldfish.h>
#include <linux/mm.h>
#include <linux/acpi.h>
#include <linux/init.h>
#include <linux/printk.h>
#include <linux/mutex.h>

#include "buafllet.h"


/********* Init Driver *********/
#define DEVICE_NAME "buafllet"

char *bullet = NULL;
DEFINE_MUTEX(g_mutex);
static int bullet_used = 0;


MODULE_AUTHOR("ghizmo");
MODULE_DESCRIPTION("Buafllet");
MODULE_LICENSE("GPL");

static const struct file_operations buafllet_fops = {
    .owner =            THIS_MODULE,
    .open =             buafllet_open,
    .release =          buafllet_release,
    .unlocked_ioctl =   buafllet_ioctl,
};

static struct miscdevice buafllet_miscdev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = DEVICE_NAME,    
    .fops = &buafllet_fops,
};

/*******************************/






/*********** IOCTLs ***********/
long int buafllet_ioctl(struct file *fp, unsigned int cmd, unsigned long arg){
    long int ret = 0x0;

    switch(cmd) {
        case IOCTL_GET_BULLET:
            ret = ioctl_get_bullet(arg);
            break;
        case IOCTL_SHOOT:
            ret = ioctl_shoot();
            break;


        case IOCTL_READ:
            if (bullet != NULL)
            {
                if(copy_to_user((char __user *)arg, bullet, 0x400))
                    return -EFAULT;
            }
            break;

        case IOCTL_WRITE:
            if (bullet != NULL)
            {
                if (copy_from_user(bullet, (const char __user *)arg, 0x400))
                    return -EFAULT;
            }
            break;


        default:
            break;
    }

    return ret;
}

int ioctl_get_bullet(unsigned long arg){
    size_t size;
    if( copy_from_user(&size, (void __user *) arg, sizeof(size)) )
        return -EFAULT;

    if(size >= 0x3000 || size <= 0x490)
    {
        return -EFAULT;
    }

    printk("Take this bullet...");

    mutex_lock(&g_mutex); 

    if (bullet_used) {
        mutex_unlock(&g_mutex);
        return -EBUSY;
    }

    bullet = kzalloc(size, GFP_KERNEL);

    bullet_used = 1;
    mutex_unlock(&g_mutex);


    return 0;
}


int ioctl_shoot(void) {
    mutex_lock(&g_mutex);

    if (!bullet_used) {
        mutex_unlock(&g_mutex);
        return -EINVAL;
    }

    kfree(bullet);

    mutex_unlock(&g_mutex);

    printk("Now what you gonna do?");
    
    return 0;
}
/******************************/












/********* Init Driver *********/
int buafllet_init(void) {
    int err = 0;

    pr_info("buafllet::buafllet_init \n");
    err = misc_register(&buafllet_miscdev);
    if(err) {
        pr_err("Unable to register buafllet driver\n");
        return err;
    }

    return 0;
}

void buafllet_exit(void) {
    pr_info("buafllet::exit\b");
    misc_deregister(&buafllet_miscdev);
}

int buafllet_open(struct inode *inode, struct file *file){
    pr_info("buafllet::open\n");
    return 0;
}

int buafllet_release(struct inode *inode, struct file *file){
    pr_info("buafllet::release\n");
    return 0;
}

module_init(buafllet_init);
module_exit(buafllet_exit);
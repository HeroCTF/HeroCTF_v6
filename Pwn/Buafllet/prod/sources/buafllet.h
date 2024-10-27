int buafllet_init(void);
void buafllet_exit(void);

int buafllet_open(struct inode *inode, struct file *file);
int buafllet_release(struct inode *inode, struct file *file);
long int buafllet_ioctl(struct file *fp, unsigned int cmd, unsigned long arg);


typedef unsigned int gfp_t;



/*********** IOCTLs ***********/
#define IOCTL_GET_BULLET   0x10
#define IOCTL_SHOOT     0x11

#define IOCTL_READ   0x12
#define IOCTL_WRITE  0x13

int ioctl_get_bullet(unsigned long arg);
int ioctl_shoot(void);


/******************************/
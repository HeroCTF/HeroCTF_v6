Giam v0.05 - solve 

This time, only one mission : kill the boss.

The boss struct is server sided, it should not be possible to actually cheat it.

```c
enemy* handle_enemy_creation(int connfd)
{
    enemy *bossito = (enemy*) malloc(sizeof(enemy));
    bossito->id = 420 % 255;
    bossito->hp = 255;
    bossito->damage = 100;
    printf("sending bossitpo \n");
    int serialized_boss = 0xFAFFF0;
    send(connfd, (char*)&serialized_boss, sizeof(serialized_boss), 0);
    
    return bossito;
}
```

A "boon" system is added, allowing you to increase your hp / damage


```c
void* handle_boon(void *boon_struc)
{
    boon_struct *bs = (boon_struct*) boon_struc;
    uint8_t boon_number = 0;
    recv(bs->connfd, &boon_number, sizeof(boon_number), 0);
    
    if (*bs->boond)
    {
        return 0;
    }
    // Fun thing is that it could overflow and potentially make your dmg / hp worse.
    // hf
    if (boon_number == 1)
    {
        printf("Increasing hp");
        *bs->hp += 5;
    }
    else
    {
        printf("Increasing dmg");
        *bs->dmg += 5;
    }
    
    // Nice race condition
    sleep(2);
    
    *bs->boond = 1;
    
    return 0;
}

[...]

                ; // <- I have to put this here so Xcode doesn't complain ?
                // Allows for the race condition.
                boon_struct *bs = (boon_struct*) malloc(sizeof(boon_struct));
                bs->connfd = connfd;
                bs->hp = &user_hp;
                bs->dmg = &user_damage;
                bs->boond = &booned;
                pthread_t thread;
                pthread_create(&thread, NULL, handle_boon, (void*) bs);
                
                printf("Damage : %u", user_damage);
                break;
```

A race condition has been introduced, allowing the player to request boons in the 2s timeframe where it is not locked.

The player can either increase his movespeed and go on the boon place multiple time in that window, or send the packets multiple times in order to maxx out the stats.

One possibility would also be to stop the enemy damage packets from going out, effectively rendering the boss useless.
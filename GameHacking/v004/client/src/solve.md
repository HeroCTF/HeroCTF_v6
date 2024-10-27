This time, the player damage and player HP is server sided.
The enemies structures are also on the server side, and damage done to them is reflected on the server.

```c
void handle_damage(int connfd,
                   enemy *enemies,
                   uint8_t *user_damage)
{
    uint8_t to = 0;
    recv(connfd, &to, sizeof(to), 0);
    
    // I h8 hackrz
    if (to >= 13)
    {
        close(connfd);
        return;
    }
    
    if (enemies[to].hp < *user_damage)
    {
        enemies[to].hp = 0;
    }
    else
    {
        enemies[to].hp -= *user_damage;
    }
    
    send(connfd, &enemies[to].hp, 1, 0);
    
    printf("Enemy : ID %u, hp %u, dmg %u", enemies[to].id, enemies[to].hp, enemies[to].damage);
    
}
```
There is a new mission : don't touch the sand for more than 10s  
The server also checks that the quests are "really done"

```c
unsigned int handle_flag(int connfd, enemy *treasure, enemy *enemies, time_t *sand_time)
{
    uint8_t enemies_alive = 0;
    
    for (unsigned int i = 0; i < 13; ++i)
    {
        if (enemies[i].hp)
        {
            ++enemies_alive;
        }
    }
    
    if (treasure->hp)
        ++enemies_alive;
    
    return enemies_alive && (*sand_time > 10);
}
```

The catch is that the enemies are declared to the server by the client

```rust
pub async fn declare_enemies(enemies : &Vec<Enemy>)
{
    let mut command_buffer: Vec<u8> = vec!(0x7u8);
    println!("wrote : {:?}", USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap());

    for nmi in enemies {
        let serialized = nmi.partial_serialize();
        println!("wrote : {:?}", USER_STREAM.lock().await.get(0).unwrap().write_all(&serialized).unwrap());
    }
}
```

```c
// Created inplace from values given by the client
// User can overwrite these in the client binary.
int handle_client_enemy_creation(int connfd, enemy enemies[])
{
    
    for (uint8_t i = 0; i < 13; i++)
    {
        enemy current_enemy = {0};
        recv(connfd, &current_enemy.id, 1, 0);
        recv(connfd, &current_enemy.hp, 1, 0);
        recv(connfd, &current_enemy.damage, 1, 0);
        
        enemies[i] = current_enemy;
        
        printf("Created enemy : id #%u hp %u dmg %u\n", current_enemy.id, current_enemy.hp, current_enemy.damage);
    }
    
    return 9;
}
```

It's possible to break at this function and modify the enemies HP values to bypass the "kill enemies quest".  

The treasure quest can be done as in the last challenge, or the packet can be fired any time (just a boolean flipping in the server)  

As for the "don't touch the sand" part, the client handles the character speed in this stub

```rust
    if is_key_down(macroquad::input::KeyCode::W) 
    {
        character_state.sprite_displacement.y -= 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 180;
    }
    if is_key_down(macroquad::input::KeyCode::S) {
        character_state.sprite_displacement.y += 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 0;
    }
    if is_key_down(macroquad::input::KeyCode::A) {
        character_state.sprite_displacement.x -= 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 270;
    }
    if is_key_down(macroquad::input::KeyCode::D) {
        character_state.sprite_displacement.x += 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 90;
    }
```

The "0.1" value can be overwritten (not by a too large value thanks to the anti cheat). 0.9 is more than enough to go through the whole beach in less than 10s, even with the slow camera movement.
Giam v0.03 - solve 

The server implements an "anti cheat" system, which is really just a position checker. 

```c
    // Absolute value of current position - previous position > 1 ?
    // Also, has position ever been set ?
    // This might allow you to TP right after spawn
    // Or TP from the (0,0) position.
    // Fix: to handle knockback, have to authorize > 1 movement
    //      right after taking damage though
    // Not expecting the user to actually find this
    if ((fabs((*c_x) - (x)) > 1 || fabs((*c_y) - (y)) > 1)
        && (*c_x && *c_y))
                                                         
    {
        if (*knocked_back)
        {
            *knocked_back = 0;
        }
        else
        {
            send(connfd, CLIENT_POS_NOK, sizeof(CLIENT_POS_NOK), 0);
            return 1;
        }
    }
```

The quests are server sided, so it's not enough to request the flag directly from the server.

```c

                if (!(done_q1 && done_q2))
                {
                    send(connfd, GAME_NO_FLAG, sizeof(GAME_NO_FLAG), 0);
                }
                else
                {
                    send(connfd, FLAG, sizeof(FLAG), 0);
                }

[...]

            case 0xf1:
                done_q1++;
                send(connfd, Q1_ACK, sizeof(Q1_ACK), 0);
            case 0xf2:
                done_q2++;
                send(connfd, Q2_ACK, sizeof(Q2_ACK), 0);
```

The player HP is also server sided, which disallows any "hack" with this.

However, the client is the one handling the damage done to the player.

```rust
pub async fn user_take_damage(damage_taken : u8)
{
    let mut command_buffer = vec!(0x6u8);

    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
    USER_STREAM.lock().await.get(0).unwrap().write_all(&[damage_taken]).unwrap();

}
```

For the goblin quest : zero out any damage dealt by the enemies  
For the treasure quest : you can clip into the walls by moving your position 1 by 1. TPs are disallowed by the "anti cheat"

It's also possible to only send the relevant packets to the server : done_q1, done_q2, get_flag
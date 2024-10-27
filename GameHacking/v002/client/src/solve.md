The game will send a packet when the game starts

```rust
/// Sends the server the game start time
pub async fn server_send_game_start_time() 
{
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_micros();
    
    let mut command_buffer = vec!(0x2u8);
    command_buffer.extend_from_slice(&now.to_le_bytes());
    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
    // println!("wrote : {:?}", USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap());

    let reponse = read_from_stream().await;

    //println!("Server answer : {:?}", reponse);
}
```

Two possibilities to get the flag :  
    - Patch the binary or breakpoint right between the time call and the write call, and make the client send a time that is further in the future  
    - Resend the "game start" packet just before finishing the game normally

This will allow to bypass the condition to get the flag  

```c
                if ((c_start + (1000000 * TIME_TO_WIN) >= c_end)  // 30s
                    && (c_start && c_end))                        // Not 0 ;)
                {
                    send(connfd, GAME_FLAG, sizeof(GAME_FLAG), 0);
                }
                else
                {
                    send(connfd, GAME_NO_FLAG, sizeof(GAME_NO_FLAG), 0);
                }
```
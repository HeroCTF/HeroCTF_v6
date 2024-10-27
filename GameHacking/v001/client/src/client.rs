use core::str;
use std::net::{SocketAddr, TcpStream};
use std::io::{Read, Write};
use macroquad::miniquad::date;
use tokio::sync::Mutex;
use lazy_static::lazy_static;

lazy_static! {
    // Using TcpStream instead of UdpSocket
    static ref USER_STREAM: Mutex<Vec<TcpStream>> = Mutex::new(Vec::new());
}

pub async fn server_connect() -> u8 {
    let remote_addr: SocketAddr = "127.0.0.1:8080".parse().unwrap();

    // Connect to the server using TCP
    let mut stream = TcpStream::connect(&remote_addr).unwrap();

    // FAF0 -> Game ID
    // 0x.. -> Game version
    // 0xFF -> Null
    let w = stream.write(&[0xFA, 0xF0, 0x01, 0xFF]).unwrap();

    // println!("Sent {:?} bytes", w);

    // Store the TcpStream for later use
    USER_STREAM.lock().await.push(stream);

    // println!("Waiting for server response");

    let mut response_buffer = [0u8; 0x1000];
    let n = USER_STREAM
        .lock()
        .await
        .get_mut(0)
        .unwrap()
        .read(&mut response_buffer)
        .unwrap();

    let response_string = str::from_utf8(&response_buffer[..n]).unwrap();
    // println!("Received {:?} from the server", &response_string);

    if response_string.contains("ERR") {
        return 1;
    }

    0
}

pub async fn server_send_game_start_time() 
{
    // Implement as needed
    let now = date::now().to_le_bytes();
    let mut command_buffer = vec!(0x2u8, 0x8u8);
    // command_buffer.extend_from_slice(&now);
    // command_buffer.reverse();
    USER_STREAM.lock().await.get(0).unwrap().write(&command_buffer).unwrap();
}

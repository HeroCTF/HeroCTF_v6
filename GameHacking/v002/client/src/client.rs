use core::str;
use std::fs::read;
use std::net::{SocketAddr, TcpStream};
use std::io::{Read, Write};
use macroquad::miniquad::date;
use tokio::sync::Mutex;
use lazy_static::lazy_static;
use std::time::{self, SystemTime, UNIX_EPOCH};

lazy_static! {
    // Using TcpStream instead of UdpSocket
    static ref USER_STREAM: Mutex<Vec<TcpStream>> = Mutex::new(Vec::new());
}

/// Handy function to read from that magnificent static stream
pub async fn read_from_stream() -> String
{
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

    return response_string.to_string();
}

pub async fn server_connect() -> u8 {

    let remote_addr = read("./realm").unwrap();
    let remote_addr_str = String::from_utf8_lossy(&remote_addr).to_string();
    println!("Connecting to {:?}", remote_addr_str);

    // Connect to the server using TCP
    let mut stream = TcpStream::connect(&remote_addr_str).unwrap();

    // FAF0 -> Game ID
    // 0x.. -> Game version
    // 0xFF -> Null
    let w = stream.write(&[0xFA, 0xF0, 0x02, 0xFF]).unwrap();

    // println!("Sent {:?} bytes", w);

    // Store the TcpStream for later use
    USER_STREAM.lock().await.push(stream);

    // println!("Waiting for server response");

    let response_string = read_from_stream().await;
    // println!("Received {:?} from the server", &response_string);

    if response_string.contains("ERR") {
        return 1;
    }

    0
}

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

/// Sends the server the game end time
pub async fn server_send_game_end_time() 
{
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_micros();
    
    let mut command_buffer = vec!(0x3u8);
    command_buffer.extend_from_slice(&now.to_le_bytes());
    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
    // println!("wrote : {:?}", USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap());

    let reponse = read_from_stream().await;

    // println!("Server answer : {:?}", reponse);
}

pub async fn server_req_flag() -> String
{
    
    let mut command_buffer = vec!(0x4u8);
    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();

    let reponse = read_from_stream().await;

    reponse
}
use core::str;
use std::fs::read;
use std::net::{SocketAddr, TcpStream};
use std::io::{Read, Write};
use std::thread::sleep;
use macroquad::math::Vec2;
use macroquad::miniquad::date;
use tokio::runtime::Runtime;
use tokio::sync::Mutex;
use lazy_static::lazy_static;
use std::time::{self, Duration, SystemTime, UNIX_EPOCH};

lazy_static! {
    // Using TcpStream instead of UdpSocket
    static ref USER_STREAM: Mutex<Vec<TcpStream>> = Mutex::new(Vec::new());
}

lazy_static! {
    static ref LAST_SERVER_POS: Mutex<Vec2> = Mutex::new(Vec2::new(0., 0.));
}

lazy_static! {
    pub static ref NET_TASK: Mutex<Runtime> = Mutex::new(tokio::runtime::Runtime::new().unwrap());
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

    let response_string = str::from_utf8(&response_buffer[..n]).unwrap_or("\0");
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
    let w = stream.write(&[0xFA, 0xF0, 0x03, 0xFF]).unwrap();

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

pub async fn server_ping()
{
    USER_STREAM.lock().await.get(0).unwrap().write_all(&[0xFA, 0xF0, 0x02, 0xFE]).unwrap();
}

/// Sends the server the game start time
pub async fn server_send_game_start_time() 
{
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_micros();
    
    let mut command_buffer = vec!(0x2u8);
    command_buffer.extend_from_slice(&now.to_le_bytes());
    // println!("wrote : {:?}", USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap());
    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();

    let reponse = read_from_stream().await;

    // println!("Server answer : {:?}", reponse);
}

/// Sends the server the game end time
pub async fn server_send_game_end_time() 
{
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_micros();
    
    let mut command_buffer = vec!(0x3u8);
    command_buffer.extend_from_slice(&now.to_le_bytes());
    // command_buffer.reverse();
    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
}

pub async fn quest_done(quest_number: u8)
{    

    let mut command_buffer = vec!(0xf1u8 + quest_number);

    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();

    let reponse = read_from_stream().await;

    // println!("Server answer : {:?}", reponse);
}

pub async fn send_user_position(user_position : Vec2)
{
    
    if LAST_SERVER_POS.lock().await.x == user_position.x 
       && LAST_SERVER_POS.lock().await.y == user_position.y
    {
        return
    }

    let mut command_buffer = vec!(0x4u8);
    let x_u8 = user_position.x.to_le_bytes();
    let y_u8 = user_position.y.to_le_bytes();

    let mut position_u8 = Vec::new();
    position_u8.extend_from_slice(&x_u8);
    position_u8.extend_from_slice(&y_u8);
    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
    USER_STREAM.lock().await.get(0).unwrap().write_all(&position_u8).unwrap();


    let reponse = read_from_stream().await;

    // println!("Server answer : {:?}", reponse);

    *LAST_SERVER_POS.lock().await = user_position;
}

pub async fn get_user_life() -> u8
{
        let mut command_buffer = vec!(0x5u8);
        USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
    
        let reponse = read_from_stream().await;
        let new_hp = reponse.as_bytes().get(0).unwrap();

        // println!("Received new hp = {:?}", new_hp);
    
        *new_hp        

}

pub async fn user_take_damage(damage_taken : u8)
{
    let mut command_buffer = vec!(0x6u8);

    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
    USER_STREAM.lock().await.get(0).unwrap().write_all(&[damage_taken]).unwrap();

}

pub async fn server_req_flag() -> String
{
    
    let mut command_buffer = vec!(0x7u8);
    // println!("wrote : {:?}", );
    USER_STREAM.lock().await.get(0).unwrap().write_all(&command_buffer).unwrap();
    let reponse = read_from_stream().await;

    reponse
}
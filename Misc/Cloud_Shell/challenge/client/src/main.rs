use std::env;
use std::io::{self, Read, Write};
use std::os::unix::net::UnixStream;
use std::path::{Path};

const SOCKET_PATH: &str = "/dev/cloud_socket";

fn sanitize_file_name(file_path: &str) -> String {
        let path = Path::new(file_path);
    path.file_name()
        .unwrap_or_default()
        .to_string_lossy()
        .into_owned()
}

fn send_tlv_message(stream: &mut UnixStream, tlv_type: u8, value: &[u8]) -> io::Result<()> {
    let length = value.len() as u8;
    let mut message = Vec::new();
    message.push(tlv_type);
    message.push(length);
    message.extend_from_slice(value);

    stream.write_all(&message)?;
    Ok(())
}

fn receive_response(stream: &mut UnixStream) -> io::Result<String> {
        let mut size_buffer = [0u8; 8];
    stream.read_exact(&mut size_buffer)?;
    let message_size = u64::from_be_bytes(size_buffer);

        let mut buffer = vec![0; message_size as usize];
    stream.read_exact(&mut buffer)?;

    Ok(String::from_utf8_lossy(&buffer).to_string())
}

fn cloud_list() -> io::Result<()> {
    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    send_tlv_message(&mut stream, 1, &[])?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn cloud_cat(file_name: &str) -> io::Result<()> {
    let sanitized_file_name = sanitize_file_name(file_name);
    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    send_tlv_message(&mut stream, 2, sanitized_file_name.as_bytes())?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn cloud_mv(old_name: &str, new_name: &str) -> io::Result<()> {
    let sanitized_old_name = sanitize_file_name(old_name);
    let sanitized_new_name = sanitize_file_name(new_name);

    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    let mut value = Vec::new();
    value.extend_from_slice(sanitized_old_name.as_bytes());
    value.push(0);     value.extend_from_slice(sanitized_new_name.as_bytes());
    send_tlv_message(&mut stream, 3, &value)?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn cloud_create(file_name: &str, content: &str) -> io::Result<()> {
    let sanitized_file_name = sanitize_file_name(file_name);
    let mut stream = UnixStream::connect(SOCKET_PATH)?;
    let mut value = Vec::new();
    value.extend_from_slice(sanitized_file_name.as_bytes());
    value.push(0);     value.extend_from_slice(content.as_bytes());
    send_tlv_message(&mut stream, 4, &value)?;
    let response = receive_response(&mut stream)?;
    println!("{}", response);
    Ok(())
}

fn main() -> io::Result<()> {
        let program_name = env::args().next().unwrap();
    let program_name = Path::new(&program_name)
        .file_name()
        .unwrap()
        .to_string_lossy();

        let args: Vec<String> = env::args().skip(1).collect();

        match program_name.as_ref() {
        "cloud_list" => {
                        cloud_list()
        }
        "cloud_cat" => {
            if args.len() != 1 {
                eprintln!("Usage: cloud_cat <file_name>");
                return Ok(());
            }
            cloud_cat(&args[0])
        }
        "cloud_mv" => {
            if args.len() != 2 {
                eprintln!("Usage: cloud_mv <old_name> <new_name>");
                return Ok(());
            }
            cloud_mv(&args[0], &args[1])
        }
        "cloud_create" => {
            if args.len() != 2 {
                eprintln!("Usage: cloud_create <file_name> <content>");
                return Ok(());
            }
            cloud_create(&args[0], &args[1])
        }
        _ => {
            eprintln!("Méthode inconnue : {}", program_name);
            Ok(())
        }
    }
}

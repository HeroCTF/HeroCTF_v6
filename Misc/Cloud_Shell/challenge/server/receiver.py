import os
import struct
import socket

SOCKET_PATH = "/jail/dev/cloud_socket"
RESTRICTED_DIR = "/server/restricted_user"

def send_response(client_socket, message):
    message_bytes = message.encode('utf-8')
    message_length = struct.pack("!Q", len(message_bytes))
    client_socket.sendall(message_length + message_bytes)

def handle_client(client_socket):
    try:
        while True:
            tlv_type = client_socket.recv(1)
            if not tlv_type:
                break
            tlv_type = int.from_bytes(tlv_type, byteorder='big')

            length = int.from_bytes(client_socket.recv(1), byteorder='big')
            value = client_socket.recv(length).decode('utf-8')

            if tlv_type == 1:  # cloud_list
                files = os.listdir(RESTRICTED_DIR)
                response = "\n".join(files)
                send_response(client_socket, response)

            elif tlv_type == 2:  # cloud_cat
                file_path = os.path.join(RESTRICTED_DIR, value)
                if os.path.exists(file_path) and os.path.isdir(file_path) == False:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    send_response(client_socket, content)
                else:
                    send_response(client_socket, "File not found")

            elif tlv_type == 3:  # cloud_mv
                old_name, new_name = value.split('\x00')
                old_path = os.path.join(RESTRICTED_DIR, old_name)
                new_path = os.path.join(RESTRICTED_DIR, new_name)
                if os.path.exists(old_path) and os.path.isdir(old_path) == False:
                    if os.path.exists(new_path):
                        send_response(client_socket, f"File {new_path} already exists")
                    else:
                        os.rename(old_path, new_path)
                        send_response(client_socket, f"Renamed {old_name} to {new_name}")
                else:
                    send_response(client_socket, f"File {old_name} not found")

            elif tlv_type == 4:  # cloud_create
                file_name, content = value.split('\x00', 1)
                file_path = os.path.join(RESTRICTED_DIR, file_name)
                if os.path.exists(file_path) == False:
                    with open(file_path, 'w') as f:
                        f.write(content)
                    send_response(client_socket, f"File {file_name} created")
                else:
                    send_response(client_socket, f"File already exists")

    finally:
        client_socket.close()


def main():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(SOCKET_PATH)
    server_socket.listen()

    # As the socket is own by our current user, 'restricted' can't delete it
    os.chmod(SOCKET_PATH, 0o777)

    try:
        while True:
            client_socket, _ = server_socket.accept()
            handle_client(client_socket)
    finally:
        server_socket.close()
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)

if __name__ == "__main__":
    main()

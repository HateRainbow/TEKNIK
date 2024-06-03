import socket
import rsa

# Define server IP and port
server_ip = '192.168.0.106'
port = 49533

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server
    client_socket.connect((server_ip, port))  # Correctly establish connection
    print(f"Connected to server {server_ip}:{port}")

    # Receive public key from server
    public_key_data = client_socket.recv(1024)
    public_key = rsa.PublicKey.load_pkcs1(public_key_data)

    byte_digits = input('Skriv sista 4 siffror att skickas: ')  # Handle user input

    # Encrypt data using server's public key
    data_to_send = rsa.encrypt(byte_digits.encode('utf-8'), public_key)

    # Send encrypted data to server
    client_socket.send(data_to_send)
    print("Data sent successfully.")

except Exception as e:
    print("Error:", e)

finally:
    # Ensure socket is closed even in case of exceptions
    client_socket.close()
    print("Disconnected from server.")

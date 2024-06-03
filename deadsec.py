from Frames import Deadsec
from rsa import encrypt, decrypt, newkeys, pkcs1
import socket

def luhn_algorithm(pn):
    """Funktionen är en luhn algorithm som ska kontrollera att siffran"""
    pnsiffor = pn
    luhn_alg = []
    for i in range(len(pnsiffor) - 2, -1, -2):  # siffror gångrat med 2
        # om siffran över 10 blir det 1 och resten av det annars ba läggs den dublat siffra
        luhn_alg.append((int(pnsiffor[i]) * 2) % 10 + 1 if int(pnsiffor[i]) * 2 >= 10 else int(pnsiffor[i]) * 2)

    for j in range(len(pnsiffor) - 1, -1, -2):  # siffror gångrat med 1
        luhn_alg.append(int(pnsiffor[j]))

    summan = sum(luhn_alg)
    if summan % 10 != 0:
        print('Ogiltig värde')
        return False
    else:
        if summan % 10 == 0:
            return True

def gender_control(code: str) -> str:
    return 'F' if int(code[-2]) % 2 == 0 else 'M'

users = [
    {"name": "Pial", "code": "850202", "gender": "M"},
    {"name": "Isak", "code": None, "gender": "M"},
    {"name": "Mikael", "code": None, "gender": "M"},
]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.0.106'  # Update with your server IP address
port = 49533
public_key, private_key = newkeys(2048)  # Use a 2048-bit key for compatibility

# Encrypt the digits "1234" and display the length of the encrypted message
code = input("Vad är kod? ")
try:
    encrypted_message = encrypt(code.encode(), public_key)
    print(f"Encrypted message: {encrypted_message}")
    print(f"Length of encrypted message: {len(encrypted_message)} bytes")
except Exception as e:
    print(f"Encryption failed: {e}")

try:
    server_socket.bind((server_ip, port))
    server_socket.listen(1)
    print(f"Listening on {server_ip}:{port} ...")

    client_socket, client_address = server_socket.accept()

    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    encrypted_request = client_socket.recv(400)

    name = input('Vad är din namn? ').capitalize()

    try:
        find_user = next(user for user in users if user['name'] == name)  # hitta lista med användare namn
    except StopIteration:
        print(f'Namn {name}, finns inte.')
        print('Server kommer att avkopplas')
        client_socket.close()
        exit()

    try:
        control_digits = decrypt(encrypted_request, private_key).decode('utf-8')
    except pkcs1.DecryptionError as e:
        print(f"Decryption failed: {e}")
        client_socket.close()
        exit()

    user_code = find_user['code']
    user_gender = find_user['gender']

    gender = input('Vad är kön (M/F)? ').capitalize()
    
    if gender not in ["M", "F"]:
        print("Fel värde")
        client_socket.close()
        exit()

    code = user_code + str(control_digits)

    if user_gender == gender_control(code):
        if luhn_algorithm(code):
            if gender == user_gender:
                Deadsec().play_animation(fps=24)
            else:
                print('ERROR')
                print('Felaktigt kön. Server kommer att avkopplas')
                client_socket.close()
                exit()
        else:
            print('ERROR')
            print('Felaktigt kod. Server kommer att avkopplas')
            client_socket.close()
            exit()
    else:
        print('ERROR')
        print('Server kommer att avslutas')
        client_socket.close()
        exit()

except Exception as e:
    print(f"An error occurred: {e}")
    client_socket.close()
finally:
    server_socket.close()
    print("Disconnected from server.")

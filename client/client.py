 
import socket
import os
import sys

def main():
    # Беремо змінні оточення
    try:
        N = int(os.environ["COLLATZ_COUNT"])
        host = os.environ["SERVER_HOST"]     
        port = int(os.environ["SERVER_PORT"])
    except Exception as e:
        print(f"Помилка змінних оточення: {e}")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))     
        except Exception as e:
            print(f"Не вдалося підключитися до {host}:{port} → {e}")
            sys.exit(1)

        s.sendall(f"{N}\n".encode("utf-8"))    
        response = s.recv(1024).decode("utf-8").strip()
        print(f"Середня кількість кроків для 1..{N} = {response}")

if __name__ == "__main__":
    main()
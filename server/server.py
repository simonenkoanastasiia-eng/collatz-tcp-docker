import socket
import statistics

def collatz_steps(n: int) -> int:
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

def main():
    HOST = "0.0.0.0"
    PORT = 9000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        print("Сервер постійно працює на порту 9000", flush=True)
        print("Чекаю клієнтів...", flush=True)

        while True:
            conn, addr = s.accept()
            print(f"Підключено клієнта: {addr}", flush=True)

            data = conn.recv(1024).decode("utf-8").strip()

            # Якщо клієнт нічого не надіслав — просто закриваємо
            if not data:
                conn.close()
                print("Чекаю клієнтів...", flush=True)
                continue

            try:
                N = int(data)
                if N < 1:
                    raise ValueError
            except ValueError:
                conn.sendall(b"ERROR\n")
                conn.close()
                print("Чекаю клієнтів...", flush=True)
                continue

            # ← ОЦІ ДВА РЯДКИ ТОЧНО З'ЯВЛЯТЬСЯ!
            print(f"Обчислюємо середнє для 1..{N}", flush=True)
            steps_list = [collatz_steps(i) for i in range(1, N + 1)]
            avg = statistics.mean(steps_list)
            print(f"Надіслано середнє: {avg:.6f}", flush=True)

            conn.sendall(f"{avg:.6f}\n".encode())
            conn.close()
            print("Чекаю клієнтів...", flush=True)

if __name__ == "__main__":
    main()
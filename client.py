import socket
import threading
import sys

class MudClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.running = True

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Conectado al servidor MUD en {self.host}:{self.port}")
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")
            sys.exit(1)

    def receive_messages(self):
        while self.running:
            try:
                data = self.socket.recv(1024).decode("utf-8")
                if not data:
                    print("\nConexión cerrada por el servidor.")
                    self.running = False
                    break
                # mostrar el mensaje recibido
                print(f"{data}", end="", flush=True)  # Restaurar el prompt solo si hay datos nuevos
            except socket.timeout:
                # Ignorar timeouts para evitar interrupciones
                continue
            except Exception as e:
                print(f"\nError al recibir datos: {e}")
                self.running = False
                break

    def send_messages(self):
        try:
            while self.running:
                message = input()  # Mostrar un prompt para la entrada del usuario
                if message.lower() in ["salir", "exit", "quit"]:
                    print("Desconectando del servidor...")
                    self.running = False
                    self.socket.shutdown(socket.SHUT_RDWR)
                    self.socket.close()
                    break
                # Asegurarse de que el mensaje incluye un carácter de nueva línea
                self.socket.sendall((message + "\n").encode("utf-8"))
        except Exception as e:
            print(f"\nError al enviar datos: {e}")
            self.running = False

    def run(self):
        self.connect()
        # Crear un hilo para recibir mensajes del servidor
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        # Manejar el envío de mensajes desde el cliente
        self.send_messages()
        receive_thread.join()

if __name__ == "__main__":
    print("Cliente MUD Telnet")
    host = input("Introduce la dirección del servidor (por defecto: localhost): ") or "localhost"
    port = input("Introduce el puerto del servidor (por defecto: 1234): ") or 1234
    try:
        port = int(port)
    except ValueError:
        print("El puerto debe ser un número.")
        sys.exit(1)

    client = MudClient(host, port)
    client.run()
    client.run()

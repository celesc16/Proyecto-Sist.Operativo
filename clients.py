import os
import time

# Ruta del FIFO del servidor
SERVER_FIFO = "/tmp/fifo_server"
# Plantilla para la ruta del FIFO de cada cliente, usando el PID como identificador
CLIENT_FIFO_TEMPLATE = '/tmp/fifo_client_%d'

class Client:
    def __init__(self):
        # Usa el PID del proceso como ID del cliente
        self.client_id = os.getpid()
        # Crea la ruta del FIFO del cliente usando el PID
        self.client_fifo = CLIENT_FIFO_TEMPLATE % self.client_id
        # Crea el FIFO del cliente si no existe
        self.create_client_fifo()

    def create_client_fifo(self):
        # Verifica si el FIFO del cliente ya existe
        if not os.path.exists(self.client_fifo):
            # Crea el FIFO del cliente
            os.mkfifo(self.client_fifo)
            print(f"FIFO cliente {self.client_fifo} creada")
        else:
            print(f"FIFO {self.client_fifo} ya existe")

    def send_request(self, request_type, data):
        # Prepara el encabezado del mensaje con el ID del cliente y el tipo de solicitud
        header = f"client_id={self.client_id};request_type={request_type}"
        # Combina el encabezado y los datos en el mensaje
        message = f"{header}|{data}"
        # Envía el mensaje al FIFO del servidor
        with open(SERVER_FIFO, 'w') as fifo:
            fifo.write(message)
        print(f"El cliente {self.client_id} envió la solicitud: {message}")

    def receive_response(self):
        while True:
            # Lee la respuesta del FIFO del cliente
            with open(self.client_fifo, 'r') as fifo:
                response = fifo.read().strip()
                if response:
                    print(f"El cliente {self.client_id} recibió la respuesta: {response}")
                    break
            # Espera un segundo antes de volver a intentar
            time.sleep(1)

    def run(self):
        while True:
            # Solicita al usuario el tipo de solicitud
            request_type = input("Ingrese el tipo de solicitud (body-header) o 'salir' para salir: ")
            if request_type == 'salir':
                print("Cliente salió")
                break
            # Solicita al usuario los datos de la solicitud
            data = input("Introducir datos: ")
            # Envía la solicitud al servidor
            self.send_request(request_type, data)
            # Espera y muestra la respuesta del servidor
            self.receive_response()

if __name__ == "__main__":
    # Crea y ejecuta una instancia del cliente
    client = Client()
    client.run()


import os
import time

SERVER_FIFO = "/tmp/fifo_server"
CLIENT_FIFO_TEMPLATE = '/tmp/fifo_client_%d'

class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.client_fifo = CLIENT_FIFO_TEMPLATE % self.client_id
        self.create_client_fifo()

    def create_client_fifo(self):
        if not os.path.exists(self.client_fifo):
            os.mkfifo(self.client_fifo)
            print(f"FIFO cliente {self.client_fifo} creada")
        else:
            print(f"FIFO {self.client_fifo} ya existe")

    def send_request(self, request_type, data):
        request = f"{self.client_id},{request_type},{data}"
        with open(SERVER_FIFO, 'w') as fifo:
            fifo.write(request)
        print(f"El cliente {self.client_id} envió la solicitud: {request}")

    def receive_response(self):
        while True:
            with open(self.client_fifo, 'r') as fifo:
                response = fifo.read().strip()
                if response:
                    print(f"El cliente {self.client_id} recibió la respuesta: {response}")
                    break
            time.sleep(1)

    def run(self):
        while True:
            request_type = input("Ingrese el tipo de solicitud (body-header) o 'salir' para salir: ")

            if request_type == 'salir':
                print("Cliente salió")
                break
            data = input("Introducir datos: ")
            self.send_request(request_type, data)
            self.receive_response()

if __name__ == "__main__":
    client_id = os.getpid()
    client = Client(client_id)
    client.run()


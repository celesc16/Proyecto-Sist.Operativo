import os

SERVER_FIFO = "/tmp/fifo_server"
CLIENT_FIFO_TEMPLATE = '/tmp/fifo_client_%d'

class Client:
    def __init__(self):
        # Inicialización del cliente con la creación de FIFO
        self.client_id = os.getpid()
        self.client_fifo = CLIENT_FIFO_TEMPLATE % self.client_id
        self.create_client_fifo()

    def create_client_fifo(self):
        # Creación del FIFO del cliente si no existe
        if not os.path.exists(self.client_fifo):
            os.mkfifo(self.client_fifo)
            print(f"FIFO cliente {self.client_fifo} creada")
        else:
            print(f"FIFO {self.client_fifo} ya existe")

    def send_request(self, body):
        # Crear el header con client_id y la ruta del FIFO del cliente
        header = f"client_id={self.client_id};fifo_path={self.client_fifo}"
        request = f"{header}|{body}"

        # Enviar la solicitud al servidor
        with open(SERVER_FIFO, 'w') as fifo:
            fifo.write(request)
        print(f"Cliente {self.client_id} envió: {request}")

    def receive_response(self):
        # Recibir la respuesta del servidor
        with open(self.client_fifo, 'r') as fifo:
            response = fifo.read().strip()
            if response:
                print(f"Cliente {self.client_id} recibió: {response}")

    def run(self):
        while True:
            body = input("Introducir datos para el body (o 'salir' para terminar): ")
            if body.lower() == 'salir':
                print("Cliente salió.")
                break

            self.send_request(body)
            self.receive_response()

if __name__ == "__main__":
    client = Client()
    client.run()


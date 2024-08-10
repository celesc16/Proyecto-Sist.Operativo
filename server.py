import os
import time

SERVER_FIFO = "/tmp/fifo_server"
CLIENT_FIFO_TEMPLATE = '/tmp/fifo_client_%d'

class Server:
    def __init__(self):
        self.server_fifo = SERVER_FIFO
        self.sequence_number = 0
        self.create_server_fifo()

    def create_server_fifo(self):
        if not os.path.exists(self.server_fifo):
            os.mkfifo(self.server_fifo)
            print(f"FIFO {self.server_fifo} creada")
        else:
            print(f"FIFO {self.server_fifo} ya existe")

    def handle_request(self, request):
        try:
            parts = request.split(",")
            if len(parts) < 3:
                print(f"El formato es inválido: {request}")
                return
            client_id = int(parts[0])
            request_type = parts[1]
            data = parts[2] if len(parts) > 2 else ''
            client_fifo = CLIENT_FIFO_TEMPLATE % client_id
            self.sequence_number += 1

            if request_type.lower() == "body":
                response = f"Body recibido: {data}, Número de secuencia: {self.sequence_number}"

            elif request_type.lower() == "header":
                response = f"Header recibido: {data}, Número de secuencia: {self.sequence_number}"

            else:
                response = f"Tipo de solicitud desconocido: {request_type}, Número de secuencia: {self.sequence_number}"

            if os.path.exists(client_fifo):
                with open(client_fifo, 'w') as fifo:
                    fifo.write(response)
                print(f"Respuesta: '{response}' enviada al cliente: {client_id}")
            else:
                print(f"FIFO del cliente {client_id} no existe")

        except Exception as e:
            print(f"No se pudo manejar la solicitud: {e}")

    def listen(self):
        print("Servidor escuchando solicitudes...")
        while True:
            with open(self.server_fifo, 'r') as fifo:
                request = fifo.read().strip()
                if request:
                    self.handle_request(request)
            time.sleep(1)

if __name__ == "__main__":
    server = Server()
    server.listen()


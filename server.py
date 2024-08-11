import os
import time

# Ruta del FIFO del servidor para recibir solicitudes
SERVER_FIFO = "/tmp/fifo_server"
# Plantilla para la ruta del FIFO de cada cliente
CLIENT_FIFO_TEMPLATE = '/tmp/fifo_client_%d'

class Server:
    def __init__(self):
        # Inicialización del servidor con la creación de FIFO
        self.server_fifo = SERVER_FIFO
        self.create_server_fifo()

    def create_server_fifo(self):
        # Creación del FIFO del servidor si no existe
        if not os.path.exists(self.server_fifo):
            os.mkfifo(self.server_fifo)
            print(f"FIFO {self.server_fifo} creada")
        else:
            print(f"FIFO {self.server_fifo} ya existe")

    def handle_request(self, request):
        try:
            # Se espera que el mensaje esté en formato "header|body"
            header, body = request.split('|', 1)

            # Procesar el header para obtener la información
            header_data = {}
            for part in header.split(';'):
                key, value = part.split('=', 1)
                header_data[key] = value

            client_id = int(header_data.get("client_id", -1))
            client_fifo = header_data.get("fifo_path", "")

            # Validar que el header contenga la información necesaria
            if client_id == -1 or not client_fifo:
                print("Header incompleto o incorrecto")
                return

            # Mostrar la información almacenada en el servidor
            print(f"Guardado en header: {header_data}")
            print(f"Guardado en body: {body}")

            # Responder al cliente con la misma información
            response = f"Header guardado: {header_data} y  Body guardado: {body}"
            if os.path.exists(client_fifo):
                with open(client_fifo, 'w') as fifo:
                    fifo.write(response)
                print(f"Respuesta enviada al cliente {client_id}: {response}")
            else:
                print(f"FIFO del cliente {client_id} no existe")

        except Exception as e:
            print(f"Error al manejar la solicitud: {e}")

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


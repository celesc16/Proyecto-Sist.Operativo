import os

class Client:
    def __init__(self, fifo_path):
        self.fifo_path = fifo_path
        self.response_fifo_path = response_fifo_path

    def send_messaje(self, messaje):
        if not os.path.exists(self.fifo_path):
            raise FileNotFoundError(f"El FIFO no se ha encontrado en la ruta: {self.fifo_path}")
        
        with open(self.fifo_path, 'w') as fifo:
            fifo.write(messaje)
            print(f"Cliente envio: {messaje}")

    def receive_response(self):
        with open(self.response_fifo_path, 'r') as fifo:
            response = fifo.read().strip()
            print(f"Customer received: {response}")
            return response

if __name__ == "__main__":
    fifo_path = "/tmp/fifo_server"
    client = Client(fifo_path, response_fifo_path)

    messaje = "ricuet"
    client.send_messaje(messaje)
    response = client.receive_response()

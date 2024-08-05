import os

class Client:
    def __init__(self, fifo_path, response_fifo_path): 
        self.fifo_path = fifo_path
        self.response_fifo_path = response_fifo_path

    def send_message(self, message): 
        if not os.path.exists(self.fifo_path):
            raise FileNotFoundError(f"El FIFO no se ha encontrado en la ruta: {self.fifo_path}")

        with open(self.fifo_path, 'w') as fifo:
            fifo.write(message)
            print(f"Cliente envió: {message}")

    def receive_response(self):
        with open(self.response_fifo_path, 'r') as fifo:
            response = fifo.read().strip()
            print(f"Cliente recibió: {response}")
            return response

if __name__ == "__main__":
    fifo_path = "/tmp/fifo_server"
    response_fifo_path = "/tmp/fifo_response"
    client = Client(fifo_path, response_fifo_path)

    message = "ricuet"
    client.send_message(message)  
    response = client.receive_response()

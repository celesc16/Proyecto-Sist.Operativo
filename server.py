
import os 
import time

class Server:
    def __init__(self):
        self.fifo_path = "/tmp/fifo_server"
        self.create_fifo()

    def create_fifo(self):
        if not os.path.exists(self.fifo_path):
            os.mkfifo(self.fifo_path)
            print(f"fifo {self.fifo_path} creada")
        else:
            print(f"fifo {self.fifo_path} ya existe")

    def listen(self):
        print("Servidor esperando mensaje...")
        with open(self.fifo_path, 'r') as fifo:
            while True:
                data = fifo.read().strip()
                if data:
                    print(f"Servidor recibio: data")
                    response = self.process_request(data)
                    self.respond_to_client(response)

    def procces_request(self,response):
        if request.lower() == "ricuet":
            return "Hola! Request recibido!. Como puedo ayudarte?"
        else:
            return " Lo siento!, no se puedo procesar tu solicitud"

    def respond_to_client(self,response):
        with open(self.fifo_path, 'w' ) as fifo:
            fifo.write(response)
            print(f"Respuesta enviada al cliente : {response}")

if __name__ == "__main__":
        server = Server()
        server.listen() 

import os

class Customer:
    def __init__(self, fifo_path):
        self.fifo_path = fifo_path

    def enviar_mensaje(self, mensaje):
        if not os.path.exists(self.fifo_path):
            raise FileNotFoundError(f"No se encontró la FIFO en la ruta: {self.fifo_path}")
          
        with open(self.fifo_path, 'w') as fifo:
            fifo.write(mensaje)
            print(f"Cliente envió: {mensaje}")

if __name__ == "__main__":
    fifo_path = "/tmp/fifo_server"
    customer = Customer(fifo_path)

    mensaje = "ricuet"
    customer.enviar_mensaje(mensaje)

import os

class Customer:
    def __init__(self, fifo_path):
        self.fifo_path = fifo_path

    def send_messaje(self, messaje):
        
        if not os.path.exists(self.fifo_path):
            raise FileNotFoundError(f"The FIFO was not found in the path: {self.fifo_path}")
        
        with open(self.fifo_path, 'w') as fifo:
            fifo.write(messaje)
            print(f"Customer sended: {messaje}")

if __name__ == "__main__":
    fifo_path = "/tmp/fifo_server"
    customer = Customer(fifo_path)

    messaje = "ricuet"
    customer.send_messaje(messaje)

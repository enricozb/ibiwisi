import socket
import time


class Connection:
    message_length = 2048

    def __init__(self, port):
        self.port = port

        print(f'listening on port {port}')
        self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_recv.bind(('', self.port))
        self.sock_recv.listen(200)

        self.client_sock = None

    def set_sink(self, addr):
        print(f"Attempting to connect :{self.port} to {addr}")
        while True:
            try:
                self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock_send.connect(addr)
                print("SUCCESS")
                return
            except:
                print(".", end="", flush=True)
                self.sock_send.close()
                time.sleep(1)

    def send(self, mssg):
        if type(mssg) is str:
            mssg = bytes(mssg, 'utf-8')

        header = bytes(f'{len(mssg):016d}', 'utf-8')
        self.sock_send.sendall(header + mssg)

    def recv(self):
        if self.client_sock is None:
            self.client_sock, _ = self.sock_recv.accept() 
        size = int(self.client_sock.recv(16))
        
        chunks = []
        while size > 0:
            chunk_len = min(size, self.message_length)
            mssg = self.client_sock.recv(chunk_len)
            chunks.append(mssg)
            size -= len(mssg)

        return b''.join(chunks)

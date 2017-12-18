import socket
import time


class Connection:
    message_length = 2048

    def __init__(self, port):
        self.port = port

        print(f'listening on port {port}')
        self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_recv.bind(('localhost', self.port))
        self.sock_recv.listen(200)

        self.client_sock = None

    def set_sink(self, addr):
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for i in range(5):
            try:
                self.sock_send.connect(addr)
                return
            except:
                time.sleep(1)
                print(f"Failed to connect to sink {addr}, {4 - i} tries left")
        else:
            raise Exception(f"Failed to connect to sink {addr}")

    def send(self, mssg):
        if type(mssg) is str:
            mssg = bytes(mssg, 'utf-8')

        print(f'sending message of size {len(mssg)} bytes')
        header = bytes(f'{len(mssg):016d}', 'utf-8')
        self.sock_send.send(header + mssg)

    def recv(self):
        print('listening...')
        if self.client_sock is None:
            self.client_sock, _ = self.sock_recv.accept() 
        size = int(self.client_sock.recv(16))
        print(f'recieving message of size {size}')
        
        chunks = []
        while size > 0:
            chunks.append(self.client_sock.recv(min(size, self.message_length)))
            size -= self.message_length

        return b''.join(chunks)

import socket


class WazzupClient:
    def __init__(self, server_port=50007, server_host='localhost'):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        message = 'Wazzup!'
        self.client_socket.send(message)
        data = self.client_socket.recv(1024)
        print 'Client received: ', data

    def stop(self):
        self.client_socket.close()
        print 'client socket is closed'


if __name__ == '__main__':
    client = WazzupClient()

    client.start()
    client.stop()

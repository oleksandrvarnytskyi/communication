import socket
import thread


class EchoServer(object):
    def __init__(self, port=50007):
        self.host = ''
        self.port = port
        self.can_run = False
        self.socket_object = None

    def is_running(self):
        return self.can_run

    @staticmethod
    def handle_connection(connection, address):
        while True:
            data = connection.recv(1024)
            if not data or data == 'disconnect\r\n':
                break
            connection.send(b'Echo=> ' + data)
        connection.close()
        print 'Connection with ' + address[0] + ' : ' + str(address[1]) \
              + ' is closed'

    def start(self):
        self.can_run = True
        # print self.is_running()
        self.socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_object.bind((self.host, self.port))
        self.socket_object.listen(5)
        while self.can_run:
            try:
                connection, address = self.socket_object.accept()
                print 'Server connected by', address
                thread.start_new_thread(self.handle_connection,
                                        (connection, address))
            except KeyboardInterrupt:
                self.can_run = False
                break

    def stop(self):
        self.socket_object.close()
        self.can_run = False


if __name__ == '__main__':
    server = EchoServer()

    print server.is_running()
    print server.port

    server.start()
    # print server.is_running()
    server.stop()
    print server.is_running()

    # server = EchoServer(54321)
    # print server.is_running()
    # print server.port
    #
    # server.start()
    # server.stop()
    # print server.is_running()

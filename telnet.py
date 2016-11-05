import httplib


class Telnet(object):
    def __init__(self, server_port=8080):
        self.server_port = server_port
        self.client_socket = None
        self.can_run = True

    def start(self):
        command = raw_input('input command (ex. GET /index.html HTTP/1.1): ')
        server_host = raw_input('HOST: ')
        conn = httplib.HTTPConnection(server_host, self.server_port)
        while self.can_run:
            command = command.split()
            if command[0] == 'exit':
                break
            conn.request(command[0], command[1])
            response = conn.getresponse()
            data_received = response.read()
            print(data_received)
            self.can_run = False
        conn.close()


if __name__ == '__main__':
    client = Telnet()

    client.start()

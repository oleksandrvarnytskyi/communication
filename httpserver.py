from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import time
import os

""" http://localhost:8080/index.html """

DIR_WITH_FILE_CONFIG = '/Users/savar/PycharmProjects/junior/communication/' \
                       'vars/www/localhost/'


def configuring():
    conf_dict = {}
    with open(DIR_WITH_FILE_CONFIG + 'http.conf') as file_conf:
        for line in file_conf:
            items = line.split()
            if items:
                conf_dict[items[0]] = ' '.join(items[1:])
    return conf_dict


def mime_types():
    mime_dict = {}
    with open(DIR_WITH_FILE_CONFIG + 'mime.types') as file_mime:
        for line in file_mime:
            parts = line.split()
            if parts:
                mime_dict[parts[0]] = ' '.join(parts[1:])
    return mime_dict

MIME_DICT = mime_types()
CONFIG_INFO = configuring()
PORT = int(CONFIG_INFO['port'])
HOST = CONFIG_INFO['address']
ROOT_DIR = CONFIG_INFO['root_dir']


class HttpHandler(BaseHTTPRequestHandler, object):
    def do_GET(self):
        self.respond()
        return

    def parse_request(self):
        self.request_version = version = "HTTP/0.9"
        request_line = self.raw_requestline
        if request_line[-2:] == '\r\n':
            request_line = request_line[:-2]
        elif request_line[-1:] == '\n':
            request_line = request_line[:-1]
        self.requestline = request_line
        words = request_line.split()
        if len(words) == 3:
            command, path, version = words
            if version[:5] != 'HTTP/':
                self.send_error(400, "Bad request version (%s)" % version)
                return False
            if command != 'GET':
                self.send_error(405, "Method Not Allowed (%s)" % command)
                return False
        elif len(words) == 2:
            command, path = words
            if command != 'GET':
                self.send_error(405, "Method Not Allowed (%s)" % command)
                return False
        else:
            self.send_error(400, "Bad request syntax (%s)" % request_line)
            return False
        self.command, self.path, self.request_version = command, path, version
        self.headers = self.MessageClass(self.rfile, 0)
        return True

    def send_error(self, code, message=None):
        try:
            short, along = self.responses[code]
        except KeyError:
            short, along = '???', '???'
        if not message:
            message = short
        explain = along
        self.log_error("code %d, message %s", code, message)
        self.send_response(code, message)
        self.end_headers()
        self.wfile.write(self.error_message_format %
                         {'code': code,
                          'message': message,
                          'explain': explain})

    @staticmethod
    def set_mimetype(path):
        for key in MIME_DICT:
            if path.endswith(key):
                mime_type = MIME_DICT[key]
                break
        else:
            mime_type = 'application/octet-stream'
        return mime_type

    def path2open(self):
        path = self.path
        if self.path == '/' or self.path == '/index.html':
            path = 'index.html'
        try:
            file2open = open(path)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
            return None, None
        return file2open, path

    def respond(self):
        file2read, file_name = self.path2open()
        if file2read:
            self.send_header('', '')
            self.send_response(200)
            self.send_header('Connection', 'close')
            fs = os.fstat(file2read.fileno())
            self.send_header("Content-Length", str(fs[6]))
            mimetype = self.set_mimetype(file_name)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(file2read.read())
            file2read.close()
            return
        else:
            self.send_header('', '')
            self.send_response(204)
            self.send_header('Connection', 'close')
            self.send_header("Content-Length", 'None')
            self.send_header('Content-type', 'None')
            self.end_headers()
            return


if __name__ == '__main__':
    os.chdir(ROOT_DIR)
    http_server = HTTPServer((HOST, PORT), HttpHandler)
    print time.asctime(), 'Http server starts - %s : %s' % (HOST, PORT)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    http_server.server_close()
    print time.asctime(), 'Http server stops - %s : %s' % (HOST, PORT)


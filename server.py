import socket
import re

def mimetype(content):
    if content.endswith('.css'):
        return 'text/css'
    if content.endswith('.html'):
        return 'text/html'
    if content.endswith('jpg'):
        return 'image/jpg'
    if content.endswith('png'):
        return 'image/png'
    if content.endswith('.js'):
        return 'text/javascript'
    if content.endswith('.ttf'):
        return 'font/ttf'

def listening(server):
    while True:
        connection, address = server.accept()
        print(f'Receive request from {address}')
        request = connection.recv(1024).decode('utf-8')
        request = request.split(' ')
        method, content = request[0], request[1].lstrip('/')

        if method == 'GET':
            if content == '': content = 'index.html'
            try:
                ifile = open(content, 'rb')
                header = 'HTTP/1.1 200 OK Content-Type: ' + mimetype(content) + '\n\n'
            except:
                ifile = open('404.html', 'rb')
                header = 'HTTP/1.1 404 Not Found \n\n'

        if method == 'POST':
            data = re.split('=|&', request[-1])
            username, password = data[1], data[3]
            if username == 'admin' and password == 'admin':
                ifile = open('info.html', 'rb')
                header = 'HTTP/1.1 200 OK Content-Type: text/html \n\n'
            else:
                ifile = open('index.html', 'rb')
                header = 'HTTP/1.1 200 OK Content-Type: text/html \n\n'
 
        response = header.encode('utf-8') + ifile.read()
        ifile.close()
        connection.send(response)
        connection.close()

def main():
    ip, port = '127.0.0.1', 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen()
    print(f'Server is listening at {ip}:{port}')
    listening(server)


if __name__ == "__main__":
    main()
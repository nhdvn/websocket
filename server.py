import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((socket.gethostname(), 8080))
server.listen()

while True:
    connection, address = server.accept()
    print(f"[LISTENING] {address}")
    request = connection.recv(1024).decode('utf-8')
    request = request.split(' ')
    method, page = request[0], request[1].lstrip('/')

    if page == '': page = 'index.html'

    try:
        file = open(page, 'rb')
        response = file.read()
        file.close()

        if page.endswith('.css'):
            mimetype = 'text/css'
        elif page.endswith('.jpg'):
            mimetype = 'image/jpg'
        else: 
            mimetype = 'text/html'

        header = 'HTTP/1.1 200 OK \n'
        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except:
        header = 'HTTP/1.1 404 Not Found \n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
 

    print(type(response))
    final_response = header.encode('utf-8') + response
    connection.send(final_response)
    connection.close()
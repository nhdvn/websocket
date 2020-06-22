import socket, json, re, os, sys

global login 
login = False

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
    if content.endswith('.py'):
        return 'text/x-python'    
    if content.endswith('.ttf'):
        return 'font/ttf'
    if content.endswith('.txt'):
        return 'text/txt'
    if content.endswith('.pdf'):
        return 'text/pdf'


def loopdir(ifile, path):
    files = os.listdir(path)
    for name in sorted(files):
        if name == '.git': continue
        folder = path + '/' + name
        if os.path.isdir(folder):
            ifile.write(f'<li class="folder">{name}')
            ifile.write('<ul>')
            loopdir(ifile, folder)
            ifile.write('</ul>')
            ifile.write('</li>')
        else:
            ifile.write('<li>')
            ifile.write(f'<a href="{path}/{name}">{name}</a>')
            ifile.write('</li>')
            


def render():
    with open('files.html', 'w') as ifile:
        ifile.write('<html>')
        ifile.write('<head>')
        ifile.write('<title>Files</title>')
        ifile.write('<link rel="stylesheet" type="text/css" href="css/files.css">')
        ifile.write('</head>')

        ifile.write('<body>')
        ifile.write('<h2>Directory List</h2>')
        ifile.write('<div class="box">')
        ifile.write('<ul class="directory-list">')
        loopdir(ifile, '.') # or ./sharing
        ifile.write('</ul>')
        ifile.write('</div>')
        ifile.write('</body>')
        ifile.write('</html>')
    ifile.close()


def parse(request):
    request = request.split(' ')
    method = request[0]
    content = request[1].lstrip('/')
    exist = request[-1].find('{')
    if exist != -1:
        data = request[-1][exist:]
    else:
        data = None
    try:
        data = json.loads(data)
    except:
        data = None
    print(method, content)
    return method, content, data


def handle(client):
    global login 
    request = client.recv(1024).decode('utf-8')
    method, content, data = parse(request)

    if method == 'POST' and content == 'login':
        if data['user'] == 'admin' and data['pswd'] == 'admin':
            login = True
        header = 'HTTP/1.1 200 OK Content-Type: application/json \n\n'
        return header.encode('utf-8') + json.dumps(login).encode('utf-8')

    if method == 'GET' and content == 'info.html':
        if login == True:
            ifile = open('info.html', 'rb')
        else:
            ifile = open('index.html', 'rb')
        header = 'HTTP/1.1 200 OK Content-Type: text/html \n\n'
        return header.encode('utf-8') + ifile.read()

    if method == 'GET' and content == 'files.html':
        ifile = open('files.html', 'rb')
        header = 'HTTP/1.1 200 OK Content-Type: text/html \n\n'
        return header.encode('utf-8') + ifile.read()

    if method == 'GET':
        if content == '': content = 'index.html'
        try:
            ifile = open(content, 'rb')
            header = 'HTTP/1.1 200 OK Content-Type: ' + mimetype(content) + '\n\n'
        except:
            ifile = open('404.html', 'rb')
            header = 'HTTP/1.1 404 Not Found \n\n'
        return header.encode('utf-8') + ifile.read()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080))
    server.listen()

    print('Server is listening at 127.0.0.1:8080')

    while True:
        client, port = server.accept()
        print('Establish connection from', port, end = ' ')
        response = handle(client)
        client.send(response)
        client.close()


if __name__ == "__main__": 
    render()
    main()
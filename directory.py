import os

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
        loopdir(ifile, './sharing')
        ifile.write('</ul>')
        ifile.write('</div>')
        ifile.write('</body>')
        ifile.write('</html>')
    ifile.close()


render()



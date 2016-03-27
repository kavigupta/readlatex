
from os import makedirs, chdir, system, remove
from os.path import exists, basename, dirname, abspath, join
from shutil import copyfile, copytree, rmtree
from sys import argv

script_location = abspath(argv[0])
backup_location = join(dirname(script_location), 'backup')

def readlatex(path):
    dobackups(path)
    movetopath(path)
    getsty()
    for dogetheight in True, False:
        addusepackage(path, dogetheight)
        runpdflatex(path)
        restore_original_file(path)
    remove('readlatex.sty')
    rmbackups()


def addusepackage(path, dogetheight):
    getheight = '[get]' if dogetheight else ''
    lines = []
    with open(path, 'r') as f:
        for line in f:
            lines.append(line)
            if r'\documentclass' in line:
                lines.append('\\usepackage' + getheight + '{readlatex}\n')
    with open(path, 'w') as f:
        for line in lines:
            f.write(line)

def runpdflatex(path):
    for _ in range(3):
        system('pdflatex ' + basename(path))

def getsty():
    location = join(dirname(script_location), 'readlatex.sty')
    copyfile(location, 'readlatex.sty')

def dobackups(path):
    movetosrc()
    copytree(dirname(path), backup_location)

def restore_original_file(path):
    copyfile(join(backup_location, basename(path)), path)

def rmbackups():
    rmtree(backup_location)

def movetosrc():
    movetopath(script_location)

def movetopath(path):
    chdir(dirname(path))

def create_if_not_exists(directory):
    if not exists(directory):
        makedirs(directory)

readlatex(abspath(argv[1]))
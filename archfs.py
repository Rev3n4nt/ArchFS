# Python 3.x
# encoding="utf-8"
# terminal based script
# Search Archive & Folder with same name in given path
# for windows OS better run with admin rights to write results (cmd)
# or simply run archfs.py file in folder (open file)
# Author: Farid Kemyakov aka Rev3n4nt
# CoAuthor: Aziz Kemyakov aka DoomStal
import sys
import re
from os import stat, listdir, path

# Add here path where to skip search:
skip = [
r'C:/windows',
r'C:/Program Files',
r'C:/Program Files (x86)',
]

# add here archive extentions:
extensions = [
'.zip',
'.7z',
'.rar',
'.tar.gz', # complicated must be higher than normals
'.tar',
'.gz',
]

# Result will be written here:
output = open('result.txt', 'w')

skip = [ re.compile(raw, re.IGNORECASE) for raw in skip ]

archives = dict()
dirs_all = dict()

_print_r = 0
def print_r(str):
    global _print_r
    sys.stdout.write('\b'*_print_r)
    sys.stdout.write(' '*_print_r)
    sys.stdout.write('\r')
    sys.stdout.write(str)
    _print_r = len(str)

def walk(cwd, depth=0):
    #if depth > 2:
     #   return

    try:
        all = [cwd+'/'+f for f in listdir(cwd)]
    except WindowsError:
        print('no access to '+cwd+'\n')
        return

    name = path.splitext( path.basename(cwd.lower()) )[0]
    if name not in dirs_all:
        dirs_all[name] = []
    dirs_all[name].append(cwd)
    print_r(cwd)

    files = [f for f in all if path.isfile(f)]
    for f in files:
        ext = next( (x for x in extensions if f.endswith(x)), None)
        if( ext ):
            name = path.basename(f.lower())[:-len(ext)]
            if name not in archives:
                archives[name] = []
            archives[name].append(f)
            print_r('archive found '+name+'\n')
            print_r('              '+f+'\n')

    dirs = [f for f in all if path.isdir(f)]
    for d in dirs:
        if( any( reg.match(d) for reg in skip ) ):
            print_r('skipped '+d+'\n')
            continue
        walk(d, depth+1)

# Add here path to search:
walk('D:/Games')
# walk('D:/DEV')

print_r('searching matches\n')

for d in sorted(dirs_all):
    if d in archives:
        print('\n***** archives ********')
        output.write('\n***** archives ********\n')
        for f in archives[d]:
            st = stat(f)
        print(str(st.st_size)+''+f)
        output.write(str(st.st_size/1048576)+' mb\n '+f+'\n')
        print('\n***** directories *****')
        output.write('\n***** directories *****\n')
        for f in dirs_all[d]:
            print(f)
            output.write(f+'\n')
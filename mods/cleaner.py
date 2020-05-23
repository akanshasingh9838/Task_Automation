import os
from path import Path

def delete_file(DIRECTORY,filename):
    d = Path(DIRECTORY)
    #replace directory with your desired directory
    for i in d.walk():
        if i.isfile():
            if i.name == filename:
                i.remove()
        

def delete_file_by_extension(DIRECTORY, extension= "*.pyc"):
    d = Path(DIRECTORY)
    files = d.walkfiles(extension)
    for file in files:
        file.remove()


def delete_file_by_size(d,bigger_tha_size = 5 *1024*1024):
    del_size = bigger_tha_size
    for i in d.walk():
        if i.isfile():
            if i.size > del_size:
                i.remove() 

def temp_file_removal(DIRECTORY,extras=[]):
    extensions = ['.—','~$*.doc','.000','.001','.bak',
                    '.bk!','.chk','.fts','.gid','.log',
                    '.old','.prv','.tmp','.wbk']
    if extras:
        extensions.extend(extras)
    for ext in extensions:
        delete_file_by_extension(DIRECTORY,ext)
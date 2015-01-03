from ftplib import FTP
from os import walk
from os import sep
from itertools import takewhile

__author__ = 'OTymchenko'

passive_mode = True
login = 'beedevs_ftp'
psswrd = ''
remoteFolder = 'beedevs.com/www'
host = 'beedevs.ftp.ukraine.com.ua'

# only for root directories and files
excluded = []
rootFolder = '.'


def run():
    ftp = ftp_connect(host, login, psswrd, remoteFolder, passive_mode)

    clear_folder(ftp)

    if ftp:
        for (dirpath, dirnames, filenames) in walk(rootFolder):

            smpdirpath = '.' + dirpath[len(rootFolder):]

            ftp.cwd('/'+remoteFolder)

            isExcluded = False
            if not (dirpath == '.' or dirpath == '..'):

                for excludedPath in excluded:
                    fullPath = rootFolder + sep + excludedPath
                    if dirpath[:len(fullPath)] == fullPath:
                        isExcluded = True
                        break

                if isExcluded:
                   continue

                ftp.cwd(smpdirpath.replace(sep, '/'))

            if dirnames and len(dirnames) > 0:
                for dir in dirnames:
                    if dir in excluded:
                        continue
                    ftp.mkd(dir)

            if filenames and len(filenames) > 0:
                for fileName in filenames:
                    if fileName in excluded:
                        continue
                    ftp_send_file(ftp, open_file(dirpath+sep+fileName))

        ftp.quit()


## FTP procedures
def ftp_connect(host, login, psswrd, remoteFolder = None, passive_mode = True):
    ftp = FTP(host, login, psswrd)
    ftp.set_pasv(passive_mode)
    if remoteFolder:
        ftp.cwd('/'+remoteFolder)
    return ftp

def ftp_ls(ftp):
    ftp.retrlines('LIST')

def ftp_send_file(ftp, file):
    ftp.storbinary("STOR "+file.name, file)

def clear_folder(ftp):

    genRes = ftp.mlsd()

    for item in takewhile(lambda x: x is not None, genRes):
        name = item[0]

        if name == '.' or name == '..':
            continue

        data = item[1]
        isDir = False
        if data:
            isDir = data['type'] == 'dir'

        if isDir:
            ftp.cwd(name)
            clear_folder(ftp)
            ftp.cwd('..')
            ftp.rmd(name)
        else:
            ftp.delete(name)


## data procedures
def open_file(fileName):
    return open(fileName, 'r+b')

run()
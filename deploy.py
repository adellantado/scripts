from ftplib import FTP
from os import walk
from os import sep

__author__ = 'OTymchenko'

# TODO: root folder edit
# remove everything at once and refill folder
# exclude files


passive_mode = True
login = 'beedevs_ftp'
psswrd = 'xxxxxxx'
remoteFolder = 'beedevs.com/www'
host = 'beedevs.ftp.com.ua'

# only for root directories
excluded = ['.git']


def run():
    ftp = ftp_connect(host, login, psswrd, remoteFolder, passive_mode)
    if ftp:

        folder = '.'
        for (dirpath, dirnames, filenames) in walk(folder):

            ftp.cwd('/'+remoteFolder)

            isExcluded = False
            if not (dirpath == '.' or dirpath == '..'):

                for excludedPath in excluded:
                    fullPath = folder + sep + excludedPath
                    if dirpath[:len(fullPath)] == fullPath:
                        isExcluded = True
                        break

                if isExcluded:
                   continue

                ftp.cwd(dirpath.replace(sep, '/'))

            folders = ftp.nlst()
            if dirnames and len(dirnames) > 0:
                for dir in dirnames:

                    if dir in excluded:
                        continue


                    if not dir in folders:
                        ftp.mkd(dir)

            if filenames and len(filenames) > 0:
                for fileName in filenames:
                    ftp_send_file(ftp, open_file(dirpath+sep+fileName))

        ftp.quit()


## FTP procedures
def ftp_connect(host, login, psswrd, remoteFolder = None, passive_mode = True):
    ftp = FTP(host, login, psswrd)
    ftp.set_pasv(passive_mode)
    if remoteFolder:
        ftp.cwd(remoteFolder)
    return ftp

def ftp_ls(ftp):
    print(ftp.retrlines('LIST'))

def ftp_send_file(ftp, file):
    ftp.storbinary("STOR "+file.name, file)


## data procedures
def open_file(fileName):
    return open(fileName, 'r+b')

run()
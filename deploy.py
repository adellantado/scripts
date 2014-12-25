from ftplib import FTP

__author__ = 'OTymchenko'

passive_mode = True
login = ''
psswrd = ''
remoteFolder = ''
host = ''


def run():
    ftp = ftpConnect()
    if ftp:
        ftpSend(readFolder())
        ftp.quit()


def ftpConnect(host, remoteFolder, login, psswrd, passive_mode = True):
    ftp = FTP(host, login, psswrd)
    ftp.set_pasv(passive_mode)
    ftp.cwd(remoteFolder)
    return ftp


def ftpSend(ftp, folder):
    for file in folder:
        ftp.storbinary("STOR "+file.name, file)


def readFolder(folder):
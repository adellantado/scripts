from ftplib import FTP

__author__ = 'OTymchenko'


def run():
    ftp = ftpConnect()
    if ftp:
        ftpSend(readFolder())
        ftp.quit()


def ftpConnect(host, initFolder, login, psswrd):
    ftp = FTP(host, login, psswrd)
    ftp.cwd(initFolder)
    ftp.retrlines('LIST')
    ftp.retrbinary('RETR README', open('README', 'wb').write)
    return ftp


def ftpSend(ftp):
    ftp


def readFolder(folder):
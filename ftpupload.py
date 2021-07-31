import glob
import ftplib
import os
import ntpath
import time
import configparser


def transfer_file(file):
    config = configparser.ConfigParser()
    config.read('trapcam.ini')
    hostname = config['ftpupload']['hostname']
    user = config['ftpupload']['user']
    password = config['ftpupload']['password']
    folder = config['ftpupload']['folder']
    session = ftplib.FTP(hostname, user, password)
    try:
        for f in folder.split('/'):
            session.cwd(f)
        return session.storbinary('STOR {0}'.format(ntpath.basename(file.name)), file).startswith('226')
    finally:
        session.quit()


def open_and_transfer_file(filename):
    file = open(filename, 'rb')
    try:
        return transfer_file(file)
    finally:
        file.close()


while(True):
    try:
        files = glob.glob("*.avi")
        for filename in files:
            if filename.find("part") == -1:
                if open_and_transfer_file(filename):
                    print("File transferred:", filename)
                    os.remove(filename)
    except Exception as ex:
        print("Error:", ex)
    time.sleep(5)

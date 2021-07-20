import glob
import ftplib
import os
import ntpath
import time

def transfer_file(file):
    session = ftplib.FTP('192.168.1.1','admin','admin')
    try:
        session.cwd('volume(sda1)')
        session.cwd('trapcam')
        return session.storbinary('STOR {0}'.format(ntpath.basename(file.name)), file).startswith('226')
    except:
        return False
    finally:
        session.quit()

def open_and_transfer_file(filename):
    file = open(filename,'rb')
    try:
        return transfer_file(file)
    except:
        return False;
    finally:
        file.close()
                      
while(True):
    try:
        files = glob.glob("/tmp/trapcam/*.avi")
        for filename in files:
            if filename.find("part") == -1:
                if open_and_transfer_file(filename):
                    print("File transferred:", filename)
                    os.remove(filename)
    except Exception as ex:
        print("Error:", ex)
    time.sleep(5)

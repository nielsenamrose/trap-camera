import glob
import ftplib
import os
import ntpath
import time

code = None

while(True):
    files = glob.glob("./video/*full.avi")
    if len(files) > 0:
        session = ftplib.FTP('192.168.1.1', 'admin', 'admin')
        session.cwd('volume(sda1)')
        session.cwd('trapcam')
        for filename in files:
            file = open(filename, 'rb')                  # file to send
            code = session.storbinary('STOR {}'.format(
                ntpath.basename(filename)), file)     # send the file
            print(code)
            file.close()
            if code.find('226') > -1:
                os.remove(filename)              # close file and FTP
        session.quit()
    time.sleep(5)

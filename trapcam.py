import glob
import cv2
import numpy as np
from datetime import datetime
import time
import os
import sys


def rename_part_files():
    files = glob.glob("*part.avi")
    for filename in files:
        os.rename(filename, filename.replace("part.avi", ".avi"))


def remove_part_files():
    files = glob.glob("*part.avi")
    for filename in files:
        os.remove(filename)


def calculate_moment(frame, reference):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    if reference is None:
        return blur, 0
    diff = cv2.absdiff(reference, blur)
    thresh = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5, 5), 'uint8')
    dilate = cv2.dilate(thresh, kernel, 2)
    return blur, cv2.moments(dilate)['m00']


def imprint_datetime(now, d, moment, frame):
    str = "{0} {1} {2}".format(now, d, moment)
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    cv2.putText(frame, str, (0, 470), font, 0.5, color, 1, cv2.LINE_AA)


def start_recording(now, frame_rate):
    filename = '{0}part.avi'.format(now.strftime("%Y-%m-%d_%H-%M-%S"))
    print('start recording video file:', filename)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, frame_rate, (640,  480))
    return out


def stop_recording(out, proved):
    print('stop recording')
    out.release()
    if proved:
        rename_part_files()
    else:
        remove_part_files()


def capture(cap):
    reference = None
    d = 0
    started = False
    proved = False
    out = None
    try:
        while(1):
            ok, frame = cap.read()
            #cv2.imshow('capture', frame)
            if not ok:
                print("Failded to capture frame")
                break
            else:
                now = datetime.now()

                reference, moment = calculate_moment(frame, reference)
                imprint_datetime(now, d, moment, frame)
                print("{0} {1}".format(d, moment))

                if moment > 50000:
                    d = min(d + 10, 100)
                    if not started:
                        out = start_recording(now, 8)
                        started = True
                        proved = False
                    if d == 100:
                        proved = True
                else:
                    d = max(d - 3, 0)
                    if d == 0 and started:
                        stop_recording(out, proved)
                        started = False

                if started:
                    out.write(frame)
    finally:
        if started:
            stop_recording(out, proved)


def start():
    rename_part_files()
    cap = cv2.VideoCapture(0)
    try:
        capture(cap)
    finally:
        cap.release()


while True:
    try:
        start()
    except Exception as ex:
        print("Error:", ex)
        # cv2.destroyAllWindows()
    time.sleep(5)

import glob
import cv2
import numpy as np
from datetime import datetime
import time
import os

def rename_part_files():
    files = glob.glob("/tmp/trapcam/*part.avi")
    for filename in files:
        os.rename(filename, filename.replace("part.avi", ".avi"))

def make_blur(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (21, 21), 0)

def imprint_datetime(now, frame):
    cv2.putText(frame, "{}".format(now), (0,470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

def calculate_moment(reference_blur, blur):
    diff = cv2.absdiff(reference_blur, blur)
    thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
    dilate = cv2.dilate(thresh, None, 2)
    return cv2.moments(dilate)['m00']

def start_recording(now, buffered_frames):
    filename = '/tmp/trapcam/{0}part.avi'.format(now.strftime("%Y-%m-%d_%H-%M-%S"))
    print('start recording video file:', filename)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640,  480))
    for f in buffered_frames:
        out.write(f)
    return out

def stop_recording(out):
    print('stop recording')
    out.release()

def capture(cap):
    d = 0
    started = False;
    reference_blur = None
    buffered_frames = []
    out = None
    try:
        while(1):
            ok, frame = cap.read()
            if not ok:
                print ("Failded to capture frame")
                break
            else:
                blur = make_blur(frame)
                now = datetime.now()
                imprint_datetime(now, frame)
                cv2.imshow('capture', frame)
                
                if not reference_blur is None:
                    moment = calculate_moment(reference_blur, blur)
                    print ("{0} {1}".format(d, moment))
            
                    if moment > 50000:
                        if d >= 50 and not started:
                            out = start_recording(now, buffered_frames)
                            started = True
                        elif not started:
                            buffered_frames.append(frame)
                        d = min(d + 10, 100)
                        
                    else:
                        if d <= -50 and started:
                            stop_recording(out)
                            out = None
                            started = False
                            rename_part_files()
                        d = max(d - 3, -100)
                        buffered_frames = []
               
                if started:
                    out.write(frame)
                reference_blur = blur
    finally:
        if started:
            out.release()

while True:
    rename_part_files()
    cap = cv2.VideoCapture(0)
    try:
        capture(cap)
    except Exception as ex:
        print("Error:", ex)
    finally:
        cap.release()
        cv2.destroyAllWindows()

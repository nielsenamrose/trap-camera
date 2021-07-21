import glob
import cv2
from datetime import datetime
import time
import os
import sys


def rename_part_files():
    files = glob.glob("*part.avi")
    for filename in files:
        os.rename(filename, filename.replace("part.avi", ".avi"))


def calculate_moment(frame, reference):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    if reference is None:
        return blur, 0
    diff = cv2.absdiff(reference, blur)
    thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
    dilate = cv2.dilate(thresh, None, 2)
    return blur, cv2.moments(dilate)['m00']


def imprint_datetime(now, frame):
    cv2.putText(frame, "{}".format(now), (0, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


def start_recording(now, buffered_frames, frame_rate):
    filename = '{0}part.avi'.format(now.strftime("%Y-%m-%d_%H-%M-%S"))
    print('start recording video file:', filename)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, frame_rate, (640,  480))
    for f in buffered_frames:
        out.write(f)
    return out


def stop_recording(out):
    print('stop recording')
    out.release()
    rename_part_files()


def capture(cap):
    start_time = datetime.now()
    number_of_frames = 0
    d = 0
    started = False
    reference = None
    buffered_frames = []
    out = None
    try:
        while(1):
            ok, frame = cap.read()
            number_of_frames += 1
            #cv2.imshow('capture', frame)
            if not ok:
                print("Failded to capture frame")
                break
            else:
                now = datetime.now()

                reference, moment = calculate_moment(frame, reference)
                imprint_datetime(now, frame)
                print("{0} {1}".format(d, moment))

                if moment > 50000:
                    if d >= 50 and not started:
                        duration_secs = (now - start_time).seconds
                        out = start_recording(
                            now, buffered_frames, 8)
                        started = True
                        start_time = now
                    elif not started:
                        buffered_frames.append(frame)
                    d = min(d + 10, 100)

                else:
                    if d <= -50 and started:
                        stop_recording(out)
                        out = None
                        started = False
                    d = max(d - 3, -100)
                    buffered_frames = []

                if started:
                    out.write(frame)
    finally:
        if started:
            stop_recording(out)


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

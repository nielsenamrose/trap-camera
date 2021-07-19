import cv2
import numpy as np
from datetime import datetime
import time
import os

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = None

reference_frame = None
reference_blur = None
i = 0  # number of frames since movement started
d = 0
#
f = 1
min_moment = 50000
started = False
buffered_frames = []
path = ""

while(1):
    ok, frame = cap.read()
    if ok:

        now = datetime.now()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (21, 21), 0)

        if reference_frame is None:
            reference_frame = frame
            reference_blur = blur

        diff = cv2.absdiff(reference_blur, blur)
        thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)[1]
        dilate = cv2.dilate(thresh, None, 2)
        moment = cv2.moments(dilate)['m00']

        print("{} {}".format(d, moment))

        cv2.putText(frame, f'{now}', (0, 470), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1, cv2.LINE_AA)

        if moment > min_moment:
            if d >= 50 and not started:
                path = './video/{}'.format(now.strftime("%Y-%m-%d_%H-%M-%S"))
                print('start writing video file:', path)
                out = cv2.VideoWriter(path+'.avi', fourcc, 20.0, (640,  480))
                for f in buffered_frames:
                    out.write(f)
                started = True
                i = 0
            elif not started:
                buffered_frames.append(frame)
            d = min(d + 10, 100)

        else:
            if d <= -50 and started:
                print('stop')
                out.release()
                os.rename(path+'.avi', path+'full.avi')
                started = False
            d = max(d - 3, -100)
            buffered_frames = []

            #cv2.imwrite(f'./frames/frame-{f:05d}-ref.jpg', reference_frame)
            #cv2.imwrite(f'./frames/frame-{f:05d}-{moment}.jpg', frame)

        if started:
            out.write(frame)
            cv2.imshow('capture', frame)

        reference_frame = frame
        reference_blur = blur

        k = cv2.waitKey(1) & 0xFF
        if k == 13:
            break
    else:
        print("Failded to capture frame")
        break

    time.sleep(0.05)

if started:
    out.release()
    os.rename(path+'.avi', path+'full.avi')
cap.release()
cv2.destroyAllWindows()

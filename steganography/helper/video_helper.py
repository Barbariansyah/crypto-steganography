import numpy as np
import cv2


def open_video_file(filename: str) -> np.array:
    cap = cv2.VideoCapture(filename)
    if cap.isOpened() == False:
        raise Exception('Video file not found')

    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        else:
            break

    cap.release()

    return np.array(frames)

import cv2
import sys
import time
import argparse
import numpy as np
from subprocess import Popen


def process_video():
    cap = cv2.VideoCapture(args.input_file)
    out = cv2.VideoWriter(
        "output_method1.avi",
        cv2.VideoWriter_fourcc(*"MJPG"),
        cap.get(cv2.CAP_PROP_FPS),
        (width, height),
    )
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        out.write(cv2.filter2D(frame, -1, kernel))

    cap.release()
    out.release()
    return None


if __name__ == "__main__":
    kernel = np.ones((7,7),np.float32)/49
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default="Kiiara.mp4", type=str)
    parser.add_argument("--x264", default=False, type=bool)
    parser.add_argument("--extra_flags", default="", type=str)
    args = parser.parse_args()

    start_time = time.time()
    cap = cv2.VideoCapture(args.input_file)
    width, height, end_frame = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        cap.get(cv2.CAP_PROP_FRAME_COUNT),
    )
    
    process_video()

    if args.x264 == True:
        ffmpeg_command = "ffmpeg -y -loglevel warning -i output_method1.avi -vcodec libx264 {} output_method1.mp4".format(
            args.extra_flags
        )
        t2 = time.time()
        Popen(ffmpeg_command, shell=True).wait()
    t3 = time.time()

    print(
        "\nMethod {}: Input:{}, x264:{}, extra_flags:{}, Time taken: {}".format(
            sys.argv[0], args.input_file, args.x264, args.extra_flags, t3 - start_time
        )
    )
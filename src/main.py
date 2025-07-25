import shutil
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from rich.text import Text

console = Console()

# TODO: make it better and less noisy
# TODO: make it so it can record and save the ascii version as a video

threshold_val = 80
fps = 15


# resize to make it fit for the terminal
def resize_video(frame, term_cols, term_rows):
    aspect_ratio_correction = 0.5
    new_w = term_cols // 2
    new_h = int((term_rows / aspect_ratio_correction) // 2)
    resized = cv2.resize(frame, (new_w, new_h))
    return resized


# img to ascii
def ascii_frame(frame):
    data = "@B&#GP5JY7?~:^.⠀"
    result = Text()

    for row in range(frame.shape[0]):
        line1 = ""
        line2 = ""
        for col in range(frame.shape[1]):
            pixel = frame[row, col]
            char = data[int(pixel) * len(data) // 256]
            line1 += char * 2
            line2 += char * 2
        result.append(line1 + "\n")
        result.append(line2 + "\n")
    return result


# convert frames to smthing that easier to decode for the ascii
def convert_frame(frame, term_cols, term_rows, threshold_val=100):
    resized_frame = resize_video(frame, term_cols, term_rows)
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.blur(gray_frame, (1, 1))
    _, thresh_frame = cv2.threshold(blur_frame, threshold_val, 255, cv2.THRESH_TOZERO)

    output = ascii_frame(thresh_frame)
    return output


# live feed for debugging
def debug_feed(frame, term_cols, term_rows, threshold_val=100):
    resized_frame = resize_video(frame, term_cols, term_rows)
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.blur(gray_frame, (1, 1))
    _, thresh_frame = cv2.threshold(blur_frame, threshold_val, 255, cv2.THRESH_TOZERO)
    return thresh_frame


if __name__ == "__main__":
    vid_cam = cv2.VideoCapture(0)

    if not vid_cam.isOpened():
        console.print("[bold red]Camera not found or failed to open.[/bold red]")
        exit()

    try:
        while True:
            term_cols, term_rows = shutil.get_terminal_size((80, 24))

            captured, frame = vid_cam.read()
            if not captured:
                console.print("[bold red]Failed to capture frame.[/bold red]")
                break

            ascii_output = convert_frame(frame, term_cols, term_rows, threshold_val)
            live_feed = debug_feed(frame, term_cols, term_rows, threshold_val)

            cv2.imshow("feed", live_feed)
            cv2.waitKey(1)

            console.clear()
            console.print(ascii_output)

            time.sleep(1 / fps)
    except KeyboardInterrupt:
        pass
    finally:
        vid_cam.release()
        cv2.destroyAllWindows()

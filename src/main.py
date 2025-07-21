import os
import shutil
import time

import cv2
from rich.console import Console
from rich.text import Text

console = Console()

# TODO: Have one pixel be drawn by 4 ascii chars instead of 1


def resize_video(frame, term_cols, term_rows):
    aspect_ratio_correction = 0.5
    new_w = term_cols
    new_h = int(term_rows / aspect_ratio_correction)
    resized = cv2.resize(frame, (new_w, new_h))
    return resized


def ascii_frame(frame):
    data = "@B&#GP5JY7?~:^. "
    rev_data = " .^:~?7YJ5PG#&B@"
    result = Text()

    for row in range(frame.shape[0]):
        for column in range(frame.shape[1]):
            pixel = frame[row, column]
            char = data[int(pixel) * len(data) // 256]
            result += char
        result.append("\n")

    return result


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

            resized_frame = resize_video(frame, term_cols, term_rows)
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            ascii_output = ascii_frame(gray_frame)

            cv2.imshow("feed", gray_frame)
            cv2.waitKey(1)

            os.system("clear")
            console.print(ascii_output)
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass
    finally:
        vid_cam.release()

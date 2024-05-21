import logging
from pathlib import Path

import click
import cv2 as cv
from cfg import cfg


@click.group(name="sample", help="Run various sample functions")
def sample():
    pass


@sample.command(name="showlog", help="Show logging format")
def showlog():
    logging.info("Showing logging format...")


@sample.command(name="showimg", help="Show test img")
def showimg():
    logging.info("Showing test image...")
    img_file = Path("images/superChicken.jpg")
    img = cv.imread(img_file.as_posix())

    cv.imshow("Display window", img)
    k = cv.waitKey(0)


@sample.command(name="convertvid", help="Convert test video to images")
def convertvid():
    vid_file = Path("videos/sirgSamp.mp4")
    vid_images_dir = cfg.root / "images" / vid_file.stem
    if vid_images_dir.exists():
        for f in vid_images_dir.iterdir():
            f.unlink()
    vid_images_dir.mkdir(exist_ok=True)

    vid = cv.VideoCapture(vid_file.as_posix())
    current_frame = 0

    while True:
        # reading from frame
        ret, frame = vid.read()

        if ret:
            # if video is still left, continue creating images
            name = vid_images_dir / f"{current_frame}.jpg"
            logging.info(f"Creating {name}...")

            # writing the extracted images
            cv.imwrite(name.as_posix(), frame)
            current_frame += 1
        else:
            break

    # release all space and windows once done
    vid.release()
    cv.destroyAllWindows()

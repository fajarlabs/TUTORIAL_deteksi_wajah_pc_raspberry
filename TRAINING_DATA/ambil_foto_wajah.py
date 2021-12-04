import cv2
import argparse
import os.path
from os import path, makedirs

parser = argparse.ArgumentParser(description='Command line description')
parser.add_argument('--folder_name', type=str,help='A required folder name argument')
parser.add_argument('--camera', type=int,help='A required camera id argument')
args = parser.parse_args()
name = args.folder_name

cam = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW)

cv2.namedWindow("press space to take a photo | esc to save", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo | esc to save", 500, 300)

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo | esc to save", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        directory = "dataset/"+ name
        if(not path.exists(directory)):
        	makedirs(directory)
        img_name = directory+"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

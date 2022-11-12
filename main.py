import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import statistics as st
import math
from PIL import Image
import pyttsx3


INDEX = 0
I = 0
SAVE = 0


def camera():
    try:
        global I
        array_path_images = create_array_of_images()
        for i in range(0, len(array_path_images)):
            img = Image.open(array_path_images[i])
            img.crop((650, 170, 1050, 500)).save('new_img.jpg', quality=95)
            # im_crop = img.crop((737, 390, 775, 415))
            # im_crop = img.crop((720, 355, 740, 375))
            arr = np.asarray(Image.open('new_img.jpg'), dtype='uint8')
            status = False
            for i in range(len(arr)):
                if status:
                    break
                for j in range(len(arr[i])):
                    if np.all(arr[i][j] == (22, 21, 19), axis=0):
                        arr = []
                        a_x = []
                        a_y = []
                        rgb_im = img.convert('RGB')
                        path = (22, 21, 19)
                        for x in range(img.size[1]):
                            for y in range(img.size[0]):
                                pix = rgb_im.getpixel((y, x))
                                if pix == path:
                                    a_y.append(y)
                                    a_x.append(x)
                        img.crop((math.floor(st.mean(a_y)) - 400, math.floor(st.mean(a_x)) - 150, math.floor(st.mean(a_y)) - 200, math.floor(st.mean(a_x)))).save('new_img.jpg', quality=95)
                        arr = np.asarray(Image.open('new_img.jpg'), dtype='uint8')
                        status = True
                        break
            max = 0
            while True:
                img = cv2.imread(array_path_images[I])
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if len(find_pix(arr, 29, 26, 19)) != 0 or len(find_pix(arr, 26, 23, 18)) != 0 or len(find_pix(arr, 72, 65, 59)) != 0:
                    print("CAMERA")
                    plt.imshow(img)
                    engine = pyttsx3.init()
                    engine.say('Внимание, камера! Ограничение 60!')
                    engine.runAndWait()
                    plt.show()
                    I += 1
                    break
                if len(arr) == 330:
                    plt.imshow(img)
                    engine = pyttsx3.init()
                    engine.say('Камер нет!')
                    engine.runAndWait()
                    plt.show()
                    I += 1
                    break
    except OSError as err:
        print(f"Error! Type of error {err}...")


def create_array_of_images():
    try:
        images = []
        for i in range(1, 100):
            images.append(f'frames\\{i:04d}.jpg')
        return images
    except OSError as err:
        print(f"Error! Type of error {err}...")


def find_pix(arr_img, red, green, blue):
    try:
        global INDEX
        if INDEX > len(arr_img):
            return "error! invalid index!"

        index_ = np.where(np.all(arr_img == (red, green, blue), axis=0))
        out = np.transpose(index_)
        INDEX += 1
        return out
    except OSError as err:
        print(f"Error! Type of error {err}...")


def video_to_frames(path):
    save = 0
    if not os.path.isdir("frames"):
        os.mkdir("frames")
    videoCapture = cv2.VideoCapture()
    videoCapture.open(path)
    frames_ = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(1, frames_):
        ret, frame = videoCapture.read()
        cv2.imwrite(f"frames/{i:04d}.jpg", frame)
        if i == 100:
            print('frames is saved!')
            save = i
            break
    return save

if __name__ == "__main__":
    # video_file = "video/video_reg.mp4"
    # SAVE = video_to_frames(video_file)
    camera()

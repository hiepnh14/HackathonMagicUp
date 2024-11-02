import cv2
import os
import numpy as np
from skimage.filters import gaussian
from test import evaluate
import argparse


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--img-path', default='imgs/116.jpg')
    return parse.parse_args()


def sharpen(img):
    img = img * 1.0
    # gauss_out = gaussian(img, sigma=5, multichannel=True)
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)
    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255
    return np.array(img_out, dtype=np.uint8)


def changePartColor(image, parsing, part=17, color=[230, 50, 20]):
    b, g, r = color      #[10, 50, 250]       # [10, 250, 10]
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part == 12 or part == 13:
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    else:
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    # if part == 17:
    #     changed = sharpen(changed)

    changed[parsing != part] = image[parsing != part]
    return changed


def makeup(image_path, colors, cp='cp/79999_iter.pth'):
    # 1  face
    # 11 teeth
    # 12 upper lip
    # 13 lower lip
    # 17 hair

    # args = parse_args()
    atts = ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'eye_g', 'l_ear', 'r_ear', 'ear_r',
            'nose', 'mouth', 'u_lip', 'l_lip', 'neck', 'neck_l', 'cloth', 'hair', 'hat']

    table = {
        'face': 1,
        'l_brow': 2,
        'r_brow': 3,
        'teeth': 11,
        'hair': 17,
        'upper_lip': 12,
        'lower_lip': 13,
        'neck': 14,
        'eye_g': 6,
        'nose': 10,
        'r_eye': 5,
        'l_eye': 4
    }

    # image_path = args.img_path

    image = cv2.imread(image_path)
    ori = image.copy()
    parsing = evaluate(image_path, cp)
    # parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)
    parsing = cv2.resize(parsing, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

    parts = [table['hair'], table['upper_lip'], table['lower_lip'], table['l_eye'], table['r_eye']]

    # colors = [[0, 0, 0], [0, 0, 0], [0,0,00]] #colors = [[230, 50, 20], [20, 70, 180], [20, 70, 180]]
    # colors = [[255, 223, 186], [255, 105, 180], [255, 0, 102], [0, 191, 255]]
    for part, color in zip(parts, colors):
        image = changePartColor(image, parsing, part, color)

    cv2.imshow('image', cv2.resize(ori, (512, 512)))
    cv2.imshow('color', cv2.resize(image, (512, 512)))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image
















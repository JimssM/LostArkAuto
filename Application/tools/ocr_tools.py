import os

from paddleocr import PaddleOCR
from .image_tools import *
from ..public import static_path

en_model = PaddleOCR(use_angle_cls=False, lang="en")  # need to run only once to download and load model into memory
ch_model = PaddleOCR(use_angle_cls=False, lang="ch")


def ppocr(rect, det=False, num_only=False, model="en"):
    if model not in ["en", "ch"]:
        raise ValueError("model must be 'en' or 'ch'")

    img_path = static_path + "\\ocr\\ocr.png"
    cv2.imwrite(img_path, grab_rect_to_cv2(rect))
    if model == "en":
        result = en_model.ocr(img_path, cls=False, det=det)
    elif model == "ch":
        result = ch_model.ocr(img_path, cls=False, det=det)

    for idx in range(len(result)):
        res = result[idx]
        if det:
            if res != []:
                if num_only:
                    r = ''.join([char for char in res[0][1][0] if char.isdigit()])
                else:
                    r = res[0][1][0]
                return r
        else:
            if num_only:
                r = ''.join([char for char in res[0][0] if char.isdigit()])
            else:
                r = res[0][0]
            return r

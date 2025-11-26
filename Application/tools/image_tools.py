import datetime

import cv2
from PIL import ImageGrab
from .input_control import *

import numpy as np

'''
找色处理
'''
def get_point_color(point):
    img = grab_rect_to_cv2(None, if_gray=False)

    # 转换为numpy数组
    img = np.array(img)

    # 提取指定点的颜色
    pixel_color = img[point[1], point[0], :3]
    return pixel_color


def match_point(point, color, tolerance=(10, 10, 10), region=None):
    img = grab_rect_to_cv2(region, if_gray=False)

    # 转换为numpy数组
    img = np.array(img)

    # 提取指定点的颜色
    pixel_color = img[point[1], point[0], :3]

    # 把容差值转换为数组
    tolerance = np.array(tolerance)

    # 获取上限和下限
    lower_bound = color - tolerance
    upper_bound = color + tolerance

    if np.all(lower_bound <= pixel_color) and np.all(pixel_color <= upper_bound):
        return True
    return False


# 多点找色，返回第一个值
def  match_points(region,base_color, tolerance, *offset_colors):
    '''
    :param base_color: 第一个颜色
    :param tolerance: 容差范围
    :param offset_colors: 列表、元组，每一个元素第一个为相对pos的偏移值，第二个为颜色
    :param region: 需要处理的矩形区域
    :return: 找到的颜色坐标，如果没有找到返回[0, 0]
    '''
    result = [0, 0]

    # 获取图片的高度和宽度，并创建一个二维数组来存储每个像素的RGB值
    img = grab_rect_to_cv2(region, if_gray=False)
    height, width, _ = img.shape
    rgb_values = img

    # 将颜色和容差转换为NumPy数组
    base_color = np.array(base_color)
    tolerance = np.array(tolerance)

    # 创建一个布尔掩码来找到与第一个颜色匹配的所有像素
    matches = np.all(np.abs(rgb_values - base_color) <= tolerance, axis=-1)

    # 遍历所有与第一个颜色匹配的像素
    for y, x in zip(*np.where(matches)):
        matched = True
        for offset, color in offset_colors:
            color = np.array(color)
            dx, dy = offset
            new_x, new_y = x + dx, y + dy

            # 检查边界条件
            if not (0 <= new_x < width and 0 <= new_y < height):
                matched = False
                break

            # 检查颜色匹配
            if not np.all(np.abs(rgb_values[new_y, new_x] - color) <= tolerance):
                matched = False
                break

        if matched:
            return (x + region[0], y + region[1])

    return result


# 多点找色并返回所有值的列表
def match_all_points(region,base_color, tolerance, *offset_colors):
    '''
    :param base_color: 第一个颜色
    :param tolerance: 容差范围
    :param offset_colors: 列表、元组，每一个元素第一个为相对pos的偏移值，第二个为颜色
    :param region: 需要处理的矩形区域
    :return: 找到的颜色坐标列表，如果没有找到返回[[0, 0]]
    '''
    result = []

    # 获取图片的高度和宽度，并创建一个二维数组来存储每个像素的RGB值
    img = grab_rect_to_cv2(region, if_gray=False)
    height, width, _ = img.shape
    rgb_values = img

    # 将颜色和容差转换为NumPy数组
    base_color = np.array(base_color)
    tolerance = np.array(tolerance)

    # 创建一个布尔掩码来找到与第一个颜色匹配的所有像素
    matches = np.all(np.abs(rgb_values - base_color) <= tolerance, axis=-1)

    # 遍历所有与第一个颜色匹配的像素
    for y, x in zip(*np.where(matches)):
        matched = True
        for offset, color in offset_colors:
            color = np.array(color)
            dx, dy = offset
            new_x, new_y = x + dx, y + dy

            # 检查边界条件
            if not (0 <= new_x < width and 0 <= new_y < height):
                matched = False
                break

            # 检查颜色匹配
            if not np.all(np.abs(rgb_values[new_y, new_x] - color) <= tolerance):
                matched = False
                break

        if matched:
            result.append([x + region[0], y + region[1]])

    if not result:
        return [[0, 0]]

    return result


# 等待颜色
def wait_for_color(pos, rgb, cast=(10, 10, 10), rect=None):
    while not match_point(pos, rgb, cast, rect):
        continue


# 等待颜色消失
def wait_no_color(pos, rgb, cast=(10, 10, 10), rect=None):
    while match_point(pos, rgb, cast, rect):
        continue


'''
图像处理
'''


# 截图，获取图像对象
def grab_rect(rect=None):
    '''
    截图，获取图像对象
    :param rect: 截图区域，默认为None，代表全屏
    :return: 返回图像对象
    '''
    if rect is None:
        img = ImageGrab.grab()
    else:
        img = ImageGrab.grab(rect)
    return img


# 截取区域，转为cv2格式图片
def grab_rect_to_cv2(rect=None, if_gray=True):
    '''
    截取区域，转为cv2格式图片
    :param rect: 截取的区域
    :param if_gray: 是否返回灰度图
    :return:
    '''
    img = grab_rect(rect)
    img_np = np.array(img)
    if if_gray == False:
        return img_np
    return cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY).astype('uint8')


def grab_rect_and_save(path, img_name=None, rect=None, format='jpg'):
    '''
    截图并保存
    :param path:保存路径
    :param img_name:图片名称，若为None则默认取名f"screenshot_{current_datetime}.{format}"
    :param rect:截取区域，若为None则默认截取全屏
    :param format:图片格式，默认jpg，可选png
    :return:
    '''
    img = grab_rect(rect)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if img_name is None:
        img_name = f"screenshot_{current_datetime}.{format}"
    else:
        img_name = f"{img_name}.{format}"
    img.save(f"{path}/{img_name}")


def rect_match_sqdiff(big_img_path: str, threshold=0.05, rect=None):
    '''
    opencv sqdiff匹配方法，适合大图涂黑，用小原图拿去匹配
    :param big_img_path: 大图路径
    :param threshold: 阈值，默认0.05，越低匹配越严格
    :param rect:小原图的截取范围
    :return:返回匹配的精准度，匹配失败返回0代表False
    '''
    small_img = grab_rect_to_cv2(rect)
    big_img = cv2.imread(big_img_path, 0)
    result = cv2.matchTemplate(small_img, big_img, cv2.TM_SQDIFF_NORMED)  # 适合匹配小图
    min_val = cv2.minMaxLoc(result)[0]
    # print(min_val)
    if min_val <= threshold:
        return min_val
    else:
        return 0


def rect_match_ccoeff(big_img_path: str, threshold=0.8, rect=None):
    '''
    opencv ccoeff匹配方法，不涂黑也可以匹配
    :param big_img_path: 大图路径
    :param threshold: 阈值，默认0.8，越高匹配越严格
    :param rect:小原图的截取范围
    :return:返回匹配的精准度，匹配失败返回0代表False
    '''
    small_img = grab_rect_to_cv2(rect)
    big_img = cv2.imread(big_img_path, 0)
    result = cv2.matchTemplate(small_img, big_img, cv2.TM_CCOEFF_NORMED)
    max_val = cv2.minMaxLoc(result)[1]
    if max_val >= threshold:
        return max_val
    else:
        return 0


def find_img_low_threshold(img_path: str, rect=None, threshold=0.05):
    '''
    匹配全屏，返回要匹配的图片坐标
    :param img_path:要在屏幕寻找的图片的路径
    :param rect:要匹配的屏幕区域，默认为None代表全屏
    :param threshold:阈值，默认0.05，越小越精确
    :return:
    '''
    img = grab_rect_to_cv2(rect)
    template = cv2.imread(img_path, 0)
    height, width = template.shape
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val = cv2.minMaxLoc(result)[0]
    # print("min val: ",min_val)
    pos = [0, 0]
    if min_val <= threshold:
        upper_left = cv2.minMaxLoc(result)[2]
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
        # 换算坐标
        if rect is None:
            pos[0] = avg[0]
            pos[1] = avg[1]
        else:
            pos[0] = avg[0] + rect[0]
            pos[1] = avg[1] + rect[1]
    return pos

def find_all_img_low_threshold(img_path: str, rect=None, threshold=0.05):
    img = grab_rect_to_cv2(rect)
    template = cv2.imread(img_path, 0)
    height, width = template.shape
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)

    matches = []

    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if min_val > threshold:
            break

        upper_left = min_loc
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))

        if rect is None:
            pos = [avg[0], avg[1]]
        else:
            pos = [avg[0] + rect[0], avg[1] + rect[1]]

        matches.append(pos)

        # 将匹配区域涂黑
        cv2.rectangle(img, upper_left, lower_right, (0, 0, 0), -1)

        # 重新计算结果
        result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)

    return matches


def find_img_high_threshold(img_path: str, rect=None, threshold=0.8):
    '''
    匹配全屏，返回要匹配的图片坐标
    :param img_path:要在屏幕寻找的图片的路径
    :param rect:要匹配的屏幕区域，默认为None代表全屏
    :param threshold:阈值，默认0.8，越大越精确
    :return:
    '''
    img = grab_rect_to_cv2(rect)
    template = cv2.imread(img_path, 0)
    height, width = template.shape
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # 适合匹配小图
    max_val = cv2.minMaxLoc(result)[1]
    pos = [0, 0]
    if max_val >= threshold:
        upper_left = cv2.minMaxLoc(result)[3]
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
        # 换算坐标
        if rect is None:
            pos[0] = avg[0]
            pos[1] = avg[1]
        else:
            pos[0] = avg[0] + rect[0]
            pos[1] = avg[1] + rect[1]
    return pos


def find_img_pyautogui(img_path, rect=None, confidence=0.9):
    if rect == None:
        return pyautogui.locateOnScreen(img_path, confidence)
    return pyautogui.locateOnScreen(img_path, confidence, region=rect)


def if_image_exists(image_path: str, threshold=0.05):
    return rect_match_sqdiff(image_path, threshold)


def click_image(image_path, threshold=0.05, delay=1):
    pos = find_img_low_threshold(image_path, threshold=threshold)
    if pos != [0, 0]:
        click(pos)
        time.sleep(delay)


def wait_for_image(image_path: str, threshold=0.05, duration=0.1, delay=1):
    while True:
        if rect_match_sqdiff(image_path, threshold):
            time.sleep(delay)
            break
        time.sleep(duration)

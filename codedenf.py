# -*- coding:utf-8 -*-
import tesserocr
from PIL import Image
import requests


def get_code(c):
    with open('code.jpg', 'wb') as code:
        code.write(c)
        code.close()
        image = Image.open('code.jpg')
    image = image_grayscale_deal(image)
    image = image_thresholding_method(image)
    #image.show()
    print(tesserocr.image_to_text(image))
    code = tesserocr.image_to_text(image)
    return code

def image_grayscale_deal(image):
    image = image.convert('L')
    return image

def image_thresholding_method(image):
    threshold = 160
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    return image

if __name__ == "__main__":
    url = 'https://health.cpic.net.cn/Account/CheckCode?ID=1'
    s = requests.session()
    c = s.get(url).content
    code = get_code(c)
    print(code)

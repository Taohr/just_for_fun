
#coding:utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter


'''
复制图片的一部分，
粘贴到别处，
并保存新的图片
'''


import random
# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))

# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def test():
    image = Image.open('0.png')
    # 创建Draw对象:
    region = (0,0,100,100)
    sub = image.crop(region)
    # sub.save('tmp.png', 'png')
    # sub = Image.open('tmp.png')
    image.paste(sub, (100, 100))
    image.save('1.png', 'png')

    # help(ImageDraw)
if __name__ == '__main__':
    test()


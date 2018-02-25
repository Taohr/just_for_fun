# -*- coding:utf-8 -*-

import imageio 
import glob 
import os 
import time
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter
import src.split_gif_to_png

SIZE_SCALE = 0.8

BASE_X = 143 * SIZE_SCALE
BASE_Y = 27 * SIZE_SCALE
BASE_H = 29 * SIZE_SCALE
OFFSET_H = -6

BOX_OFFSET_X = 0
BOX_OFFSET_Y = 55
BOX_SCALE = 1.25

COLOR = (225, 225, 225)

OUT_PUT_FOLDER = 'out'

def cmp(a, b):
    a = os.path.basename(a)
    b = os.path.basename(b)
    ia = int(a.split('.')[0])
    ib = int(b.split('.')[0])
    return ia - ib

# look for all images needed 
def find_all_png(path): 
    png_filenames = glob.glob('%s/*.png'%path)
    # png_filenames.sort(cmp)
    png_filenames.sort(reverse = True)
    buf = png_filenames[:]
    return buf

#make images into a gif 
def create_gif(image_list, gif_name): 
    frames = [] 
    for image_name in image_list: 
        frame = imageio.imread(image_name, 'png')
        frames.append(frame) 
        # Save them as frames into a gif 
        out_git_name = os.path.join(OUT_PUT_FOLDER, gif_name)
        imageio.mimsave(out_git_name, frames, 'GIF', duration = 0.1)

def get_gif_name(path, text):
    gif_name = os.path.basename(path)
    folder, ext = os.path.splitext(gif_name)
    gif_name = folder + '-%s'%text + ext
    return gif_name

def get_paste_box(x, y, h):
    nx = x + BOX_OFFSET_X
    ny = y + BOX_OFFSET_Y
    nw = nx+round(h * BOX_SCALE, 2)
    nh = ny+round(h * BOX_SCALE, 2)
    frm = (nx, ny, nw, nh)
    to = (x, y-5, nw, nh)
    return frm, to

def paste_sub_image(image, frm, to):
    sub = image.crop(frm)
    sub = sub.filter(ImageFilter.BLUR)
    image.paste(sub, to[:2])
    return image

def add_text(path, text, size, x, y, color, scale, copy_sub = False):
    size = size * scale
    image = Image.open(path)
    if (copy_sub):
        frm, to = get_paste_box(x, y, size)
        image = paste_sub_image(image, frm, to)
    font = ImageFont.truetype('Arial Unicode.ttf', int(size))
    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, font=font, fill=color)
    basename = os.path.basename(path)
    ext = basename.split('.')[-1]
    savepath, ext = os.path.splitext(path)
    if ext[0] == '.':
        ext = ext[1:]
    image.save(path, ext)
    pass

def get_posdata():
    posfile = open('src/pos.log')
    posdata = posfile.readlines()
    posdata = [pos[:-1] for pos in posdata]
    posdata = [pos.split(',') for pos in posdata]
    posdata = [[int(p)*SIZE_SCALE for p in pos] for pos in posdata]
    return posdata

def copy_a_temp_path(path):
    folder = path+'-tmp'
    if (os.path.exists(folder)):
        shutil.rmtree(folder)
    shutil.copytree(path, folder)
    return folder

def add_text_to_png(text, png_files, posdata, scale):
    color = COLOR
    x = posdata[0][0]
    y = posdata[0][1]
    h = posdata[0][2]

    offx = BASE_X - x
    offy = BASE_Y - y
    offh = BASE_H - h
    offh = offh + OFFSET_H#针对字数过多的情况

    for i in range(len(png_files)):
        if (i >= len(posdata)):
            break
        data = posdata[i]
        x = data[0]
        y = data[1]
        h = data[2]
        new_x = x + offx
        new_y = y + offy + (h * (1-scale))
        new_size = h + offh
        path = png_files[i]
        add_text(path, text, new_size, new_x, new_y, color, scale)
    pass

def create(path, text, scale = 1.0, res = None):
    if res == None:
        res = split_gif_to_png.split(path)
    else:
        res = copy_a_temp_path(res)
    png_files = find_all_png(res)
    posdata = get_posdata()
    add_text_to_png(text, png_files, posdata, scale)
    gif_name = get_gif_name(path, text)
    create_gif(png_files, gif_name)
    if (os.path.exists(res)):
        shutil.rmtree(res)
    pass

def main(text, scale = 1.0):
    gif_path = 'res/tuboshu.gif'
    res = 'res/tuboshu-png'
    create(gif_path, text, scale, res)

if __name__ == '__main__':
    main('hello')
    pass

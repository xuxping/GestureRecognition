# -*- coding:utf-8 -*-
import os
from PIL import Image, ImageOps

IMAGE_WIDTH,IMAGE_HEGHT = 64, 64
def enhance_image():
    """增强图片"""
    imgid = 0
    for dirpath, dirnames, filenames in os.walk('./gesture/raw_data/'):
        label =  dirpath.split('/')[-1]
        wid = 0
        for filename in filenames:
            if filename[0] == '.':
                continue
            filepath = os.path.join(dirpath, filename)
            im = Image.open(filepath).convert('L')
            imgs = [im, im.rotate(90), im.rotate(180), im.rotate(270), ImageOps.mirror(im), ImageOps.flip(im)]
            iid = 0
            for img in imgs:
    		img = img.resize((IMAGE_WIDTH,IMAGE_HEGHT), Image.ANTIALIAS)
                img.save('./gesture/train/%s%s%s%s.jpg' % (imgid, wid, iid, label))
                iid += 1
            wid += 1
        imgid += 1

if __name__ == '__main__':
    enhance_image()

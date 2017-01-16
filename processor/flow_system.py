"""
core funciton:
    1. give your intresting region of a target picuter.
    2. sewing all picture into one big picuter.
"""
from PIL import Image
from PIL import ImageOps
from numpy import array
import os


# helper function
def to_region(x, y, dx, dy):
    return x, y, x + dx, y + dy


class SewingMachine(object):
    def __init__(self, image_path, conf):
        self.region_list = list(SewingMachine.get_region(conf['region_file']))
        # target img which you want to sew.
        self.target_img = image_path
        self.last = 0
        self.fangda = tuple(conf['fangda'])
        self.save_address = conf['save_address']

    @staticmethod
    def get_region(region_file):
        with open(region_file, 'r') as f:
            data = f.read()
        region_str_list = data.split('\n')
        for one in region_str_list:
            yield tuple([int(one) for one in one.strip('()').split(',')])

    def normalize(self, img_list):
        threshold_x, threhold_y = self.fangda
        for one in img_list:
            width, height = one.size
            if width < threshold_x:
                width = threshold_x
            if height < threhold_y:
                height = threhold_y
            yield one.resize((width, height))

    def get_picture(self):
        raw_img = Image.open(self.target_img)

        for one in self.region_list:
            yield raw_img.crop(to_region(*one))

    def paste_one_picture(self, background, new):
        width, length = new.size
        # left, upper, right, and lower
        background.paste(new, [0, self.last])
        self.last += length
        return background

    def process(self):
        img_list = list(self.get_picture())
        resized_img_list = list(self.normalize(img_list))
        vertical_pixel = sum([one.size[1] for one in resized_img_list])
        horizontal_pixel = max([one.size[0] for one in resized_img_list])
        background = Image.new('RGB', (horizontal_pixel, vertical_pixel))
        for img in resized_img_list:
            background = self.paste_one_picture(background, img)
        # os.remove(self.target_img)
        background = ImageOps.invert(background)

        background.convert('L').save(self.save_address)
        # background.show()
        print('the picture is saved')
        return self.save_address

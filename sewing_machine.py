import os
import random
import subprocess
import time
from sys import version_info
from utils import read_delete, get_conf, CustomImage, CustomText
from PIL import Image

conf_dict = get_conf('conf/main.toml')['sewing_machine']


class Radar(object):
    """Represents a scanner of scaning new image file on specific directory.

    Subclass may do what, for now we don't know that.

    Public attributes:
    -image_direectory is derectory of your receiving images.
    -language languange you use to OCR.
        xxx.trained.data
    -counter how many direcotory you want to store for debuging.
    -debug_object for internal use.

    """

    def __init__(self, conf):
        """
        initilaize
        """
        self.image_directory = conf['image_store']
        self.language = conf['language']
        self.counter = conf['box_count']
        self.debug_object = []

    def get_a_picture_randomly(self):
        """
        from the directory we are scaning, pop up a picuture randomly
        :return: str::a fullpath of this poped image.
        """
        files = os.listdir(self.image_directory)
        if len(files) == 0:
            return None
        full_image_name = os.path.abspath(self.image_directory + random.choice(files))
        return full_image_name

    @staticmethod
    def use_plugin(image_path, plugin_name):
        """
        get a image name , load a function to process image,
        then it can be tesseract recognition.
        :return: return a result of machine.process(), normal it's a image path.
        """

        import_str = 'from processor.{} import SewingMachine'.format(plugin_name)
        exec(import_str, globals())
        conf = get_conf('processor/{}.toml'.format(plugin_name))
        machine = SewingMachine(image_path, conf)
        return machine.process()

    def get_result(self, image_path):
        """call tesseract to generate out.txt. And read
            data from it.

        :param image_path: use this picture to recognition
        :return: text data from out.txt
        """

        cmd = 'tesseract {} out -l {}'.format(image_path, self.language)
        arguments = cmd.split()
        if version_info[0] == 2:
            subprocess.call(arguments)
        else:
            subprocess.run(arguments)
        # os.remove(image_path)
        a.collector('out.txt', 'no use')
        data = read_delete('out.txt')
        return data

    def collector(self, file_name, which):
        ext = file_name[-3:]
        if ext in ('png', 'bmp'):
            # png read method
            one_picture = Image.open(file_name)
            size = one_picture.size
            if which == 'good':
                # g = one_picture.getdata(1)
                # b = one_picture.getdata(2)
                # data = [one for one in zip(g, b)]
                # data = one_picture.getdata(0)
                data = one_picture.getdata()
            else:
                data = one_picture.getdata()
            self.debug_object.append(CustomImage(size, data, which))

        if ext in 'txt':
            # txt read method
            with open(file_name, 'r') as f:
                data = f.read()
            self.debug_object.append(CustomText(data))


def save(debug_object, index):
    num = index % 10
    for one in debug_object:
        one.custome_save(num)


if __name__ == '__main__':
    a = Radar(conf_dict)
    number = 0
    while True:
        image_to_be_processed = a.get_a_picture_randomly()

        if image_to_be_processed is not None:
            a.collector(image_to_be_processed, 'raw')
            good_image = a.use_plugin(image_to_be_processed, plugin_name=conf_dict['plugin_name'])
            a.collector(good_image, 'good')
            res = a.get_result(good_image)
            save(a.debug_object, number)
            print(res)
            number += 1
            time.sleep(5)
        else:
            print('there is no picuture in directory.')
            time.sleep(3)

import os
import random
import subprocess
import time

from utils import read_delete, get_conf

conf_dict = get_conf('conf/main.toml')['sewing_machine']


class Radar(object):
    """Represents a scanner of scaning new image file on specific directory.

    Subclass may do what, for now we don't know that.

    Public attributes:
    -image_direectory is derectory of your receiving images.
    -whcih languange you use to OCR.
        xxx.trained.data

    """

    def __init__(self, conf):
        """
        initilaize
        """
        self.image_directory = conf['image_store']
        self.language = conf['language']

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
        print(cmd)
        arguments = cmd.split()
        subprocess.run(arguments)
        # os.remove(image_path)
        data = read_delete('out.txt')
        return data


if __name__ == '__main__':
    a = Radar(conf_dict)
    while True:
        image_to_be_processed = a.get_a_picture_randomly()
        if image_to_be_processed is not None:
            good_image = a.use_plugin(image_to_be_processed, plugin_name=conf_dict['plugin_name'])
            res = a.get_result(good_image)
            print(res)
            time.sleep(5)
        else:
            print('there is no picuture in directory.')
            time.sleep(3)

import toml
import os
import uuid
from PIL import Image
# helper function
def get_conf(conf_file):
    """  configuration file in toml format """

    with open(conf_file, 'r') as conf_h:
        conf = toml.loads(conf_h.read())

    return conf


# helper function
def read_delete(path):
    """

    :param path: out.txt path
    :return: list data splited
    """
    with open(path, 'r') as f:
        data = f.read()
    os.remove(path)
    return data.split('\n')


# helper class
class CustomImage(object):
    def __init__(self, size, data, name):
        self.size = size
        self.data = data
        self.name = name

    def custome_save(self, num):
        # TODO: will be closed soon.
        path_str = 'debug/{}'.format(num)
        os.makedirs(path_str, exist_ok=True)
        new_ = Image.new('RGB', self.size)
        new_.putdata(self.data, scale=1.0, offset=0.0)
        if self.name == 'good':
            new_.convert('L').save(path_str+'/{}.png'.format(self.name))
        else:
            new_.save(path_str + '/{}.png'.format(self.name))



class CustomText(object):
    def __init__(self, raw_str):
        self.str = raw_str

    def custome_save(self, num):
        path_str = 'debug/{}'.format(num)
        os.makedirs(path_str, exist_ok=True)
        with open(path_str+'/out.txt', 'w') as f:
            f.write(self.str)


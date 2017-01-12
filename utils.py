import toml
import os


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

import configparser
import os
import pathlib

PATH = str(pathlib.Path(__file__).parent.absolute())
PATH = os.path.normpath(PATH + os.sep + os.pardir)


def createConfig(path_file):
    """Create a config file"""
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "week", "1")
    # Сохраняем конфиг. файл.
    with open(PATH + path_file, "w") as config_file:
        config.write(config_file)


def getWeekConfig(path_file):
    if not os.path.exists(PATH + path_file):
        createConfig(path_file)
    config = configparser.ConfigParser()
    config.read(PATH + path_file)
    # Читаем значения из конфиг. файла.
    return config.get("Settings", "week")


def changeWeekConfig(path_file):
    if not os.path.exists(PATH + path_file):
        createConfig(path_file)
    config = configparser.ConfigParser()
    config.read(PATH + path_file)
    # Меняем значения из конфиг. файла.
    if getWeekConfig(path_file) == '1':
        config.set("Settings", "week", "2")
    else:
        config.set("Settings", "week", "1")
    # Вносим изменения в конфиг. файл.
    with open(PATH + path_file, "w") as config_file:
        config.write(config_file)

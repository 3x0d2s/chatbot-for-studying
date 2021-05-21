# -*- coding: utf8 -*-
#
import configparser
import os
import pathlib

PATH = str(pathlib.Path(__file__).parent.absolute())
PATH = os.path.normpath(PATH + os.sep + os.pardir)


def create_config(path_file):
    """Создаёт файл конфигурации."""
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "week", "1")
    # Сохраняем конфиг. файл.
    with open(PATH + path_file, "w") as config_file:
        config.write(config_file)


def get_week_config(path_file):
    """Парсит конфигурацию и получаем текущий идентификатор недели."""
    if not os.path.exists(PATH + path_file):
        create_config(path_file)
    config = configparser.ConfigParser()
    config.read(PATH + path_file)
    # Читаем значения из конфиг. файла.
    return config.get("Settings", "week")


def change_week_config(path_file):
    """Сменяет текущий идентификатор недели."""
    if not os.path.exists(PATH + path_file):
        create_config(path_file)
    config = configparser.ConfigParser()
    config.read(PATH + path_file)
    # Меняем значения из конфиг. файла.
    if get_week_config(path_file) == '1':
        config.set("Settings", "week", "2")
    else:
        config.set("Settings", "week", "1")
    # Вносим изменения в конфиг. файл.
    with open(PATH + path_file, "w") as config_file:
        config.write(config_file)

import configparser
import os


def createConfig(path):
    """Create a config file"""
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "week", "1")
    # Сохраняем конфиг. файл.
    with open(path, "w") as config_file:
        config.write(config_file)


def getWeekConfig(path):
    if not os.path.exists(path):
        createConfig(path)

    config = configparser.ConfigParser()
    config.read(path)
    # Читаем некоторые значения из конфиг. файла.
    return config.get("Settings", "week")


def changeWeekCondfig(path, value):
    if not os.path.exists(path):
        createConfig(path)
    config = configparser.ConfigParser()
    # Меняем значения из конфиг. файла.
    config.set("Settings", "week", value)
    # Вносим изменения в конфиг. файл.
    with open(path, "w") as config_file:
        config.write(config_file)

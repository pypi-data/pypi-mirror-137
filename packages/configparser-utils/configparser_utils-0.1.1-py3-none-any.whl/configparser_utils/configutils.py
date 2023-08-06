"""
Typical utilities for configuration files
"""


import configparser


def get_config(path):
    """
    Getting configuration file

    path - path to config file
    """
    config = configparser.ConfigParser()
    config.read(path)
    return config


def update_setting(path, section, setting, value):
    """
    Update settings in config file

    path - path to config file
    section - section name
    setting - setting name
    value - setting value
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def get_setting(path, section, setting):
    """
    Get setting from configuration file

    path - path to config file
    section - section name
    setting - setting name
    """
    config = get_config(path)
    value = config.get(section, setting)
    return value

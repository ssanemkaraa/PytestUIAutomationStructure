import configparser
import os
from pathlib import Path

project_path = os.path.dirname(os.getcwd())

config_file_path = Path(project_path + "/utils/configs/config.ini")

config = configparser.ConfigParser()

print(config_file_path)


class Config:

    def __init__(self):
        print("Config initialized")

    @staticmethod
    def create_example_config():
        if not os.path.exists(os.path.dirname(config_file_path)):
            os.makedirs(os.path.dirname(config_file_path))

        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        config['driver'] = {}
        config['driver'] = {'base_url': 'google.com',
                            'implicity_wait': '5'}

        config['data'] = {}
        config['data'] = {'username': 'username',
                          'password': 'password'}

        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def get_config_sections():
        config.read(config_file_path)
        sections = config.sections()
        print(sections)
        return sections

    @staticmethod
    def get_config_details():
        config.read(config_file_path)
        sections = config.sections()
        for section in sections:
            print("----- " + section + " -----")
            for key in config[section]:
                value = config[section][key]
                print(key + " = " + value)

    @staticmethod
    def get_base_url():
        config.read(config_file_path)
        url = config.get('driver', 'base_url')
        print(url)
        return url

    @staticmethod
    def get_implicity_wait():
        config.read(config_file_path)
        wait = config.get('driver', 'implicity_wait')
        return wait

    @staticmethod
    def get_driver_path():
        config.read(config_file_path)
        path = config.get('driver', 'driver_path')
        return path

    @staticmethod
    def get_driver_name():
        config.read(config_file_path)
        driver_name = config.get('driver', 'driver_name')
        print(driver_name)
        return driver_name

    @staticmethod
    def get_data_username():
        config.read(config_file_path)
        data = config.get('data', 'username')
        return data

    @staticmethod
    def get_data_password():
        config.read(config_file_path)
        data = config.get('data', 'password')
        return data

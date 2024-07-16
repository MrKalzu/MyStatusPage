import configparser

class Config:
    def __init__(self, config_file):
        self.config_file = config_file

    def get_tokens(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        tokens = {}
        if 'Servers' in config:
            tokens = {server: config['Servers'][server] for server in config['Servers']}
        return tokens

    def get_config(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_file)
        config = {}
        if 'Config' in config_parser:
            config = {key: config_parser['Config'][key] for key in config_parser['Config']}
        return config


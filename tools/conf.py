import ConfigParser


def configure(config_file):
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    return config

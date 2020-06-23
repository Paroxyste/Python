import configparser

def read_params(config, section, parameter, defaultValue):
    if(section in config):
        try:
            value = config.get(section, parameter)

        except configparser.NoOptionError:
            value = defaultValue

    else:
        value = defaultValue

    print(parameter + ' : ' + str(value))

    return value
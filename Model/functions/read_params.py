import configparser

def read_params(config, section, parameter, default):
    if(section in config):
        try:
            value = config.get(section, parameter)

        except configparser.NoOptionError:
            value = default

    else:
        value = default

    print(parameter + ' : ' + str(value))

    return value
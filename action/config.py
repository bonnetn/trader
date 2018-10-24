import configparser


def parse_config():
    """
    Read config.ini to fetch the credentials of the user.
    :return: login, password and url
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    cred = config["credentials"]
    general = config["general"]
    url = general["url"].strip('"')

    print("Loaded config.")
    return cred["login"], cred["password"], url

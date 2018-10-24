import configparser


def parse_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    cred = config["credentials"]
    general = config["general"]
    url = general["url"].strip('"')

    print("Loaded config.")
    return cred["login"], cred["password"], url

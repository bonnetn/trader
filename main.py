import configparser

from selenium import webdriver

TIMEOUT = 10

PLAY_BUTTON_XPATH = '//*[@id="accountlist"]/div/div[1]/div[2]/div/div/div[11]/button'
COUNTER_METAL_XPATH = '//*[@id="resources_metal"]'
COUNTER_CRYSTAL_XPATH = '//*[@id="resources_crystal"]'
COUNTER_DEUTERIUM_XPATH = '//*[@id="resources_deuterium"]'
COUNTER_ENERGY_XPATH = '//*[@id="resources_energy"]'


def launch_bot():
    username, password, url = parse_config()
    driver = webdriver.Chrome()
    driver.get(url)
    print("Launched browser.")

    login_sequence(driver, username, password)

    ctx = {}
    extract_resources(driver, ctx)

    driver.close()

    print(ctx)


def parse_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    cred = config["credentials"]
    general = config["general"]
    url = general["url"].strip('"')

    print("Loaded config.")
    return cred["login"], cred["password"], url


def login_sequence(driver, username, password):
    driver.find_element_by_id("ui-id-1").click()
    driver.find_element_by_id("usernameLogin").send_keys(username)
    driver.find_element_by_id("passwordLogin").send_keys(password)

    old_value = driver.find_element_by_id('loginSubmit').text
    driver.find_element_by_id("loginSubmit").click()
    print("Logged in.")

    driver.implicitly_wait(TIMEOUT)
    driver.find_element_by_xpath(PLAY_BUTTON_XPATH).click()
    print("Chose the universe.")

    driver.switch_to.window(driver.window_handles[1])
    print("Switched to new tab.")


def extract_resources(driver, ctx):
    driver.implicitly_wait(TIMEOUT)
    ctx["resources"] = {
        "metal": driver.find_element_by_xpath(COUNTER_METAL_XPATH).text,
        "crystal": driver.find_element_by_xpath(COUNTER_CRYSTAL_XPATH).text,
        "deuterium": driver.find_element_by_xpath(COUNTER_DEUTERIUM_XPATH).text,
        "energy": driver.find_element_by_xpath(COUNTER_ENERGY_XPATH).text,
    }


if __name__ == "__main__":
    launch_bot()

from action import constants


def login_sequence(driver, username, password):
    driver.find_element_by_id("ui-id-1").click()
    driver.find_element_by_id("usernameLogin").send_keys(username)
    driver.find_element_by_id("passwordLogin").send_keys(password)

    driver.find_element_by_id("loginSubmit").click()
    print("Logged in.")

    driver.find_element_by_xpath(constants.PLAY_BUTTON_XPATH).click()
    print("Chose the universe.")

    driver.switch_to.window(driver.window_handles[1])
    print("Switched to new tab.")

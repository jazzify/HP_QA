# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from hillsqa.private_settings import DRIVER, USER, PASSWORD


def start_driver():
    """
    Runs Chrome webdriver from selenium, and log in AEM.
    """
    DRIVER.get("https://author-colgate-prod.adobecqms.net")
    user = DRIVER.find_element_by_name("j_username")
    password = DRIVER.find_element_by_name("j_password")
    user.send_keys(USER)
    password.send_keys(PASSWORD)
    password.send_keys(Keys.RETURN)

from selenium import webdriver

# GENERAL SETTINGS
CHROME_WEBDRIVER = "path/to/chromedriver.exe"
CHROME_EXE_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
DRIVER = webdriver.Chrome(executable_path=CHROME_WEBDRIVER)

# SITE SETTINGS
HILLS = " Title Expected"
DOMAIN = 'domain.com'
PROPERTY_LINK = 'url'

# USER SETTINGS
USER = "user"
PASSWORD = "password"

AUTH = (USER, PASSWORD)

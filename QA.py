# -*- coding: utf-8 -*-
import webbrowser
import requests
from bs4 import BeautifulSoup
from qautils.screenshot import highlight
from qautils.driver import start_driver, DRIVER
from qautils.fixers import fix_pg_title, fix_nav_title, U_T_O
from hillsqa.private_settings import CHROME_EXE_PATH, HILLS, AUTH, PROPERTY_LINK, DOMAIN


start_driver()

URLS_TO_OPEN = set()
URLS_404 = set()


with open('urls.txt', 'r') as urls_file:
    URL_LIST = [line.strip('\n') for line in urls_file]

    for url in URL_LIST:
        print('\n\nTesting url:', URL_LIST.index(url) + 1, 'of', len(URL_LIST))
        print('UTO:', len(URLS_TO_OPEN), " , 404:", len(URLS_404))
        new_url = PROPERTY_LINK + url.split(PROPERTY_LINK[0:42], 1)[1].replace('.html?wcmmode=disabled', '')
        prod_site = requests.get(new_url, auth=AUTH)
        prod_soup = BeautifulSoup(prod_site.text, 'html.parser')

        try:
            if 'Internal Server Error' in prod_soup.body.h1.text:
                print(404)
                URLS_404.add(url)

        except AttributeError:
            inputs = prod_soup.select('div.coral-TabPanel-content input')
            description = prod_soup.find('textarea').text
            for inp in inputs:
                try:
                    if inp['name'] == './jcr:title':
                        main_title = inp['value']
                    if inp['name'] == './pageTitle':
                        pg_title = inp['value']
                    if inp['name'] == './navTitle':
                        nav_title = inp['value']
                except:
                    pass

            # Page Title
            if pg_title is '':
                print('PAGE TITLE NOT FOUND')
                prod_site = requests.get(url, auth=AUTH)
                prod_soup = BeautifulSoup(prod_site.text, 'html.parser')
                heading_1 = prod_soup.h1.text
                print(f"<h1> tag found: {heading_1}")
                open_pg_title = input('Open and fix? (y/c/n): ')
                if open_pg_title == 'y':
                    webbrowser.get(CHROME_EXE_PATH).open_new_tab(url)
                    webbrowser.get(CHROME_EXE_PATH).open_new_tab(new_url)
                elif open_pg_title == 'c':
                    DRIVER.get(new_url)
                    custom_pg_title = input('Please provide the page title: ')
                    custom_pg_title += HILLS
                    page_title_input = DRIVER.find_element_by_name('./pageTitle')
                    page_title_input.send_keys(custom_pg_title)
                    fix_nav_title(new_url)

            elif (not pg_title.endswith(HILLS)) and (not pg_title.endswith(f'{HILLS} ')):
                DRIVER.get(new_url)
                fix_pg_title(new_url)

            elif nav_title == '' or not nav_title in pg_title:
                DRIVER.get(new_url)
                fix_nav_title(new_url)

            else:
                if ' hillpet' in pg_title.lower() or ' hillspet' in pg_title.lower():
                    print('Weird')
                    URLS_TO_OPEN.add(new_url)
                print("PT:", pg_title)
                print("NT:", nav_title)

            # Description
            if ' hillpet' in description.lower() or ' hillspet' in description.lower():
                if f' {DOMAIN}' in description.lower():
                    print('Description:', description)
                else:
                    print('Description failed')
                    URLS_TO_OPEN.add(new_url)
            elif description.lower().strip() == '':
                print('DESCRIPTION NOT FOUND')
                description = highlight(DRIVER, url, new_url)
                if description:
                    description_field = DRIVER.find_element_by_name('./jcr:description')
                    description_field.clear()
                    description_field.send_keys(description)
                    DRIVER.find_element_by_id('shell-propertiespage-saveactivator').click()
                else:
                    open_fix_description = input('Open and fix description manually? (y/n): ')
                    if open_fix_description.lower() == 'y':
                        webbrowser.get(CHROME_EXE_PATH).open_new_tab(url)
                        webbrowser.get(CHROME_EXE_PATH).open_new_tab(new_url)

            else:
                print('Description:', description)

    UTO = URLS_TO_OPEN.union(U_T_O)
    if UTO:
        for url in UTO:
            webbrowser.get(CHROME_EXE_PATH).open_new_tab(url)

    if URLS_404:
        print("\n404 URLS:")
        for url in URLS_404:
            print(url)

input()

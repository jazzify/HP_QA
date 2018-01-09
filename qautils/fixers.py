# -*- coding: utf-8 -*-
import webbrowser
import requests
from bs4 import BeautifulSoup
from time import sleep
from .driver import DRIVER
from hillsqa.private_settings import CHROME_EXE_PATH, HILLS, AUTH

URLS_TO_OPEN = set()

HP_LIST = [ '| Hill´s Pet',   '| Hill´s Pet ',
            '| Hill´s pet',   '| Hill´s pet ',
            '|  Hill´s Pet',  '|  Hill´s Pet ',
            '| Hills Pet',    '| Hills Pet ',
            '| hillspet',     '| hillspet ',
            "|  Hill's Pet",  "|  Hill's Pet ",
            "| HIll's Pet",   "| HIll's Pet ",
            "| HIll´s Pet",   "| HIll´s Pet ",
            "|  Hill´s pet",  "|  Hill´s pet ",
            "|  Hill's pet",  "|  Hill's pet ",
            "- Hill's Pet",   "- Hill's Pet ",
            "- hillspet.lt",  "- hillspet.lt ",
            "| Hill's",       "| Hill's ",
            "| Хиллс",        "| Хиллс ",
            " | Hill’s Pet",  " | Hill’s Pet ",
            " | Hills' Pet",  " | Hills' Pet ",
            " | Hill's Pets", " | Hill's Pets "
        ]



def fix_no_pg_title(edit_link, stage_link):
    """
    Try to fix the pg_title if it not exist.
    """
    print('No page title found')
    prod_site = requests.get(stage_link, auth=AUTH)
    prod_soup = BeautifulSoup(prod_site.text, 'html.parser')
    try:
        heading_h1 = prod_soup.h1.text
        print(f"<h1> tag found: {heading_h1}")
    except AttributeError:
        print('NO <h1> tag in the site')

    open_pg_title = input('Open and fix? (y/c/a/n): ')

    if open_pg_title == 'y':
        webbrowser.get(CHROME_EXE_PATH).open_new_tab(stage_link)
        webbrowser.get(CHROME_EXE_PATH).open_new_tab(edit_link)
        return True

    elif open_pg_title == 'c':
        if DRIVER.current_url is not edit_link:
            DRIVER.get(edit_link)
        custom_pg_title = input('Please provide the page title: ')
        custom_pg_title += HILLS

    elif open_pg_title == 'a':
        if DRIVER.current_url is not edit_link:
            DRIVER.get(edit_link)
        custom_pg_title = heading_h1 + HILLS

    page_title_input = DRIVER.find_element_by_name('./pageTitle')
    page_title_input.send_keys(custom_pg_title)

    fix_nav_title(edit_link)


def fix_pg_title(link):
    """
    Try to fix the pg_title if is not well writen.
    """
    print('FIXING Page Title')
    page_title_input = DRIVER.find_element_by_name('./pageTitle')

    pg_title = page_title_input.get_attribute('value')

    for option in HP_LIST:
        if pg_title.endswith(option):
            fixed_pg_title = pg_title.replace(option, HILLS)
            page_title_input.clear()
            page_title_input.send_keys(fixed_pg_title)
            break
    else:
        print('ERROR', pg_title)
        URLS_TO_OPEN.add(link)
        return False

    fix_nav_title(link, no_save=True)

    DRIVER.find_element_by_id('shell-propertiespage-saveactivator').click()


def fix_nav_title(link, no_save=False):
    """
    Try to fix the nav_title if is none or if is not well writen.
    """
    page_title_input = DRIVER.find_element_by_name('./pageTitle')
    nav_title_input = DRIVER.find_element_by_name('./navTitle')

    pg_title = page_title_input.get_attribute('value')
    nav_title = nav_title_input.get_attribute('value')

    if ('/dog-breeds/' in link) or ('/cat-breeds/' in link):
        print('FIXING Nav Title')
        if nav_title != pg_title:
            nav_title_input.clear()
            nav_title_input.send_keys(pg_title)
    else:
        print('FIXING Nav Title')
        fixed_nav_title = pg_title.replace(HILLS, '')
        if nav_title != fixed_nav_title:
            nav_title_input.clear()
            nav_title_input.send_keys(fixed_nav_title)

    if not no_save:
        DRIVER.find_element_by_id('shell-propertiespage-saveactivator').click()


    print("PT:", pg_title)
    print("NT:", nav_title)

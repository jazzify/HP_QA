# -*- coding: utf-8 -*-
from time import sleep
from .driver import DRIVER

U_T_O = set()

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
            "- Hill's Pet",   "- Hill's Pet ", "| Hill's"
        ]

def fix_pg_title(link):
    """
    redirects de driver to the link given and try to fix the pg_title
    """
    print('FIXING Page Title')
    page_title_input = DRIVER.find_element_by_name('./pageTitle')

    pg_title = page_title_input.get_attribute('value')

    for option in HP_LIST:
        if pg_title.endswith(option):
            fixed_pg_title = pg_title.replace(option, "| Hill's Pet")
            page_title_input.clear()
            page_title_input.send_keys(fixed_pg_title)
            break
    else:
        print('ERROR', pg_title)
        U_T_O.add(link)
        return False

    fix_nav_title(link, no_save=True)

    DRIVER.find_element_by_id('shell-propertiespage-saveactivator').click()


def fix_nav_title(link, no_save=False):
    """
    redirects de driver to the link given and try to fix the nav_title
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
        fixed_nav_title = pg_title.replace(" | Hill's Pet", '')
        if nav_title != fixed_nav_title:
            nav_title_input.clear()
            nav_title_input.send_keys(fixed_nav_title)

    if not no_save:
        DRIVER.find_element_by_id('shell-propertiespage-saveactivator').click()


    print("PT:", pg_title)
    print("NT:", nav_title)

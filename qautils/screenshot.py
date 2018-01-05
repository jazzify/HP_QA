from io import BytesIO
from PIL import Image

def highlight(driver, url, new_url):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver.get(url)
    try:
        element = driver.find_element_by_css_selector('#content div.paragraphSystem div.component-content p:first-of-type')
        description_text = element.text
        print('DESCRIPTION FOUND:', description_text)
        if element.text:
            driver = element._parent
            def apply_style(style):
                """
                Highlights the selected element
                """
                driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)
            apply_style("background: #81D4FA; border: 2px solid #0277BD;")

            driver.execute_script("window.scrollTo(0, 550);")
            img = driver.get_screenshot_as_png()
            img = Image.open(BytesIO(img))
            img.show()
            driver.get(new_url)
            open_and_fix = input('Auto fix description? (y/c/n): ')
            if open_and_fix.lower() == 'y':
                return description_text
            elif open_and_fix.lower() == 'c':
                custom_description_text = input('Please provide description text: ')
                return custom_description_text
            else:
                return False
        else:
            print("Element have no text")
            return False
    except:
        driver.get(new_url)
        print("Can't hightlight the item")
        return False

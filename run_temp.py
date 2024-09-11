# %reset -f

import os
with open(os.path.join(os.getcwd(), 'initialize.py')) as f:
    exec(f.read(), globals())
driver = browser_driver
driver_el = browser_driver_el
step=''
sleep=0
# clean_memory()
# =============================================================================
url = 'https://lotangroup.com'
url = 'https://www.otomoto.pl/'
url = 'https://geekforce.io/'
url = 'https://app.woodpecker.co/login'
url = 'https://woodpecker.co'
url = 'https://otomoto.pl'
url = 'https://olx.pl'
url = 'https://allegro.pl'
url = 'https://pl.linkedin.com/'
url = 'https://x.com'
url = 'https://example.com'
url = 'https://woodpecker.co/signup/'
url = "https://www.tripadvisor.com/Restaurant_Review-g274812-d13189858-Reviews-Iggy_Pizza-Wroclaw_Lower_Silesia_Province_Southern_Poland.html"
url = 'https://www.google.com/recaptcha/api2/demo' # no
url = 'https://2captcha.com/demo/recaptcha-v2' #no
url = 'https://2captcha.com/demo/mtcaptcha' # no
url = 'https://2captcha.com/demo/recaptcha-v3' # ok
url = 'https://accounts.google.com/'
driver.get(url)

# =============================================================================

# =============================================================================
# driver_el.elements, driver_el.df_e = elements_data(driver)
# df_e = driver_el.df_e
# =============================================================================
print(page_names(driver, driver_el, step=''))


task = "Go to https://2captcha.com/demo/recaptcha-v3 and solve the puzzle - finish once done."
name_task = task.replace(' ','_')
for s in ['.','!','-','(','[',')',']',':','/']:name_task = name_task.replace(s,'')

print(name_task)


# =============================================================================
# button ='Dalej'
# link = 'Current URL'
# box = 'Adres e-mail lub telefon'
# scroll= 500
# step = 'Describe the page'
# task = 'Login'
# print(browser_link_goto(step, link))
# print(browser_button_click(step, button))
# print(browser_box_fill(step, box, 'xxx'))
# print(browser_scroll(step, scroll))
# print(browser_vision(step, task))
# 
# query = 'Winobranie Zielona Gora 2024'
# print(web_page(url,''))
# print(web_search(query, method='concise'))
# print(web_search(query, method='detailed'))
# =============================================================================
# =============================================================================
# driver.close()
# driver.quit()
# =============================================================================

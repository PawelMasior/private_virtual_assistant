import os
import numpy as np
import pandas as pd
import re
import time
import random
import openai
from openai import OpenAI
from datetime import datetime
from copy import deepcopy
from settings.gcp import img_to_bucket, blobs_clean
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = OpenAI()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from tools.selenium_plt import *

bool_filter_elements = True
bool_filter_plt = True

el_set = {
    'button': {
        'action': 'button',
        'col': {'name': 'button','x_loc': 'x', 'y_loc': 'y'},
        'msg': 'buttons to click', 
        'nr': 50,
        },
    'generic': {
        'action': 'button',
        'col': {'name': 'button','x_loc': 'x', 'y_loc': 'y'},
        'msg': 'generic elements (potential buttons) to click', 
        'nr': 20,
        },
    'DisclosureTriangle': {
        'action': 'button',
        'col': {'name': 'button','x_loc': 'x', 'y_loc': 'y'},
        'msg': 'DisclosureTriangles to click', 
        'nr': 20,
        },
    'listitem': {
        'action': 'button',
        'col': {'name': 'button','x_loc': 'x', 'y_loc': 'y'},
        'msg': 'listitem to click', 
        'nr': 40,
        },
    'tab': {
        'action': 'button',
        'col': {'name': 'button', 'x_loc': 'x', 'y_loc': 'y'},
        'msg': 'tab to click',
        'nr': 20,
        },
    'combobox': {
        'action': 'box',
        'col': {'name': 'box', 'idx': 'idx', 'value': 'text'},
        'msg': 'comboboxes to send text to', 
        'nr': 25,
        },
    'textbox': {
        'action': 'box',
        'col': {'name': 'box', 'idx': 'idx', 'value': 'text'},
        'msg': 'textboxes to send text to', 
        'nr': 25,
        },
    'link': {
        'action': 'link',
        'col': {'name': 'link', 'href': 'url'},
        'msg': 'links to navigate to', 
        'nr': 20,
        },
    'article': {
        'action': 'article',
        'col': {'name': 'article', 'x': 'x', 'y': 'y'},
        'msg': 'articles to go to', 
        'nr': 20,
        },
}

script_elements = """
const elements = Array.from(document.querySelectorAll('*')).filter(el => {
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return rect.top >= 0 && 
        rect.bottom <= 0 + window.innerHeight &&
        rect.height > 5 &&
        rect.width > 5 &&
        style.display !== 'none' &&
        style.visibility !== 'hidden' &&
        parseFloat(style.opacity) > 0 &&
        el.aria_role !== null;        
});
"""
#window.scrollY
script_elements_loc = f"""
{script_elements}

return elements.map(el => {{
    return {{
        alt: el.getAttribute('alt'),
        tag_name: el.tagName,
        x: el.getBoundingClientRect().x,
        y: el.getBoundingClientRect().y,
        height: el.getBoundingClientRect().height,
        width: el.getBoundingClientRect().width,
    }};
}});
"""
# =============================================================================
# Functions
# =============================================================================
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    # options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    # options.add_argument('--disable-application-cache')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-search-engine-choice-screen")    

    driver = webdriver.Chrome(options=chrome_options)
    driver.save_screenshot(os.path.join('monitor',  'prtscn', 'cuts.png'))
    driver.save_screenshot(os.path.join('monitor',  'prtscn', 'elements.png'))
    driver.save_screenshot(os.path.join('monitor',  'prtscn', 'names.png'))
    driver.save_screenshot(os.path.join('monitor',  'prtscn', 'view.png'))
    return driver

# ZAINICJOWANA KLASA DO PAMIECI ELEMENTOW
class init_elements:
    # print(f"init_elements:: init_elements")
    def __init__(self, elements=None, df_e=None, agent_folder=None):
        self.elements = elements if elements is not None else []
        self.df_e = df_e if df_e is not None else pd.DataFrame()    
        self.agent_folder = agent_folder if agent_folder is not None else ''
        
    def update(self, elements_new, df_e_new):
        self.elements = elements_new
        self.df_e = df_e_new
  
# POBRANIE ELEMENTOW I JSON ICH LOKALIZACJ ZA POMOCA SKRYPTOW
def elements_get(driver, max_attempts=3, sleep_attempts=2):
    # print("elements_get:: elements_get")
    attempts = 0
    while attempts < max_attempts:
        try:
            elements = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "*")))
            elements_raw = driver.execute_script(f"{script_elements}return elements;")
            elements_loc = driver.execute_script(script_elements_loc)
            df_loc = pd.DataFrame(elements_loc)
            if bool_filter_elements:
                aria_role = [el.aria_role for el in elements_raw]# if el.aria_role in el_set.keys()]
                elements = [el for i,el in enumerate(elements_raw) if aria_role[i] in el_set.keys()]
                df_loc = df_loc[df_loc.index.isin([i for i, el in enumerate(elements_raw) 
                                                   if aria_role[i] in el_set.keys()])]
                df_loc = df_loc.reset_index(drop=True)
            else:
                elements = elements_raw
            # print(f"elements_get:: elements:: {len(elements)}")
            return elements, df_loc
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(sleep_attempts + random.uniform(0.1, 1))
    return [], pd.DataFrame()

# AGREGACJA ELEMENTOW I FILTROWANIE
def elements_df(driver, elements, df_loc, step=''):
    # print("elements_df:: elements_df")
    random.seed(123)
    if len(elements):
        # print(f"elements_df:: elements:: {len(elements)}")
        data = []
        for i, el in enumerate(elements):
            size = el.size
            location = el.location
            data += [{
                'id': el.id,
                'aria_role': el.aria_role,
                'name': el.accessible_name, 
                'text': el.text,
                'value': el.get_attribute("value"),
                'href': el.get_attribute('href'),
                }]
        df_all = pd.DataFrame(data)
        df_all = df_all.merge(df_loc, left_index=True, right_index=True, how='left')
        df_all.loc[df_all['name'] == '', 'name'] = df_all.loc[df_all['name'] == '', 'text']
        # print(f"elements_df:: df_all:: {df_all.shape[0]}")

        df_all['idx'] = df_all.index
        df_all['space'] = df_all['height']*df_all['width']
        df_all['y_loc'] = df_all['y'] + df_all['height']*random.uniform(0.3, .7)
        df_all['x_loc'] = df_all['x'] + df_all['width']*random.uniform(0.3, .7)
        df_all.loc[len(df_all)] = {
            'id': 'current_url',
            'name': 'Current URL',
            'href': driver.current_url,
            'aria_role': 'link',
            'x': -1,
            'y': -1,
            'height': 0,
            'width': 0,
            }
        df_all = df_all.sort_values(by=['y', 'x'])
        df = deepcopy(df_all)
        # print(f"elements_df:: df:: {df.shape[0]}")

        if 'link' in df['aria_role'].unique():
            name = 'link'
            df_in = deepcopy(df)
            df_in = df_in[(df_in['aria_role'].isin([name])) &
                          (df_in['name'] != '') &
                          (df_in['href'].str.len() < 400) &
                          (df_in['href'] == df_in['href'])]
            df_in = df_in[(~df_in['href'].duplicated())]
            if not bool_filter_plt: 
                df_out = df[(df['aria_role'].isin([name])) & (~df['id'].isin(df_in['id']))]
                filter_draw(driver, df_in, df_out, name)
            
            df_other = df[df['aria_role'].isin([k for k in el_set.keys() if k != name])]
            if df_other.shape[0] > 0:
                overlap = []
                for i,r in df_other.iloc[:,:].iterrows(): 
                    overlap += [df_in[
                        (df_in['x'] >= r['x']) & 
                        (df_in['y'] >= r['y']) &
                        (df_in['x']+df_in['width'] <= r['x']+r['width']) &
                        (df_in['y']+df_in['height'] <= r['y']+r['height'])
                        ].shape[0] + df_in[
                            (df_in['x'] <= r['x']) & 
                            (df_in['y'] <= r['y']) &
                            (df_in['x']+df_in['width'] >= r['x']+r['width']) &
                            (df_in['y']+df_in['height'] >= r['y']+r['height'])
                            ].shape[0]]# + 1*(r['aria_role'] in ['article', 'textbox', 'combobox'])]
                df_other = df_other[(np.array(overlap)==0) |
                                    (df_other['aria_role'].isin(['article', 'textbox', 'combobox']))]
            df = pd.concat([df_other, df_in])
        # print(f"elements_df:: link:: {df.shape[0]}")

        if 'button' in df['aria_role'].unique():
            name = 'button'
            df_in = deepcopy(df)
            df_in = df_in[(df_in['aria_role'].isin([name])) &
                          (df_in['name'] != '')]
            df_in['duplicated'] = 1
            df_in['duplicated'] = df_in.groupby(by=['name'])['duplicated'].cumsum()
            df_in = df_in[df_in['duplicated'] <= 3]
            df_out = df[(df['aria_role'].isin([name])) & (~df['id'].isin(df_in['id']))]        
            if not bool_filter_plt: filter_draw(driver, df_in, df_out, name)
            df = pd.concat([df[~df['aria_role'].isin([name])], df_in])
            
        if 'listitem' in df['aria_role'].unique():
            name = 'listitem'            
            df_in = deepcopy(df)
            df_in = df_in[(df_in['aria_role'].isin([name]))]
            df_in.loc[df_in['name'] == '', 'name'] = df_in.loc[df_in['name'] == '', 'value']
            df_in = df_in[~df_in['name'].duplicated()]
            df_out = df[(df['aria_role'].isin([name])) & (~df['id'].isin(df_in['id']))]
            if not bool_filter_plt: filter_draw(driver, df_in, df_out, name)
            df = pd.concat([df[~df['aria_role'].isin([name])], df_in])
            
        if 'textbox' in df['aria_role'].unique():
            name = 'textbox'            
            df_in = deepcopy(df)
            df_in = df_in[(df_in['aria_role'].isin([name]))]
            df_out = df[(df['aria_role'].isin([name])) & (~df['id'].isin(df_in['id']))]
            if not bool_filter_plt: filter_draw(driver, df_in, df_out, name)
            df = pd.concat([df[~df['aria_role'].isin([name])], df_in])

        if 'article' in df['aria_role'].unique():
            name = 'article'            
            df_in = deepcopy(df)
            df_in = df_in[(df_in['aria_role'].isin([name]))]
            df_in = df_in[~df_in['name'].duplicated()]
            df_out = df[(df['aria_role'].isin([name])) & (~df['id'].isin(df_in['id']))]
            if not bool_filter_plt: filter_draw(driver, df_in, df_out, name)
            df = pd.concat([df[~df['aria_role'].isin([name])], df_in])

        if 'generic' in df['aria_role'].unique():
            name = 'generic'
            window_space = driver.get_window_size()['width']*driver.get_window_size()['height']
            df_in = deepcopy(df)
            df_in = df_in[(df_in['aria_role'].isin([name])) & 
                          (df_in['space'] > 0) &
                          (df_in['space']/window_space < .015) &
                          (df_in['space']/window_space > .0001) &
                          (df_in['text'] != '') &
                          (df_in['text'] != ' ') &
                          ((df_in['text'].str.len() > 3)) &
                          ((df_in['text'].str.len() < 50))
                          ]
            if df_in.shape[0]: 
                df_in = df_in[~df_in['text'].duplicated()]
                df_in['name'] = df_in['text'].str.replace("\n"," ")
                overlap = []
                df_other = df[df['aria_role'].isin([k for k in el_set.keys() if k != name])]
                for i,r in df_in.iloc[:,:].iterrows(): 
                    overlap += [df_other[
                        (df_other['x'] >= r['x']) & 
                        (df_other['y'] >= r['y']) &
                        (df_other['x']+df_other['width'] <= r['x']+r['width']) &
                        (df_other['y']+df_other['height'] <= r['y']+r['height'])
                        ].shape[0] + df_other[
                            (df_other['x'] <= r['x']) & 
                            (df_other['y'] <= r['y']) &
                            (df_other['x']+df_other['width'] >= r['x']+r['width']) &
                            (df_other['y']+df_other['height'] >= r['y']+r['height'])
                            ].shape[0] + df_in[
                                (df_in['idx'] != r['idx']) &
                                (df_in['x'] >= r['x']) & 
                                (df_in['y'] >= r['y']) &
                                (df_in['x']+df_in['width'] <= r['x']+r['width']) &
                                (df_in['y']+df_in['height'] <= r['y']+r['height'])
                                ].shape[0]]
                df_in = df_in[np.array(overlap)==0]
            df_out = df[(df['aria_role'].isin([name])) & (~df['id'].isin(df_in['id']))]
            if not bool_filter_plt: filter_draw(driver, df_in, df_out, name)
            df = pd.concat([df[~df['aria_role'].isin([name])], df_in])
        # print(f"elements_df:: filter:: {df.shape[0]}")

        if not bool_filter_plt: 
            for name in df['aria_role'].unique():
                if name not in ['link', 'button', 'article', 'listitem','textbox', 'generic']:
                    df_in = deepcopy(df)
                    df_in = df_in[(df_in['aria_role'].isin([name]))]
                    df_out = df[(df['aria_role'].isin([name])) & (~df['id'].isin(df_in['id']))]
                    filter_draw(driver, df_in, df_out, name)

        df = df.sort_values(by=['y', 'x'])
        df['name'] = df['name'].replace('\n',' ', regex=True)
        df['role'] = df['aria_role']
        for k,v in el_set.items(): df['role'] = df['role'].replace(k,v['action'])
        # group by role get first
        
        # print(f"elements_df:: to_draw:: {df.shape[0]}")
        try:
            elements_draw(driver, df)
        except: print(f"Error: Image prepration")
        # print(f"elements_df:: draw:: {df.shape[0]}")
        # df_e = df_e[~df_e['aria_role'].isin(['image', 'img', 'svg', 'Video'])]

    else:
        df = pd.DataFrame(columns=['id', 'aria_role', 'name', 'text', 'value', 'href', 'alt', 'height',
               'tag_name', 'width', 'x', 'y', 'idx', 'space', 'y_loc', 'x_loc'])
    return df

# elements_get + elements_df (KILKA ATTEMPTOW ZEBY BYLO SZYBCIEJ I UJELO DYNAMICZNE ELEMENTY)
def elements_data(driver, max_attempts=3, sleep_attempts=3):
    # print("elements_data:: elements_data")
    attempts = 0
    while attempts < max_attempts:
        try:
            elements, df_loc = elements_get(driver)
            # print(f"elements_data:: elements:: {len(elements)}")
            df_e = elements_df(driver, elements, df_loc)
            # print(f"elements_data:: df_e:: {df_e.shape[0]}")
            return elements, df_e
        except:
            attempts += 1
            time.sleep(sleep_attempts + random.uniform(0.1, 1))
    return [], pd.DataFrame()

# NAZWY ELEMENTOW JAKO WIADOMOSC DLA AGENTA
def elements_names(driver, df_e):
    # print("elements_names:: elements_names")
    # print(f"elements_names:: df_e:: {df_e.shape[0]}")
    pageYOffset = driver.execute_script("return window.pageYOffset")
    msg = f'## Current page elements:'
    msg+= f"\n(Scrolled already: {pageYOffset}px down)" if pageYOffset else ''
    
    roles = [r for r in el_set.keys() if r in df_e['aria_role'].unique()]
    for role in roles:
        action = el_set[role]['action']
        names = list(df_e[df_e['aria_role']==role]['name'].astype(str))
        hrefs = list(df_e[df_e['aria_role']==role]['href'].astype(str))
        msg+= f"""\n\n### {role.capitalize()}: {len(names)} {el_set[role]['msg']}:\n\t"""
        if action == 'link':
            hrefs = list(df_e[df_e['aria_role']==role]['href'].astype(str))
            msg+= f"""\n\t""".join([f"""{action}='{n}', url='{h}'""" for n,h in zip(names, hrefs)])
        elif action == 'box':
            hrefs = list(df_e[df_e['aria_role']==role]['value'].astype(str))
            msg+= f"""\n\t""".join([f"""{action}='{n}', value='{h}'""" for n,h in zip(names, hrefs)])            
        else:
            msg+= f"""\n\t""".join([f"""{action}='{n}'""" for n in names])
    return msg

def prtscn_url(driver_el):
    agent_folder = driver_el.agent_folder
    blobs_clean(agent_folder)
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    file_source = os.path.join('monitor',  'prtscn', f'view'+'.png')
    file_destination = f'{agent_folder}/prtscn/raw_{time_str}.png'
    url = img_to_bucket(file_source, file_destination)
    
    file_source = os.path.join('monitor',  'prtscn', f'cuts'+'.png')
    file_destination = f'{agent_folder}/prtscn/elements_{time_str}.png'
    url_elements = img_to_bucket(file_source, file_destination)
    return url, url_elements

def elements_llm(driver, driver_el, tx_e):
    url, url_elements = prtscn_url(driver_el)
    
    prompt = f"""
    Analyze the elements on the current page with image urls.
    
    # Return:
    1. Current page describtion
    2. The most important, useful, and popular element names for the user.
    
    ## Each element has unchanged name value.
        
    ## Constraints:
    - **Focus** on elements essential for everyday tasks, navigation, search results, and settings; (and search result if applicable based on image). 
    - **Include** search results (if applicable based on image).
    - **Disregard** elements that are less frequently used or non-critical.. 
    - **Output** elements with their original name values without any alterations.
    - **Optimize** output in terms of number of tokens.
    - **Context** focus on current prompt and image urls only.
        
    ## Suggest If Applicable (do not mention if you dont see any):
    - **Pop-up windows:** If you see pop-up window currently blocking the view, suggest how to close it.
    - **Cookie Acceptance:** If you see is a button to accept cookies, suggest clicking it.
    {tx_e}
    """
    # print(prompt)
    response = client_openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "user",
          "content": [
              { "type": "image_url", "image_url": {"url": url,},},
            #   { "type": "image_url", "image_url": {"url": url_elements,},},
              { "type": "text", "text": prompt,},
             ],
        }
      ],
      max_tokens=4000,
      temperature=0.
    )
    msg = response.choices[0].message.content
    # print(msg)
    return msg

def scroll_text(driver, scroll_limit=3000):
    window_height = driver.get_window_size()['height']
    page_height = driver.execute_script("return document.body.scrollHeight")
    pageYOffset = driver.execute_script("return window.pageYOffset")
    px_up = max(pageYOffset, 0)
    px_dw = max(page_height - window_height - pageYOffset,0)
    msg = ''
    if px_up > 50 or (px_dw > 50 and px_up<scroll_limit):
        if px_up > 50 and (px_dw > 50 and px_up<scroll_limit):
            msg = f'\nScroll up or down (max up: {px_up}px, down: {px_dw}px)'
        elif px_up > 50:
            msg = f'\nScroll up (max: {px_up}px)'
        else:
            msg = f'\nScroll down (max: {px_dw}px)'
        msg += f' only if current page content is not enough to proceed and you did not scroll more than {scroll_limit}px already.'
    else:
        msg = '\nScrolling not applicable!'
    return msg

# TUTAJ WYRZUCAM INFO O ELEMENTACH
def page_names(driver, driver_el, step=''):
    # print(f"page_names:: page_names")
    # print(f"page_names:: id(driver_el):: {id(driver_el)}")
    elements, df_e = elements_data(driver)
    driver_el.update(elements, df_e)

    tx_e = elements_names(driver, df_e)
    if df_e.shape[0]<=100:  msg = tx_e
    else: msg = elements_llm(driver, driver_el, tx_e)
    msg+= scroll_text(driver)
    msg+= "\nYou can use vision tools for better understaning visible elements and next steps - if needed."
    return msg

def page_vision(driver, driver_el, step='', task=''):
    page_draw(driver, msg='Using vision to identify best elements', c = (99, 0, 199), step=step)
    elements, df_e = elements_data(driver)
    driver_el.update(elements, df_e)
    tx_e = elements_names(driver, df_e)
    url, url_elements = prtscn_url(driver_el)
    
    if df_e.shape[0] >= 60:
        prompt = f"""    
        # Provide:
        1. Brief description of the current page content.
        2. Information where is the user, ex is logged in, current stage etc
        3. If there are any problems on the page - identify them and suggest how to resolve.
        3. List actions on the current page that relate to the Step & Task.
            Next to actions list down elements names and urls.
            
        ## Step: {step}
        ## Task: {task}
    
        **Actions**
        - Make sure suggested actions too choose from elements and are efficient.
        - Prioritize and order relevant actions and elements.
        - Action elements have their name value.
    
        **Constraints:**
        - **Information:** Use only the information from the screenshot URLs and current page element names.
        - **Consistent:** Do not invent or change element names.
        - **Format:** Keep lists sufficiently long and unchanged.
        - **Context:** focus on current prompt and image urls only.
    
        ## Suggest If Applicable (do not mention if you dont see any):
        - **Pop-up windows:** Only if you see pop-up window currently blocking the view, suggest how to close it.
        - **Cookie Acceptance:** Only if you see is a button to accept cookies, suggest clicking it.
        - **Generic Buttons:** If generic elements are actual buttons, specify those.
    
        {tx_e}
        """
    else:
        prompt = f"""    
        # Provide:
        1. Brief description of the current page content.
        2. Information where is the user, ex is logged in, current stage etc
        3. If there are any problems on the page - identify them and suggest how to resolve.

        ## Step: {step}
        ## Task: {task}
    
        **Constraints:**
        - **Information:** Use only the information from the screenshot URLs and current page elements.
        - **Consistent:** Do not invent or change element names.
        - **Context:** focus on current prompt and image urls only.
    
        ## Suggest If Applicable (do not mention if you dont see any):
        - **Pop-up windows:** Only if you see pop-up window currently blocking the view, suggest how to close it.
        - **Cookie Acceptance:** Only if you see is a button to accept cookies, suggest clicking it.
        - **Generic Buttons:** If generic elements are actual buttons, specify those.
    
        {tx_e}
        """
    # print(prompt)
    response = client_openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "user",
          "content": [
              { "type": "image_url", "image_url": {"url": url,},},
              { "type": "image_url", "image_url": {"url": url_elements,},},
              { "type": "text", "text": prompt,},
             ],
        }
      ],
      max_tokens=2500,
      temperature=0.
    )
    msg = response.choices[0].message.content
    if not df_e.shape[0] >= 60: msg += f"""\n\n{tx_e}"""
    # print(msg)
    return msg

def page_scroll(driver, driver_el, step='', scrollBy=500, scroll_limit=3000, direction='down'):
    window_height = driver.get_window_size()['height']
    page_height = driver.execute_script("return document.body.scrollHeight")
    pageYOffset = driver.execute_script("return window.pageYOffset")
    px_up = max(pageYOffset, 0)
    px_dw = max(page_height - window_height - pageYOffset,0)
    msg = ""
    if direction == 'down':
        if scrollBy > px_dw:
            msg = f"Error: you can only scroll down max {px_dw}px."
        elif px_up > scroll_limit:
            msg = f"Error: you already scrollded down {px_up}px - try something else!."
        else: px = scrollBy + random.uniform(-50, 50)
    elif direction == 'up':
        if scrollBy > px_up:
            msg = f"Error: you can only scroll up max {px_up}px."
        else: px = -scrollBy + random.uniform(-50, 50)
    else:
        msg = f"Error: 'direction' can have only 'up' or 'down' value."
    
    if not 'Error' in msg: 
        scroll_draw(driver, y_scroll=px, step=step)
        driver.execute_script(f"window.scrollBy(0, {px});")
        msg = f"""Success: Scrolled by {scrollBy}"""
        msg+= '\n\n' + page_names(driver, driver_el, step=step)
    return msg

def check_name(driver_el, name='', role=''):
    df_e = driver_el.df_e
    df_role = df_e[df_e['role']==role]
    if df_role.shape[0]:
        names = list(df_e[df_e['role']==role]['name'].astype(str))
        if sum(df_role['name'] == name):
            msg = 'Ok'
        else:
            msg = f"Error: there is no {role} available of name: '{name}'"
            msg+= f"""\n**{role.capitalize()}** there are {len(names)} {el_set[role]['msg']}:\n\t"""
            if role == 'link':
                hrefs = list(df_e[df_e['aria_role']==role]['href'].astype(str))
                msg+= f"""\n\t""".join([f"""({role})='{n}', url='{h}'""" for n,h in zip(names, hrefs)])
            else:
                msg+= f"""\n\t""".join([f"""({role})='{n}'""" for n in names])
    else:
        msg = f"Error: there is no {role} available on the current page"
    return msg

def link_goto(driver, driver_el, step='', sleep=0, name=''):
    page_draw(driver, msg=f"Go to: {name}", c = (0, 255, 0), step=step)
    if 'https' in name:
        url = name
    else:
        msg_check = check_name(driver_el, name, 'link')
        msg_check+= "\n(or provide https url in name input)"
        if "Error" in msg_check: return msg_check
        # elements, df_e = elements_data(driver)
        # driver_el.update(elements, df_e)
        elements = driver_el.elements
        df_e = driver_el.df_e
        # do: add element selection, optional argument
        r = df_e[(df_e['role']=='link') & (df_e['name'] == name)].iloc[0]
        url = r['href']
    msg = ''
    try: 
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) # await
        time.sleep(sleep + random.uniform(0.1, 1))
        msg = f'Success: Opened link: {driver.current_url}'
        msg+= '\n\n' + page_names(driver, driver_el, step=step)
    except WebDriverException as e:
        if 'net::ERR_NAME_NOT_RESOLVED' in str(e): 
            msg = f"Error: Unable to resolve the {url}"
        else:
            msg = f"Error: {str(e)[:200]}"
    return msg

def msg_df(df):
    # msg += ':\n'+dumps(loads(df.to_json(orient="records")))    
    return'\n\t'.join(['{'+', '.join([f'{k}: {v}' for k,v in r.to_dict().items()])+'}' for i,r in df.iterrows()])

def box_fill(driver, driver_el, step='', sleep=0, name='', text='', hit_return=False):
    msg_check = check_name(driver_el, name, 'box')    
    if "Error" in msg_check: return msg_check

    elements, df_e = elements_data(driver)
    driver_el.update(elements, df_e)
    # do: add element selection, optional argument
    r = df_e[(df_e['role']=='box') & (df_e['name'] == name)].iloc[0]
    elements = driver_el.elements
    df_e = driver_el.df_e
    msg = ''
    try:
        el = elements[int(r['idx'])]
        box_draw(driver, x=el.location['x'], y=el.location['y'], height=el.size['height'], width=el.size['width'], text=text, step=step)
        el.clear()
        el.send_keys(f"{text}")
        msg = f"Success: Filled box '{name}' with: {text}"
        time.sleep(random.uniform(0.1, 1))
        if hit_return: 
            el.send_keys(Keys.RETURN)
            time.sleep(sleep + random.uniform(0.1, 1))
            msg += f' and hit RETURN.\n'
            msg += page_names(driver, driver_el, f'Identify current page elements.')
        else:
            elements, df_e = elements_data(driver)
            driver_el.update(elements, df_e)
        
            cols = {'name': 'name', 'aria_role': 'type', 'value': 'text'}
            df_role = df_e[df_e['role'].isin(['box'])]
            df_role = df_role[cols.keys()].rename(columns=cols)
            df_empty = df_role[(df_role['text'].isin(['', 'None'])) | (df_role['text'].isna())]
            df_empty = df_empty[['name','type']]
            df_filled = df_role[~df_role.index.isin(df_empty.index)]
            
            if df_filled.shape[0]:
                msg+= f"\nFilled boxes:\n\t{msg_df(df_filled)}"
            else: msg+= f"\nFilled boxes: none"
            if df_empty.shape[0]:
                msg+= f"\nEmpty boxes:\n\t{msg_df(df_empty)}"
            else: msg+= f"\nEmpty boxes: none"        
        return msg
    except Exception as e:
        msg = f"Error: {str(e)[:200]}"
    return msg

def button_click(driver, driver_el, step='', sleep=0, name=''):
    msg_check = check_name(driver_el, name, 'button')    
    if "Error" in msg_check: return msg_check    
    
    elements, df_e = elements_data(driver)
    driver_el.update(elements, df_e)
    # do: add element selection, optional argument
    r = df_e[(df_e['role']=='button') & (df_e['name'] == name)].iloc[0]
    msg = ''
    try:
        button_draw(driver, x=r['x_loc'], y=r['y_loc'], r=10, step=step)
        driver.execute_script(f"el = document.elementFromPoint({r['x_loc']}, {r['y_loc']}); el.click();")
        time.sleep(sleep + random.uniform(0.1, 1))
        msg = f"Success: Clicked on {name}"
        msg+= '\n\n' + page_names(driver, driver_el, step=step)
    except Exception as e:
        msg = f"Error: {str(e)[:200]}"
    return msg
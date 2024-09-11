import os
import numpy as np
import pandas as pd
from copy import deepcopy
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

el_color = {
    'link': (0, 255, 0),                    # Green
    'button': (255, 80, 80),                # Light Red
    'listitem': (255, 0, 0),                # Standard Red
    'DisclosureTriangle': (200, 0, 0),      # Darker Red
    'checkbox': (150, 0, 0),                # Darker Red (with less intensity)
    'tab': (255, 100, 100),                 # Light Red (different shade)
    'generic': (128, 0, 128),               # Purple
    'textbox': (0, 0, 255),                 # Blue
    'combobox': (128, 255, 255),            # Light Cyan
    'article': (255, 255, 0),               # Yellow
}

role_color = {
    'link': (0, 255, 0),                # Green
    'button': (255, 0, 0),            # Light Red
    'box': (0, 0, 255),                 # Blue
    'generic': (128, 0, 128),           # Purple
    'article': (255, 215, 0)            # Golden Yellow
}

def img_action(func):
    def wrapper(driver, *args, **kwargs):
        w = int(driver.execute_script('return window.innerWidth'))
        h = int(driver.execute_script('return window.innerHeight'))
        driver.save_screenshot(os.path.join('monitor', 'prtscn', f'view'+'.png'))
        img = Image.open(os.path.join('monitor', 'prtscn', f'view'+'.png')).resize((w, h))
        draw = ImageDraw.Draw(img, "RGBA")

        func(draw, img, *args, **kwargs)

        img.save(os.path.join('monitor',  'prtscn', 'action.png'))
        img.save(os.path.join('monitor', 'actions', f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'))
    return wrapper

@img_action
def page_draw(draw, img, msg='Listing elements', c=(255, 0, 0), step=''):
    draw.rectangle((0, 0, img.width, img.height), fill=c+(40,), outline=c, width=3)
    draw.text((5, 5), f'{msg}', fill=c, font=ImageFont.load_default(44))
    draw.text((5, 60), f'Step: {step}', fill=(0, 0, 0), font=ImageFont.load_default(32))

@img_action
def scroll_draw(draw, img, y_scroll, step=''):
    c = (128, 255, 255)
    draw.rectangle((0, 0, img.width, img.height), fill=c+(40,))
    draw.rectangle((0, 0, img.width, y_scroll), fill=(165, 165, 165)+(150,), outline=c+(150,), width=3)
    draw.rectangle((0, y_scroll, img.width, img.height), fill=c+(0,), outline=c, width=3)
    draw.text((5, y_scroll-100), f' |\n |\n\|/ Scrolling down by {np.round(y_scroll,2)}', fill=c, font=ImageFont.load_default(44))
    draw.text((5, 60), f'Step: {step}', fill=c, font=ImageFont.load_default(32))

@img_action
def box_draw(draw, img, x=0, y=0, height=0, width=0, text='', step=''):
    draw.rectangle((0, 0, img.width, img.height), fill=role_color['box']+(40,))
    draw.rectangle((x, y, x + width, y + height), outline=role_color['box'], width=3)
    draw.text((x, y), text, fill=role_color['box'], font=ImageFont.load_default(17))
    draw.text((5, 60), f'Step: {step}', fill=role_color['box'], font=ImageFont.load_default(32))

@img_action
def button_draw(draw, img, x=0, y=0, r=10, step=''):
    draw.rectangle((0, 0, img.width, img.height), fill=role_color['button']+(40,))
    draw.ellipse((x - r, y - r, x + r, y + r), fill=role_color['button'])
    draw.text((5, 60), f'Step: {step}', fill=role_color['button'], font=ImageFont.load_default(32))

@img_action
def link_draw(draw, img, msg='', url='', step=''):
    draw.rectangle((0, 0, img.width, img.height), fill=role_color['link']+(40,))
    draw.text((5, 5),  f'{msg} to {url}', fill=role_color['link'], font=ImageFont.load_default(44))
    draw.text((5, 60), f'Step: {step}', fill=role_color['link'], font=ImageFont.load_default(32))


def filter_draw(driver, df_g, df_g_o, name='generic', step=''):
    w = int(driver.execute_script('return window.innerWidth'))
    h = int(driver.execute_script('return window.innerHeight'))
    driver.save_screenshot(os.path.join('monitor', 'prtscn', f'view'+'.png'))
    img = Image.open(os.path.join('monitor', 'prtscn', f'view'+'.png')).resize((w, h))
    draw = ImageDraw.Draw(img, "RGBA")
    
    try: c = el_color[name]
    except: c = (0, 255, 255)
    for i,r in df_g_o.iterrows():
        x, y, height, width = r['x'], r['y'], r['height'], r['width']
        draw.rectangle((x, y, x + width, y + height), fill=(165, 165, 165)+(20,), outline=(165, 165, 165)+(150,), width=2)    
    for i,r in df_g.iterrows():
        x, y, height, width = r['x'], r['y'], r['height'], r['width']
        draw.rectangle((x, y, x + width, y + height), fill=c+(50,), outline=c, width=2)  
    img.save(os.path.join('monitor','filter', f'{name}.png'))

def legend_draw(draw, img, role_color):
    legend_y_0 = 275
    legend_y_1 = 100
    draw.rectangle((0, img.size[1]-legend_y_0, 120, img.size[1]-legend_y_1), fill=(255, 255, 255))
    for i, (k, c) in enumerate(role_color.items()):
        draw.rectangle((10, img.size[1]-legend_y_0+10 +i*32, 30, 
                        img.size[1]-legend_y_0+30 +i*32), fill=c+(0,), outline=c+(200,), width=2)
        draw.text((40, img.size[1]-legend_y_0+15 +i*31), k, fill=(0, 0, 0), font=ImageFont.load_default(17))
        
def elements_draw(driver, df_e):
    w = int(driver.execute_script('return window.innerWidth'))
    h = int(driver.execute_script('return window.innerHeight'))
    driver.save_screenshot(os.path.join('monitor', 'prtscn', f'view'+'.png'))
    img = Image.open(os.path.join('monitor', 'prtscn', f'view'+'.png')).resize((w, h))
    draw = ImageDraw.Draw(img, "RGBA")

    # highlight
    df = deepcopy(df_e)
    for i,r in df.iterrows():
        if r['role'] in list(role_color.keys()):
            x, y, height, width, c = r['x'], r['y'], r['height'], r['width'], role_color[r['role']]
            draw.rectangle((x, y, x + width, y + height), fill=c+(0,), outline=c+(200,), width=2)
    legend_draw(draw, img, role_color)
    img.save(os.path.join('monitor', 'prtscn', f'elements'+'.png'))

    # names
    draw.rectangle((0, 0, img.width, img.height), fill=(255, 255, 255)+(255,), width=3)
    for i,r in df.iterrows():
        if r['role'] in list(role_color.keys()):
            x, y, height, width, c = r['x'], r['y'], r['height'], r['width'], role_color[r['role']]
            draw.rectangle((x, y, x + width, y + height), fill=c+(0,), outline=c+(200,), width=2)
            draw.text((x, y), str(r['name']), fill=(0,0,0), font=ImageFont.truetype("DejaVuSans.ttf", size=14))
    legend_draw(draw, img, role_color)
    img.save(os.path.join('monitor', 'prtscn', f'names'+'.png'))  
    
    # cuts
    img_view = Image.open(os.path.join('monitor', 'prtscn', f'view'+'.png')).resize((w, h))  
    draw.rectangle((0, 0, img.width, img.height), fill=(255, 255, 255)+(255,), width=3)
    for i,r in df.iterrows():
        if r['role'] in list(role_color.keys()):
            x, y, height, width, c = r['x'], r['y'], r['height'], r['width'], role_color[r['role']]
            if x>=0: 
                img_cut = img_view.crop((x, y, x + width, y + height)).convert("RGBA")
                img.paste(img_cut, (int(x),int(y)), img_cut)
                draw.rectangle((x, y, x + width, y + height), fill=c+(0,), outline=c+(200,), width=2)
    legend_draw(draw, img, role_color)
    img.save(os.path.join('monitor', 'prtscn', f'cuts'+'.png')) 




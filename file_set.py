import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from PIL import Image


assets_dir = os.path.join(os.getcwd(), 'assets')

if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)


def download_page_with_css(url, download_dir='assets'):
    response = requests.get(url)
    html_content = response.text

    page_name = 'index.html'
    html_path = os.path.join(download_dir, page_name)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')
    css_files = []

    for link in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, link.get('href'))
        css_files.append(css_url)

    for css_url in css_files:
        css_response = requests.get(css_url)
        css_filename = os.path.basename(urlparse(css_url).path)
        css_path = os.path.join(download_dir, css_filename)
        
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_response.text)

def pic_resize(path_to_pic):
    new_size = (1920, 1080)
    with Image.open(path_to_pic) as img:
        resized_img = img.resize(new_size)

        resized_img.save(assets_dir + '\\bg.png')

def virtina_resize(path_to_pic):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    # if re.match(regex, url) is not None:

    image = Image.open(path_to_pic)

    width, height = image.size

    left = 494
    upper = 256
    right = width - 796
    lower = height

    cropped_image = image.crop((left, upper, right, lower))

    cropped_image.save(assets_dir + '\\baner.png')
    
    
if __name__ == '__main__':
    url = 'https://steamcommunity.com/id/VerhovnaVlada/'
    download_page_with_css(url)
    pic_resize(assets_dir + '\\bg.jpg')
    virtina_resize(assets_dir + '\\bg.png')
    


import requests
from bs4 import BeautifulSoup
import sys

def get_html(url):
    res = requests.get(url)
    return res.text

def write_html(html, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

def translate_en_html(html, tags):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(tags)
    for element in elements:
        translate_api_url = 'https://script.google.com/macros/s/AKfycbxYOApQm2RXoRhRoLGsuu8chdqqq_1fgNZfUPBBkUKXN_ibmAgfRbShmL2YMXSPpeey4Q/exec?text='+element.text+'&source=en&target=ja'
        translated = requests.get(translate_api_url).json().get('text')
        ruby = soup.new_tag('ruby')
        ruby.string = element.text
        rt = soup.new_tag('rt')
        rt.string = translated
        ruby.append(rt)
        element.string = ''
        element.append(ruby)
    return str(soup)

def main(args):
    target_url = args[1]
    target_file = ''
    if len(args) >= 3:
        target_file = args[2]
    else:
        target_file = 'translated.html'
    html = get_html(target_url)
    tags = ['p', 'dt'] 
    translated_html = translate_en_html(html, tags)
    write_html(translated_html, target_file)

if __name__ == '__main__':
    args = sys.argv
    main(args)
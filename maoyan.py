import requests
import re
import time
import json


def get_one_page(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?href.*?title="(.*?)".*?"star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',
        re.S)
    result = re.findall(pattern, html)
    for i in result:
        yield {
            'title': i[0],
            'actor': i[1].strip()[3:],
            'time': i[2],
            'score': i[3] + i[4]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    for i in range(0, 110, 10):
        url = 'http://maoyan.com/board/4' + '?offset=' + str(i)
        html = get_one_page(url)
        for i in parse_one_page(html):
            print(i)
            write_to_file(i)
        time.sleep(1)


main()

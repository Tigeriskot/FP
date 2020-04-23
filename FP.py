import requests
from bs4 import BeautifulSoup
import json
import re

def get_html(url):
    r = requests.get(url)
    return r


def get_content(html):
    listOlTag = []
    soup = BeautifulSoup(html, 'html.parser')
    i = 1
    while i < 7:
        listOlTag.append(getTeg(soup.find_all(f'h{i}')))
        i = i + 1
    listOlTag.append(getTeg(soup.find_all('p')))
    listOlTag.append(getTeg(soup.find_all('img')))
    listOlTag = list(filter(None, listOlTag))
    return listOlTag


def getTeg(tags):
    flag = True
    teglist = []
    for tag in tags:
        if flag:
            teglist.append(tag.name)
            flag = False
        if tag.name == "img":
            teglist.append((tag.get('src')))
        else:
            teglist.append((tag.text).strip("\n").strip("\r").strip(" "))
    return teglist

def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        pageOpen = True
        tags = get_content(html.text)
        paragraphs_template = []
        images_template = []
        headers_dic = {}
        for tag in tags:

            if re.search(r'h\d', f'{tag[0]}'):
                temp = tag[0]
                tag.remove(tag[0])
                headers_dic[temp] = tag
            elif tag[0] == 'p':
                tag.remove(tag[0])
                paragraphs_template = tag
            elif tag[0] == 'img':
                tag.remove(tag[0])
                images_template = tag

        to_json = {'page_exist': pageOpen , 'headers': headers_dic, 'paragraphs': paragraphs_template, "images": images_template}
        with open('output.json', 'w') as f:
            json.dump(to_json, f, indent=2, ensure_ascii=False)
        with open('output.json') as f:
            print(f.read())

    else:
        print('Сайт открыть не удалось')


def main():
    #тестовые примеры
    listURl = ['https://vk.com/garik_kotok', 'https://dataart.ru/company/history', 'http://www.amm.vsu.ru/students/asset/']
    for url in listURl:
        parse(url)
    choice = 0
    while choice != 1:
        print('Если хотите выйте нажмите - 1')
        print('Если хотите ввести URl для парсинга нажмите - 2')
        choice = input()
        if choice == '2':
            print('Введите URl сайта:')
            you_Url = input()
            parse(you_Url)
        elif choice == '1':
            break


if __name__ == main():
    main()

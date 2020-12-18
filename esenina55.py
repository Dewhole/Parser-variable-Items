import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib
import fake_useragent
import transliterate



HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0', 'accept': '*/*'}

HOST = 'https://2676270.ru'


# Получение необходимой страницы
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



# Считаем количество страниц в категории/каталоге
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paginationTo = soup.find('ul', class_='pagination')
    if paginationTo:
        paginationTo = soup.find('ul', class_='pagination')
        pagination = paginationTo.find_all('a') 
        print(pagination)
        return int(pagination[-2].get_text())  
    else:
        return 1
        

# Получаем необходимые поля/данные
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('ul', class_='catalog')

    catalog = []

    for item in items:
        anchors = item.find_all("a")
        for a in anchors:

            # Получаем страницу товара
            titles = HOST + a.get('href')
            print(titles)

            # Обращаемся к этой странице
            html2 = get_html(titles)
            # Получаем суп
            soup2 = BeautifulSoup(html2.text, 'html.parser')
            
            # парсим ссылку на картинку
            soupimage = soup2.find('div', class_='product_img')
            imagelink = HOST + soupimage.find('img').get('src') 

            # парсим категорию товара
            soupkategory = soup2.find('div', class_='breadcrumbs')
            kategory = soupkategory.findAll('a')[4].text

            # парсим описание, заменяемые значения можно заменить на словарь
            souptext = soup2.find('div', class_='info')
            text = souptext.findAll('p')[0:3]
            text1 = str(text)
            text2 = text1.replace('[<p><span>', '')
            text3 = text2.replace('</span>', '')
            text4 = text3.replace('</p>', '')           
            text5 = text4.replace('</p>]', '')   
            text6 = text5.replace(']', '')   
            text7 = text6.replace('<p><span>', '')     
            print(text7)

            # Ищем все вариации товара
            soupvarimgs = soup2.findAll('div', class_='img')
            
            # Счётчик цикла
            counter = 0

            # пробегаемся по всем вариациям товара
            for soupvar in soupvarimgs:
                counter += 1 
   
                # Парсим ссылка на картинку вариации
                soupvarimg = HOST + soupvar.find('a').get('href')
                
                # Парсим цвет вариации
                colors = soupvar.find('img').get('alt')

                # Транслит цвета для изменения названия товара, в зависимости от цвета вариации
                colorsTranslite = transliterate.translit(colors, reversed=True)
                if counter == 1:
                    title = soup2.find('h1', class_='heading').get_text(strip=True)
                else:
                    title = soup2.find('h1', class_='heading').get_text(strip=True) + ' ' + colorsTranslite

                # Добавляем полученные значения за проход по циклу в каталог и так до конца цикла
                catalog.append({
                    'title': title,
                    'kategory': kategory,
                    'image': imagelink,
                    'imageVar': soupvarimg,
                    'color': colors,
                    'text': text7,
                    'cost': soup2.find('div', class_='price').get_text(strip=True),
                    'visible': 'visible'
                        
                })
                    
        return catalog                    
            

            



# функция записи спарсенных значений в csv файл
def save_file(items, path):
    with open(path, 'w',  encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Категории', 'Имя', 'Изображения', 'Изображения2', 'Цвет', 'Описание', 'Базовая цена', 'Видимость в каталоге'])
        for item in items:
            writer.writerow([item['kategory'], item['title'], item['image'], item['imageVar'], item['color'], item['text'], item['cost'], item['visible']])

# Основная функция Создаём каталог
def parse():
    for URL in [
        
'https://2676270.ru/catalog/yarn/1419/'

    ]:

        html = get_html(URL)
        if html.status_code == 200:
            catalog = []
            pages_count = get_pages_count(html.text)
            for page in range (1, pages_count + 1):
                print(f'Парсинг страницы {page} {pages_count} {URL}...')
                html = get_html(URL, params={'PAGEN_1': page})
                catalog.extend(get_content(html.text))
                time.sleep(1)
            FILE = URL[33:-1] + 'ghk' + '.csv'   
            save_file(catalog, FILE)


            print(f'Получено {len(catalog)} товаров')
        else:
            print('Error')    





parse()



""" 'https://2676270.ru/catalog/yarn/92/',
'https://2676270.ru/catalog/yarn/93/',
'https://2676270.ru/catalog/yarn/1419/'
'https://2676270.ru/catalog/yarn/1677/',
'https://2676270.ru/catalog/yarn/2453/',
'https://2676270.ru/catalog/yarn/909/',
'https://2676270.ru/catalog/yarn/95/' """
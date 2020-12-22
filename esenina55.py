import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib
import fake_useragent
import transliterate
import datetime
from langdetect import detect

now = datetime.datetime.now()
date = now.strftime("%d-%m-%Y %H:%M")
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

            # парсим цену товара плюс наценка            
            cost = soup2.find('div', class_='price').get_text(strip=True)
            cost3 = cost.replace('руб.', '')
            cost33 = cost3.replace(' ', '')
            intcost = float(cost33)
            cost5 = intcost * 0.5 + intcost
            cost5 = float('{:.0f}'.format(cost5))
            cost7 = str(cost5)
            cost8 = cost7[:-2]


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
         

            
            # Ищем все вариации товара
            
            soupvarimgs = soup2.findAll('div', class_='img')
            
            # Счётчик цикла
            counter = 0

            colorsAtribute = []
            # пробегаемся по всем вариациям товара

            
            for soupvar in soupvarimgs:
                counter += 1 

                # Парсим ссылка на картинку вариации
                soupvarimg = soupvar.find('a')
                if soupvarimg:
                    soupvarimg = HOST + soupvar.find('a').get('href')
                else:
                    soupvarimg = ''
                
                # Парсим цвет вариации и добавляем в список
                colors = soupvar.find('img').get('alt')
                colorsAtribute.append(colors)
                


            
            # Записываем родительский товар
            colorsAtributeString = ', '.join(colorsAtribute)
            imagelink = HOST + soupimage.find('img').get('src') 
            title = soup2.find('h1', class_='heading').get_text(strip=True)
            Type = 'variable'  
            catalog.append({
                'title': title,
                'kategory': 'ПРЯЖА' + ' > ' + kategory,
                'image': imagelink,
                'text': text7,
                'cost': cost8,
                'visible': 'visible',
                'Type': Type,
                'SKU': title,
                'parent': '',
                'Attribute 1 name': 'Цвет',
                'Attribute 1 value(s)': colorsAtributeString,
            })        

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

            # парсим цену товара плюс наценка            
            cost = soup2.find('div', class_='price').get_text(strip=True)
            cost3 = cost.replace('руб.', '')
            cost33 = cost3.replace(' ', '')
            intcost = float(cost33)
            cost5 = intcost * 0.5 + intcost
            cost5 = float('{:.0f}'.format(cost5))
            cost7 = str(cost5)
            cost8 = cost7[:-2]


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
         

            
            # Ищем все вариации товара
            
            soupvarimgs = soup2.findAll('div', class_='img')
            
            # Счётчик цикла
            counter = 0

            colorsAtribute = []
            # пробегаемся по всем вариациям товара

            
            for soupvar in soupvarimgs:
                counter += 1 

                # Парсим ссылка на картинку вариации
                soupvarimg = soupvar.find('a')
                if soupvarimg:
                    soupvarimg = HOST + soupvar.find('a').get('href')
                else:
                    soupvarimg = ''
                
                # Парсим цвет вариации и добавляем в список
                colors = soupvar.find('img').get('alt')
                colorsAtribute.append(colors)
                

                # Транслит цвета для изменения названия товара, в зависимости от цвета вариации
                intcolors = colors.isdigit()
                if intcolors == True:
                    colorsTranslite = colors
                else:
                    detectLang = detect(colors)
                    if detectLang == 'ru':
                        colorsTranslite = transliterate.translit(colors, reversed=True)
                    else:
                        colorsTranslite = colors   
         
                

                parent = soup2.find('h1', class_='heading').get_text(strip=True)
                title = soup2.find('h1', class_='heading').get_text(strip=True) + ' ' + colorsTranslite
                Type = 'variation'
                parent = parent
                imagelink = soupvarimg
                # Добавляем полученные значения за проход по циклу в каталог и так до конца цикла
                catalog.append({
                    'title': title,
                    'kategory': 'ПРЯЖА' + ' > ' + kategory,
                    'image': imagelink,
                    'text': text7,
                    'cost': cost8,
                    'visible': 'visible',
                    'Type': Type,
                    'SKU': title,
                    'parent': parent,
                    'Attribute 1 name': 'Цвет',
                    'Attribute 1 value(s)': colors,
                })            

        return catalog      
        
            

            



# функция записи спарсенных значений в csv файл
def save_file(items, path):
    with open(path, 'w',  encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Категории', 'Имя', 'Изображения', 'Описание', 'Базовая цена', 'Видимость в каталоге', 'Type', 'SKU', 'Attribute 1 name', 'Attribute 1 value(s)', 'parent'])
        for item in items:
            writer.writerow([item['kategory'], item['title'], item['image'], item['text'], item['cost'], item['visible'], item['Type'], item['SKU'], item['Attribute 1 name'], item['Attribute 1 value(s)'], item['parent']])

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
            FILE = URL[32:-1] + date + '.csv'   
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
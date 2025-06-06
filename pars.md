Конечно, могу! Давайте сделаем интересно: я приведу **примеры парсинга с разных сайтов** и покажу, **как сохранять результат в разные форматы** — TXT, CSV, JSON и даже SQLite. Мы будем использовать Python и библиотеку `requests` + `BeautifulSoup`.

> 💡 Перед началом убедитесь, что установлены нужные библиотеки:
```bash
pip install requests beautifulsoup4
```

---

## 🌐 Пример 1: Парсинг цен с сайта (например, [https://books.toscrape.com](https://books.toscrape.com))

Это учебный сайт для парсинга. Соберём названия книг и их цены.

### ✅ Сохранение в текстовый файл `.txt`
```python
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('article', class_='product_pod')

with open('books.txt', 'w', encoding='utf-8') as f:
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        f.write(f'{title} - {price}\n')
```

---

## 📊 Пример 2: Парсинг новостей (например, [https://example-sites.com/news](https://example-sites.com/news))  
*(Предположим, что сайт существует)*

### ✅ Сохранение в CSV-файл
```python
import csv
import requests
from bs4 import BeautifulSoup

url = 'https://example-sites.com/news'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

news_items = soup.find_all('div', class_='news-item')

with open('news.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Заголовок', 'Дата'])

    for item in news_items:
        title = item.find('h2').text
        date = item.find('span', class_='date').text
        writer.writerow([title, date])
```

---

## 🧠 Пример 3: Парсинг информации о фильмах (например, [https://www.imdb.com/chart/top/](https://www.imdb.com/chart/top/))

### ✅ Сохранение в JSON-файл
```python
import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

movies = soup.select('li.ipc-metadata-list-summary-item')

data = []

for movie in movies[:5]:  # возьмем первые 5 фильмов
    title = movie.select_one('.ipc-title__text').text.split('.')[1].strip()
    rating = movie.select_one('.ipc-rating-star').text.split('(')[0].strip()
    data.append({
        'title': title,
        'rating': rating
    })

with open('top_movies.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
```

---

## 🗃️ Пример 4: Парсинг товаров (например, [https://fake-ecom.site/products](https://fake-ecom.site/products))  
(Вымышленный URL для примера)

### ✅ Сохранение в базу данных SQLite
```python
import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price TEXT
    )
''')

url = 'https://fake-ecom.site/products'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

items = soup.find_all('div', class_='product')

for item in items:
    name = item.find('h3').text
    price = item.find('span', class_='price').text
    cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (name, price))

conn.commit()
conn.close()
```

---

## 🎁 Полезные советы для вас с ребёнком:

- Попробуйте сделать **"парсер мультфильмов"**: спарсите список из любимых мультов и сохраните в CSV.
- Используйте **веб-сайт для практики**, например:
  - https://books.toscrape.com/
  - https://webscraper.io/test-sites/e-commerce
  - https://quotes.toscrape.com/

---

Хочешь, я помогу придумать проект под ваши интересы? Например, парсер анекдотов, стихов или космических новостей 🚀?

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as r
import re

urls = []
urls += ['http://books.toscrape.com/index.html'] # first page url
urls += [f'http://books.toscrape.com/catalogue/page-{i+2}.html' for i in range(49)] # paginated urls

# Grabs all detailed page urls for each book
def get_detail_page_urls(urls) -> list:
    
    book_urls = []
    
    for url in urls:
        soup = bs(r.get(urls[0]).content, 'html.parser')
        divs = soup.find_all('div', class_='image_container')
        book_urls.extend([urls[0][:-10] + div.a['href'] for div in divs])
        
    return book_urls
    
book_urls = get_detail_page_urls(urls)

# Cycles through each detail page, scrapes book data
def get_book_data(book_urls) -> dict:
    
    title, price, stock, rating, category, upc = [], [], [], [], [], []
    
    for url in book_urls:
        soup = bs(r.get(url).content, 'html.parser')
        
        title.append(soup.find('h1').text)
        price.append(float(soup.find('p', class_='price_color').text.replace('£', '')))
        stock.append(int(re.search(r'\d+', soup.find('p', class_='instock availability').text)[0]))
        rating.append(soup.find('p', class_='star-rating')['class'][1])
        category.append(soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip())
        upc.append(soup.find('table', class_='table-striped').find_all('td')[0].text)
        
    book_dict = {
        'title': title,
        'price': price,
        'stock': stock,
        'rating': rating,
        'category': category,
        'upc': upc,
    }
    
    return book_dict
    
data = pd.DataFrame(get_book_data(book_urls))

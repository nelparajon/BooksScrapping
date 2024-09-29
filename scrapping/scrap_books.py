from bs4 import BeautifulSoup 
import requests
from urllib.parse import urljoin

class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_categories(self):
        """
        Obtiene todas las categorías disponibles en el sitio web.
        Returns:
            List[Tuple[str, str]]: Lista de tuplas con el nombre y la URL de cada categoría.
        """
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        categories = []
        category_links = soup.find('ul', class_='nav-list').find('ul').find_all('a')
        for link in category_links:
            category_name = link.text.strip()
            category_url = urljoin(self.base_url, link['href'])
            categories.append((category_name, category_url))
        return categories

    def switch_page(self, soup, current_url):
        """
        Obtiene la URL de la siguiente página de la categoría actual.
        
        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup de la página actual.
            current_url (str): URL de la página actual.
            Returns:
                str: URL de la siguiente página, si existe. None en caso contrario.
        """
        next_page = soup.find('li', class_='next')
        if next_page:
            href = next_page.find('a')['href']
            link = urljoin(current_url, href)
            return link
        return None

    def scrap_rating(self, book):
        """
            Obtiene la calificación de un libro.
        Args:
            book (Tag): Objeto Tag de BeautifulSoup que contiene la información del libro.
        Returns:
            int: Calificación del libro, donde 0 es el valor por defecto si no se encuentra la calificación.
        """
        rating = book.find('p', class_='star-rating')['class'][1]
        ratings_map = {'One': 1, 'Two': 2, 'Three':3, 'Four':4, 'Five':5}
        return ratings_map.get(rating, 0)

    def scrap_all_books_from_category(self, category_name, category_url):
        """
            Obtiene todos los libros de una categoría.
        
        Args:
            category_name (str): nombre de la categoria a la que pertenecen los libros.
            category_url (str): URL de la página de la categoría.
        
            Returns:
                List[tuple[str, float, int, str]]: Lista de tuplas con el título, precio, calificación y categoría de cada libro.
        """
        
        n_page = 1
        books_list = []
        url = category_url
        while url:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            for book in books:
                title = book.h3.a['title']
                price_text = book.find('p', class_='price_color').text
                price = float(price_text.replace('£', '').replace('Â',''))
                rating = self.scrap_rating(book)
                books_list.append((title, price, rating, category_name))
            url = self.switch_page(soup, url)
            n_page += 1
        return books_list
    
    

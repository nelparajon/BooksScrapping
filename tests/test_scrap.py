import unittest
from bs4 import BeautifulSoup
from scrapping.scrap_books import Scraper

class TestScrapBooks(unittest.TestCase):

    def setUp(self):
        self.scrap_books = Scraper('http://books.toscrape.com/')

    def test_initialization(self):
        self.assertIsNotNone(self.scrap_books)

    def test_get_all_categories(self):
        result = self.scrap_books.get_all_categories()
        self.assertEqual(len(result), 50)
        self.assertIn("Travel", result)
        self.assertIn("Mistery", result)

    def test_switch_page(self):
        soup = BeautifulSoup('<li class="next"><a href="page2.html">Next</a></li>', 'html.parser')
        current_url = 'http://books.toscrape.com/catalogue/page-1.html'
        result = self.scrap_books.switch_page(soup, current_url)
        self.assertEqual(result, 'http://books.toscrape.com/catalogue/page2.html')
    
    def test_scrap_rating(self):
        book = BeautifulSoup('<p class="star-rating Three">Three</p>', 'html.parser')
        result = self.scrap_books.scrap_rating(book)
        self.assertEqual(result, 3)
    
    def test_scrap_all_books_from_category(self):
        category_name = 'Travel'
        category_url = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
        result = self.scrap_books.scrap_all_books_from_category(category_name, category_url)
        self.assertEqual(len(result), 11)
        self.assertIn(('It\'s Only the Himalayas', 45.17, 2, 'Travel'), result)
        self.assertIn(('Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond', 49.43, 4, 'Travel'), result)



if __name__ == "__main__":
    unittest.main()

from data.database_manager import DatabaseManager
from scrapping.scrap_books import Scraper
from data.config_db import db_path

class DataPipeline:
    def __init__(self, base_url):
        self.scraper = Scraper(base_url)
        self.db_manager = DatabaseManager(db_path)

    def run(self):
        categories = self.scraper.get_all_categories()
        if categories:
            for category_name, category_url in categories:
                books = self.scraper.scrap_all_books_from_category(category_name, category_url)
                if books:
                    for book in books:
                        title, price, rating, category = book
                        self.db_manager.add_book(title, price, rating, category)             
                else:
                    print(f"No se encontraron libros para la categoría '{category_name}'.")
        else:
            print("No se encontraron categorías.")
        self.db_manager.close()
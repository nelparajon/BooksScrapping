import unittest
import sqlite3
from unittest import mock
from unittest.mock import patch
import time
from data.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para cada prueba.
        Utiliza una base de datos SQLite en memoria para aislar las pruebas.
        """
        self.db_manager = DatabaseManager(':memory:')
    
    def tearDown(self):
        """
        Limpieza después de cada prueba.
        Cierra la conexión a la base de datos.
        """
        self.db_manager.close()
    
    def test_connection_established(self):
        """
        Verifica que la conexión a la base de datos se haya establecido correctamente.
        """
        self.assertIsNotNone(self.db_manager.connection, "La conexión a la base de datos no se estableció.")
        self.assertIsNotNone(self.db_manager.cursor, "El cursor de la base de datos no se creó.")
    
    def test_create_tables(self):
        """
        Verifica que las tablas 'categories' y 'books' se hayan creado correctamente.
        """
        self.db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in self.db_manager.cursor.fetchall()]
        self.assertIn('categories', tables, "La tabla 'categories' no se creó.")
        self.assertIn('books', tables, "La tabla 'books' no se creó.")
    
    def test_add_category_new(self):
        """
        Verifica que agregar una nueva categoría funcione correctamente.
        """
        category_name = 'Ficción'
        category_id = self.db_manager.add_category(category_name)
        self.assertIsInstance(category_id, int, "El ID de la categoría no es un entero.")
        
        self.db_manager.cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        result = self.db_manager.cursor.fetchone()
        self.assertIsNotNone(result, "La categoría no se agregó a la base de datos.")
        self.assertEqual(result[0], category_name, "El nombre de la categoría no coincide.")
    
    def test_add_category_existing(self):
        """
        Verifica que agregar una categoría que ya existe retorne el mismo ID.
        """
        category_name = 'No Ficción'
        first_id = self.db_manager.add_category(category_name)
        second_id = self.db_manager.add_category(category_name)
        self.assertEqual(first_id, second_id, "IDs diferentes para la misma categoría existente.")
    
    def test_add_book_with_new_category(self):
        """
        Verifica que agregar un libro con una nueva categoría funcione correctamente.
        """
        title = 'Libro de Ciencia'
        price = 29.99
        rating = 4
        category_name = 'Ciencia'
        
        self.db_manager.add_book(title, price, rating, category_name)
        
        self.db_manager.cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        category = self.db_manager.cursor.fetchone()
        self.assertIsNotNone(category, "La categoría no se agregó correctamente.")
        category_id = category[0]
        
        self.db_manager.cursor.execute("SELECT title, price, rating, category_id FROM books WHERE title = ?", (title,))
        book = self.db_manager.cursor.fetchone()
        self.assertIsNotNone(book, "El libro no se agregó a la base de datos.")
        self.assertEqual(book[0], title, "El título del libro no coincide.")
        self.assertEqual(book[1], price, "El precio del libro no coincide.")
        self.assertEqual(book[2], rating, "La calificación del libro no coincide.")
        self.assertEqual(book[3], category_id, "El ID de la categoría del libro no coincide.")
    
    def test_add_book_with_existing_category(self):
        """
        Verifica que agregar un libro a una categoría existente funcione correctamente.
        """
        category_name = 'Historia'
        category_id = self.db_manager.add_category(category_name)
        
        title = 'Libro de Historia'
        price = 19.99
        rating = 5
        
        self.db_manager.add_book(title, price, rating, category_name)
        
        self.db_manager.cursor.execute("SELECT title, price, rating, category_id FROM books WHERE title = ?", (title,))
        book = self.db_manager.cursor.fetchone()
        self.assertIsNotNone(book, "El libro no se agregó a la base de datos.")
        self.assertEqual(book[0], title, "El título del libro no coincide.")
        self.assertEqual(book[1], price, "El precio del libro no coincide.")
        self.assertEqual(book[2], rating, "La calificación del libro no coincide.")
        self.assertEqual(book[3], category_id, "El ID de la categoría del libro no coincide.")
    
    def test_close_connection(self):
        """
        Verifica que la conexión a la base de datos se cierre correctamente.
        """
        self.db_manager.close()
        with self.assertRaises(sqlite3.ProgrammingError, msg="La conexión no se cerró correctamente."):
            self.db_manager.cursor.execute("SELECT 1")
    
    def test_add_category_invalid_input(self):
        """
        Verifica que agregar una categoría con un nombre inválido (por ejemplo, None) maneje correctamente el error.
        """
        with self.assertRaises(sqlite3.IntegrityError, msg="No se lanzó IntegrityError para una categoría inválida."):
            self.db_manager.add_category(None)
    
    def test_add_book_missing_fields(self):
        """
        Verifica que agregar un libro con campos faltantes (por ejemplo, sin título) maneje correctamente el error.
        """
        category_name = 'Matemáticas'
        with self.assertRaises(sqlite3.IntegrityError, msg="No se lanzó IntegrityError para un libro con campos faltantes."):
            self.db_manager.add_book(None, 25.99, 4, category_name)


if __name__ == '__main__':
    unittest.main()

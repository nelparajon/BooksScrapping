import sqlite3
import time

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()
        self.create_tables()
    
    def connect(self):
        """
            Establece la conexión a la base de datos.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print("CONEXION A LA BASE DE DATOS EXTABLECIDA CON ÉXITO")
            return self.connection
            
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def create_tables(self):
        """
            crea las tablas de la base de datos si no existen.
        
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                rating INTEGER NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        self.connection.commit()

    def add_category(self, category_name):
        """
            Añade una categoría a la base de datos si no existe.
        Args:
            category_name (str): nombre de la categoría.
        Returns:
            int: id de la categoría con lastrowid si se añade, id de la categoría si ya existe.
        """
    
        self.cursor.execute('''
            SELECT id FROM categories WHERE category_name = ?
        ''', (category_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute('''
                INSERT INTO categories (name) VALUES (?)
            ''', (category_name,))
            self.connection.commit()
            return self.cursor.lastrowid

    def add_book(self, title, price, rating, category_name):
        """
            Añade un libro a la base de datos.
        Args:
            title (str): titulo del libro.
            price (float): precio del libro.
            rating (int): calificación del libro.
            category_name (str): nombre de la categoría a la que pertenece el libro.
            
        """
        category_id = self.add_category(category_name)
        retry_count = 5
        for attempt in range(retry_count):
            try:
                self.cursor.execute('''
                    INSERT INTO books (title, price, rating, category_id) VALUES (?, ?, ?, ?)
                ''', (title, price, rating, category_id))
                self.connection.commit()
                
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    print(f"Database is locked, retrying {attempt + 1}/{retry_count}...")
                    time.sleep(1)
                else:
                    raise

    def close(self):
        self.connection.close()
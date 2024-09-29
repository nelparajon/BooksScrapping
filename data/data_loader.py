import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, db_conn) -> None:
        """
            Inicializa el objeto DataLoader. Carga la conexión a la bd y el dataframe.
        """
        self.db_conn = db_conn
        self.df = None

    def load_books_df(self):
        """
            Carga el dataframe con la información de los libros.
        """
        try:
            self.df = pd.read_sql_query("SELECT * FROM books", self.db_conn)
            print("DATOS DE LIBROS CARGADOS")
            return self.df
        except Exception as e:
            print(f"Error al cargar los datos de libros: {e}")
            return None
    
    def load_categories(self):
        """
            Carga el dataframe con la información de una tabla específica.
        """
        try:
            self.df = pd.read_sql_query(f"SELECT * FROM categories", self.db_conn)
            print(f"DATOS DE CATEGORIAS CARGADOS")
            return self.df
        except Exception as e:
            print(f"Error al cargar los datos de categories: {e}")
            return None
    def merge_dataframes(self, books_df, categories_df):
        """
            Realiza un merge de los dataframes de libros y categorías.
        """
        try:
            merge_df = pd.merge(books_df, categories_df, left_on='category_id', right_on='id')
            print("DATAFRAMES MERGEADOS")
            return merge_df
        except Exception as e:
            print(f"Error al mergear los dataframes: {e}")
            return None
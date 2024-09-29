import pandas as pd
import numpy as np
from data.data_loader import DataLoader as dl
from data.database_manager import DatabaseManager


class DataAnalyzer:
    def __init__(self, df=None) -> None:
        self.df = df
        
    def get_data_books(self):
        if self.df is None:
            raise ValueError("El DataFrame no ha sido inicializado.")
        return self.df

    def get_data_info(self):
        return self.df.info()

    def get_data_columns(self):
        return self.df.columns

    def get_data_shape(self):
        return self.df.shape

    def get_data_describe(self):
        return self.df.describe()

    def get_data_head(self, n):
        return self.df.head(n)

    def get_data_tail(self, n):
        return self.df.tail(n)

    def get_data_columns_type(self):
        return self.df.dtypes

    def get_data_missing_values(self):
        return self.df.isnull().sum()

    def get_data_unique_values(self):
        return self.df.nunique()

    def get_data_correlation(self):
        return self.df.corr()

    def get_data_groupby(self, column):
        return self.df.groupby(column)

    def get_data_groupby_mean(self, column):
        return self.df.groupby(column).mean()

    def get_data_groupby_sum(self, column):
        return self.df.groupby(column).sum()

    def get_data_groupby_max(self, column):
        return self.df.groupby(column).max()

    def get_data_groupby_min(self, column):
        return self.df.groupby(column).min()
    
    def get_data_groupby_count(self, column):
        return self.df.groupby(column).count()
    
    def get_average_price_by_category_id(self):
        if 'category_id' not in self.df.columns or 'price' not in self.df.columns:
            raise ValueError("Las columnas especificadas no existen en el DataFrame.")
        return self.df.groupby('category_id')['price'].mean()
    
    def get_avg_price_by_category(self):
        if 'category_name' not in self.get_data_columns() or 'price' not in self.get_data_columns():
            raise ValueError("Las columnas especificadas no existen en el DataFrame.")
        avg_price_df = self.df.groupby('category_name')['price'].mean()
        avg_price_df.columns = ['category_name', 'price']
        return avg_price_df
    
    def get_books_by_rating(self):
        if 'rating' not in self.df.columns:
            raise ValueError("Las columnas especificadas no existen en el DataFrame.")
        rating_counts = self.df['rating'].value_counts().sort_index(ascending=False)
        rating_counts = rating_counts.reset_index()
        rating_counts.columns = ['rating', 'total']
        return rating_counts
    
    def get_avg_price_by_rating(self):
        if 'rating' not in self.get_data_columns() or 'price' not in self.get_data_columns():
            raise ValueError("Las columnas especificadas no existen en el DataFrame.")
        return self.df.groupby('rating')['price'].mean()
        
    
    def get_price_by_rating(self):
        if 'rating' not in self.df.columns or 'price' not in self.df.columns:
            raise ValueError("Las columnas especificadas no existen en el DataFrame.")
        return self.df.groupby('rating')['price'].mean()
    
    

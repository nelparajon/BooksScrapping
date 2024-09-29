from data.data_pipeline import DataPipeline
from data.database_manager import DatabaseManager as dbm
from data.data_loader import DataLoader as dl
from analyzer.data_analyzer import DataAnalyzer as da
from visualizer.data_visualizer import DataVisualizer as dv
from data.config_db import db_path

def Scrap_data():
    base_url = 'http://books.toscrape.com/'
    pipeline = DataPipeline(base_url)
    print("Extraidos todos los datos con BSoup de libros")   
    pipeline.run()

def load_books_data():
    try:
        db_manager = dbm(db_path)
        db_conn = db_manager.connect()
        if db_conn is None:
            print("No se pudo establecer la conexión a la base de datos.")
            return None
        data_loader = dl(db_conn)
        books_df = data_loader.load_books_df()
        return books_df
    except Exception as e:
        print(f"Error al cargar los datos de los libros: {e}")
        return None

def load_categories_data():
    try:
        db_manager = dbm(db_path)
        db_conn = db_manager.connect()
        if db_conn is None:
            print("No se pudo establecer la conexión a la base de datos.")
            return None
        data_loader = dl(db_conn)
        categories_df = data_loader.load_categories()
        return categories_df
    except Exception as e:
        print(f"Error al cargar los datos de las categorías: {e}")
        return None

def analyze_books_data(df):
    analyzer = da(df)
    return analyzer

def merge_dataframes(books_df, categories_df):
    data_loader = dl(None)
    merge_df = data_loader.merge_dataframes(books_df, categories_df)
    return merge_df

def get_first_and_last_five_books(analyzer):
    first_five_books = analyzer.get_data_head(5)
    last_five_books = analyzer.get_data_tail(5)
    return first_five_books, last_five_books

def get_books_by_rating(analyzer):
    return analyzer.get_books_by_rating()

def get_avg_price_by_category(analyzer):
    return analyzer.get_avg_price_by_category()

def get_avg_price_by_rating(analyzer):
    print("Promedio de precio de los libros por rating:")
    avg_price_by_rat = analyzer.get_avg_price_by_rating()
    avg_price_by_rat = avg_price_by_rat.sort_index(ascending=False)
    avg_price_by_rat = avg_price_by_rat.apply(lambda x: f"{x:.2f}€")
    return avg_price_by_rat

def visualize_books_price_avg_by_category(analyzer):
    data_visualizer = dv(analyzer)
    mean_prices = analyzer.get_avg_price_by_category()
    data_visualizer.plot_mean_price_by_category_horizontal(mean_prices)

def menu():
    while True:
        print("\nMenu:")
        print("1. Scrape data")
        print("2. Load books data")
        print("3. Load categories data")
        print("4. Analyze books data")
        print("5. Merge dataframes")
        print("6. Get first and last five books")
        print("7. Get books by rating")
        print("8. Get average price by category")
        print("9. Get average price by rating")
        print("10. Visualize books price average by category")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            Scrap_data()
        elif choice == '2':
            books_df = load_books_data()
            if books_df is not None:
                print(books_df.head())
        elif choice == '3':
            categories_df = load_categories_data()
            if categories_df is not None:
                print(categories_df.head())
        elif choice == '4':
            books_df = load_books_data()
            if books_df is not None:
                analyzer = analyze_books_data(books_df)
                print("Books data analyzed.")
        elif choice == '5':
            books_df = load_books_data()
            categories_df = load_categories_data()
            if books_df is not None and categories_df is not None:
                merge_df = merge_dataframes(books_df, categories_df)
                print(merge_df.head())
        elif choice == '6':
            books_df = load_books_data()
            if books_df is not None:
                analyzer = analyze_books_data(books_df)
                first_five, last_five = get_first_and_last_five_books(analyzer)
                print("First five books:\n", first_five)
                print("Last five books:\n", last_five)
        elif choice == '7':
            books_df = load_books_data()
            if books_df is not None:
                analyzer = analyze_books_data(books_df)
                books_by_rating = get_books_by_rating(analyzer)
                print(books_by_rating)
        elif choice == '8':
            books_df = load_books_data()
            if books_df is not None:
                analyzer = analyze_books_data(books_df)
                avg_price_by_category = get_avg_price_by_category(analyzer)
                print(avg_price_by_category)
        elif choice == '9':
            books_df = load_books_data()
            if books_df is not None:
                analyzer = analyze_books_data(books_df)
                avg_price_by_rating = get_avg_price_by_rating(analyzer)
                print(avg_price_by_rating)
        elif choice == '10':
            books_df = load_books_data()
            if books_df is not None:
                analyzer = analyze_books_data(books_df)
                visualize_books_price_avg_by_category(analyzer)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    menu()
        
    
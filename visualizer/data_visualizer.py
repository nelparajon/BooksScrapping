import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self, data):
        self.data = data

    def plot_line(self, x, y, title="Line Plot", xlabel="X-axis", ylabel="Y-axis"):
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    def plot_bar(self, categories, values, title="Bar Plot", xlabel="Categories", ylabel="Values"):
        plt.figure(figsize=(10, 6))
        plt.bar(categories, values, color='skyblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, axis='y')
        plt.show()

    def plot_scatter(self, x, y, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis"):
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, c='red', marker='x')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    def plot_mean_price_by_category_horizontal(self, mean_prices, title="Mean Price by Category", xlabel="Mean Price", ylabel="Categories", figsize=(18, 15)):
        plt.figure(figsize=figsize)
        bars = plt.barh(mean_prices.index, mean_prices.values, color='skyblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, axis='x')
        
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{bar.get_width():.2f}', va='center')
        
        plt.show()

import pandas as pd
import numpy as np
from message import print_title, print_stat, log_message

def generate_dummy_data(path="data.csv"):
    log_message("Генеруємо фейкові дані...")
    df = pd.DataFrame({
        'product': np.random.choice(['Phone', 'Laptop', 'Tablet'], size=100),
        'price': np.random.randint(100, 1000, size=100),
        'quantity': np.random.randint(1, 10, size=100)
    })
    df.to_csv(path, index=False)
    log_message(f"Збережено у {path}")

def load_data(path="data.csv"):
    log_message(f"Завантажуємо дані з {path}")
    return pd.read_csv(path)

def analyze_data(df):
    print_title("Основна статистика")
    df['total'] = df['price'] * df['quantity']
    print_stat("Середній дохід", df['total'].mean())
    print_stat("Загальний дохід", df['total'].sum())

    print_title("Продажі за продуктами")
    grouped = df.groupby('product')['total'].sum()
    print(grouped)

def main():
    generate_dummy_data()
    df = load_data()
    analyze_data(df)

if __name__ == "__main__":
    main()

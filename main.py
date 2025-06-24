import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from message import print_title, print_stat, log_message, warn_message


DATA_PATH = "data.csv"
FIG_DIR = "figures"
FIG_PATH = os.path.join(FIG_DIR, "sales_by_product.png")


def generate_dummy_data(path: str = DATA_PATH) -> None:
    """Генерує штучні дані про продажі."""
    log_message("Генеруємо фейкові дані…")
    df = pd.DataFrame({
        "product": np.random.choice(["Phone", "Laptop", "Tablet"], size=100),
        "price": np.random.randint(100, 1_000, size=100),
        "quantity": np.random.randint(1, 10, size=100)
    })
    df.to_csv(path, index=False)
    log_message(f"Дані збережено у {path}")


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Читає CSV із даними (генерує, якщо нема)."""
    if not os.path.exists(path):
        warn_message(f"{path} не знайдено — генеруємо новий датасет.")
        generate_dummy_data(path)
    log_message(f"Завантажуємо дані з {path}")
    return pd.read_csv(path)


def analyze_data(df: pd.DataFrame) -> pd.DataFrame:
    """Виводить базову статистику й повертає групування для графіка."""
    print_title("Основна статистика")
    df["total"] = df["price"] * df["quantity"]
    print_stat("Середній дохід", df["total"].mean())
    print_stat("Загальний дохід", df["total"].sum())

    print_title("Продажі за продуктами")
    grouped = df.groupby("product")["total"].sum()
    print(grouped, "\n")
    return grouped


def plot_sales(grouped: pd.Series, path: str = FIG_PATH) -> None:
    """Будує й зберігає стовпчикову діаграму."""
    # Створюємо директорію, якщо її нема
    os.makedirs(os.path.dirname(path), exist_ok=True)

    plt.figure(figsize=(6, 4))
    grouped.sort_values(ascending=False).plot(kind="bar")
    plt.title("Сумарний дохід за продуктами")
    plt.ylabel("Дохід, $")
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    log_message(f"Графік збережено у {path}")
    plt.close()


def main() -> None:
    """Точка входу."""
    df = load_data()
    grouped_sales = analyze_data(df)
    plot_sales(grouped_sales)


if __name__ == "__main__":
    main()

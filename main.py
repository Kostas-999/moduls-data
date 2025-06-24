import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

    top_product = grouped.idxmax()
    top_value = grouped.max()
    print_title("Найуспішніший продукт")
    print_stat(top_product, top_value)

    return grouped


def plot_pie(grouped: pd.Series, path: str = os.path.join(FIG_DIR, "sales_pie.png")) -> None:
    """Будує кругову діаграму продажів за продуктами."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    plt.figure(figsize=(5, 5))
    grouped.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Розподіл доходу за продуктами")
    plt.ylabel("")  # прибираємо вісь Y
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    log_message(f"Кругова діаграма збережена у {path}")
    plt.close()


def plot_histogram(series: pd.Series,
                   path: str = os.path.join(FIG_DIR, "sales_hist_price.png"),
                   title: str = "Розподіл цін товарів") -> None:
    """Будує та зберігає гістограму."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.figure(figsize=(6, 4))
    sns.histplot(series, kde=True, bins=15)
    plt.title(title)
    plt.xlabel("Ціна, $")
    plt.ylabel("Кількість")
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    log_message(f"Гістограма збережена у {path}")
    plt.close()


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


def summary_stats(series: pd.Series, name: str = "Дохід") -> None:
    """Виводить базові статистичні показники для series."""
    print_title(f"Статистика: {name}")
    stats = {
        "count": series.count(),
        "mean":  series.mean(),
        "median": series.median(),
        "std":   series.std(),
        "min":   series.min(),
        "max":   series.max(),
    }
    for k, v in stats.items():
        print_stat(k, v)


def main() -> None:
    """Точка входу."""
    df = load_data()

    # Аналіз та агрегація
    grouped_sales = analyze_data(df)

    # Базові статистики (ціни + дохід)
    summary_stats(df["price"], name="Ціна товару")
    summary_stats(df["total"], name="Сумарний дохід (рядки)")

    # Візуалізації
    plot_sales(grouped_sales)          # bar-chart
    plot_pie(grouped_sales)            # pie-chart
    plot_histogram(df["price"])        # histogram


if __name__ == "__main__":
    main()

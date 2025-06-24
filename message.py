def print_title(title: str):
    print(f"\n{'=' * 10} {title} {'=' * 10}")

def print_stat(name: str, value: float):
    print(f"{name}: {value:.2f}")

def log_message(text: str):
    print(f"[INFO] {text}")

def warn_message(text: str):
    print(f"[WARN] {text}")

def error_message(text: str):
    print(f"[ERROR] {text}")
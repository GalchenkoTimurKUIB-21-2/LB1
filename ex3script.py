import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# URL API НБУ
BASE_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"

# Функція для отримання курсу валют за певну дату
def get_exchange_rate(date, selected_currencies=None):
    formatted_date = date.strftime("%Y%m%d")  # Формат дати: YYYYMMDD
    params = {"date": formatted_date, "json": ""}  # Параметри запиту
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if selected_currencies:
            # Фільтруємо дані за обраними валютами
            data = [rate for rate in data if rate['cc'] in selected_currencies]
        return data
    else:
        print(f"Помилка: {response.status_code}")
        return None

# Отримання курсу за попередній тиждень
def get_last_week_rates(selected_currencies=None):
    today = datetime.now()
    last_week = [today - timedelta(days=i) for i in range(1, 8)]  # Дати за останній тиждень

    all_rates = {}
    for date in last_week:
        rates = get_exchange_rate(date, selected_currencies)
        if rates:
            all_rates[date.strftime("%Y-%m-%d")] = rates
    return all_rates

# Побудова графіка
def plot_exchange_rates(rates_last_week, selected_currencies):
    dates = list(rates_last_week.keys())  # Дати для осі X
    plt.figure(figsize=(10, 6))  # Розмір графіка

    for currency in selected_currencies:
        values = []
        for date in dates:
            # Знаходимо курс обраної валюти на кожну дату
            rate = next((r['rate'] for r in rates_last_week[date] if r['cc'] == currency), None)
            values.append(rate)

        # Додаємо лінію для валюти
        plt.plot(dates, values, marker='o', label=currency)

    # Налаштування графіка
    plt.title("Зміна курсу валют за останній тиждень")
    plt.xlabel("Дата")
    plt.ylabel("Курс (грн)")
    plt.xticks(rotation=45)  # Поворот підписів дат
    plt.legend()  # Легенда для валют
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Основна функція
if __name__ == "__main__":
    # Вибір валют (наприклад, USD, EUR)
    print("Введіть коди валют через кому (наприклад, USD, EUR):")
    user_input = input("Ваш вибір: ").strip()
    selected_currencies = [cc.strip().upper() for cc in user_input.split(",")]

    # Отримуємо курси за попередній тиждень
    rates_last_week = get_last_week_rates(selected_currencies)

    # Виводимо результати
    for date, rates in rates_last_week.items():
        print(f"Дата: {date}")
        for rate in rates:
            print(f"  {rate['txt']} ({rate['cc']}): {rate['rate']}")
        print()

    # Побудова графіка
    plot_exchange_rates(rates_last_week, selected_currencies)
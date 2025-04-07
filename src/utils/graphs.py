import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def wczytaj_dane(finance_path, categories_path, user_id=1):
    with open(finance_path, 'r') as file:
        finance_data = json.load(file)
    with open(categories_path, 'r') as file:
        categories_data = json.load(file)
        
    # Filter categories by user_id
    user_categories = [category for category in categories_data.get('categories', []) if category.get('user_id') == user_id]
    categories_dict = {str(category['id']): category['name'] for category in user_categories}
    
    # Filter finances by user_id
    user_spending = [item for item in finance_data.get('spending', []) if item.get('user_id') == user_id]
    user_incomes = [item for item in finance_data.get('incomes', []) if item.get('user_id') == user_id]
    
    filtered_finance_data = {
        'spending': user_spending,
        'incomes': user_incomes
    }
    
    return filtered_finance_data, categories_dict


def filtruj_dane(dane, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    filtered_expenses = [item for item in dane['spending'] if start_date <= datetime.strptime(item['date'], '%Y-%m-%d') <= end_date]
    filtered_incomes = [item for item in dane['incomes'] if start_date <= datetime.strptime(item['date'], '%Y-%m-%d') <= end_date]
    return {'expenses': filtered_expenses, 'incomes': filtered_incomes}


def generuj_miesiace(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    months = []
    current_date = start_date
    while current_date <= end_date:
        months.append(current_date.strftime('%Y-%m'))
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)
    return months


def generuj_wykres_kolowy_wydatkow(dane, categories, start_date, end_date):
    if not dane['expenses']:
        plt.figure(figsize=(8, 8))
        plt.text(0.5, 0.5, 'Brak danych z danego okresu', horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.axis('off')
        plt.savefig(f'wydatki_wedlug_kategorii_{start_date}_do_{end_date}.png')
        plt.show()
        return

    category_expenses = {}
    for expense in dane['expenses']:
        category_id = str(expense['categoryId'])
        category_name = categories.get(category_id, 'Inne')
        category_expenses[category_name] = category_expenses.get(category_name, 0) + expense['amount']

    labels = [f"{category} ({amount})" for category, amount in category_expenses.items()]
    sizes = category_expenses.values()
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=None, autopct='%1.1f%%', startangle=140)
    plt.title(f'Wydatki według kategorii\n{start_date} do {end_date}')
    plt.axis('equal')
    plt.legend(labels=labels, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2)
    plt.savefig(f'wydatki_wedlug_kategorii_{start_date}_do_{end_date}.png', bbox_inches='tight')
    plt.show()


def generuj_wykres_kolumnowy_wydatkow(dane, start_date, end_date):
    if not dane['expenses']:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, 'Brak danych z danego okresu', horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.axis('off')
        plt.savefig(f'wydatki_{start_date}_do_{end_date}.png')
        plt.show()
        return

    monthly_expenses = {}
    for expense in dane['expenses']:
        month = datetime.strptime(expense['date'], '%Y-%m-%d').strftime('%Y-%m')
        monthly_expenses[month] = monthly_expenses.get(month, 0) + expense['amount']

    all_months = generuj_miesiace(start_date, end_date)
    amounts = [monthly_expenses.get(month, 0) for month in all_months]
    plt.figure(figsize=(10, 6))
    plt.bar(all_months, amounts, color='red', label='Wydatki')
    plt.xlabel('Miesiąc')
    plt.ylabel('Kwota')
    plt.title(f'Wydatki\n{start_date} do {end_date}')
    plt.legend()

    interval = max(1, len(all_months) // 10)
    plt.xticks(ticks=range(0, len(all_months), interval), labels=[all_months[i] for i in range(0, len(all_months), interval)], rotation=45)

    plt.savefig(f'wydatki_{start_date}_do_{end_date}.png')
    plt.show()


def generuj_wykres_kolumnowy_przychodow(dane, start_date, end_date):
    if not dane['incomes']:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, 'Brak danych z danego okresu', horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.axis('off')
        plt.savefig(f'przychody_{start_date}_do_{end_date}.png')
        plt.show()
        return

    monthly_incomes = {}
    for income in dane['incomes']:
        month = datetime.strptime(income['date'], '%Y-%m-%d').strftime('%Y-%m')
        monthly_incomes[month] = monthly_incomes.get(month, 0) + income['amount']

    all_months = generuj_miesiace(start_date, end_date)
    amounts = [monthly_incomes.get(month, 0) for month in all_months]
    plt.figure(figsize=(10, 6))
    plt.bar(all_months, amounts, color='green', label='Przychody')
    plt.xlabel('Miesiąc')
    plt.ylabel('Kwota')
    plt.title(f'Przychody\n{start_date} do {end_date}')
    plt.legend()

    interval = max(1, len(all_months) // 10)
    plt.xticks(ticks=range(0, len(all_months), interval), labels=[all_months[i] for i in range(0, len(all_months), interval)], rotation=45)

    plt.savefig(f'przychody_{start_date}_do_{end_date}.png')
    plt.show()

def rysuj_wykresy(start_date, end_date, wykres_typ, user_id=1):
    finance_data, categories_data = wczytaj_dane('data/finances.json', 'data/user_categories.json', user_id)
    dane = filtruj_dane(finance_data, start_date, end_date)

    if wykres_typ == 'kolowy':
        generuj_wykres_kolowy_wydatkow(dane, categories_data, start_date, end_date)
    elif wykres_typ == 'kolumnowy_wydatki':
        generuj_wykres_kolumnowy_wydatkow(dane, start_date, end_date)
    elif wykres_typ == 'kolumnowy_przychody':
        generuj_wykres_kolumnowy_przychodow(dane, start_date, end_date)
    else:
        print("Nieznany typ wykresu. Dostępne typy: 'kolowy', 'kolumnowy_wydatki', 'kolumnowy_przychody'")

if __name__ == "__main__":
    rysuj_wykresy('2023-01-01', '2023-12-02', 'kolowy', 1)
    rysuj_wykresy('2023-01-01', '2023-12-02', 'kolumnowy_wydatki', 1)
    rysuj_wykresy('2023-01-01', '2023-12-02', 'kolumnowy_przychody', 1)

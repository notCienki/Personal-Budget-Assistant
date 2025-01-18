import json
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Wczytaj dane z pliku JSON
def wczytaj_dane(finance_path, categories_path):
    with open(finance_path, 'r') as file:
        finance_data = json.load(file)
    with open(categories_path, 'r') as file:
        categories_data = json.load(file)
    categories_dict = {str(category['id']): category['name'] for category in categories_data['categories']}
    return finance_data, categories_dict

# Generuj wykres kołowy wydatków według kategorii
def generuj_wykres_kolowy_wydatkow(dane, categories):
    category_expenses = {}
    for expense in dane['spending']:
        category_id = str(expense['categoryId'])
        category_name = categories.get(category_id, 'Inne')
        category_expenses[category_name] = category_expenses.get(category_name, 0) + expense['amount']

    #print("category_expenses:", category_expenses)  # Debugging output

    labels = category_expenses.keys()
    sizes = category_expenses.values()
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Wydatki według kategorii')
    plt.axis('equal')
    plt.savefig('wydatki_wedlug_kategorii.png')
    plt.show()

# Generuj wykres kolumnowy wydatków
def generuj_wykres_kolumnowy_wydatkow(dane):
    monthly_expenses = {}
    for expense in dane['spending']:
        month = datetime.strptime(expense['date'], '%Y-%m-%d').strftime('%Y-%m')
        monthly_expenses[month] = monthly_expenses.get(month, 0) + expense['amount']

    #print("monthly_expenses:", monthly_expenses)  # Debugging output

    months = sorted(monthly_expenses.keys())
    amounts = [monthly_expenses[month] for month in months]
    plt.figure(figsize=(10, 6))
    plt.bar(months, amounts, color='red')
    plt.xlabel('Miesiąc')
    plt.ylabel('Kwota')
    plt.title('Wydatki')
    plt.savefig('wydatki.png')
    plt.show()

# Generuj wykres kolumnowy przychodów
def generuj_wykres_kolumnowy_przychodow(dane):
    monthly_incomes = {}
    for income in dane['incomes']:
        month = datetime.strptime(income['date'], '%Y-%m-%d').strftime('%Y-%m')
        monthly_incomes[month] = monthly_incomes.get(month, 0) + income['amount']

    #print("monthly_incomes:", monthly_incomes)  # Debugging output

    months = sorted(monthly_incomes.keys())
    amounts = [monthly_incomes[month] for month in months]
    plt.figure(figsize=(10, 6))
    plt.bar(months, amounts, color='green')
    plt.xlabel('Miesiąc')
    plt.ylabel('Kwota')
    plt.title('Przychody')
    plt.savefig('przychody.png')
    plt.show()

# Główna funkcja do rysowania wykresów
def rysuj_wykresy():
    finance_data, categories_data = wczytaj_dane('src/data/finance.json', 'src/data/categories.json')
    #print("categories_data:", categories_data)  # Debugging output
    #print("finance_data:", finance_data)  # Debugging output

    # Generowanie wykresów
    generuj_wykres_kolowy_wydatkow(finance_data, categories_data)
    generuj_wykres_kolumnowy_wydatkow(finance_data)
    generuj_wykres_kolumnowy_przychodow(finance_data)

# Przykładowe wywołanie funkcji
if __name__ == "__main__":
    rysuj_wykresy()
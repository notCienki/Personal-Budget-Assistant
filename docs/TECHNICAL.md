# Dokumentacja Techniczna - Personalny Asystent Budżetu Domowego

## 1. Struktura Projektu

### 1.1 Drzewo katalogów
```
src/
├── data/
│   ├── finance.json
│   ├── categories.json
│   ├── user.json
│   ├── exchange_rates.json
│   └── base_currency.json
├── utils/
│   ├── validation/
│   └── currency_converter.py
└── docs/
    └── types/
```

### 1.2 Opis komponentów
- **data/** - przechowywanie danych aplikacji
- **utils/** - narzędzia i funkcje pomocnicze
- **docs/** - dokumentacja techniczna

## 2. Specyfikacja Danych

### 2.1 Format danych użytkownika (user.json)
```json
{
    "user": {
        "login": "string",
        "name": "string",
        "last_name": "string",
        "email": "string",
        "password": "hashed_string"
    }
}
```

### 2.2 Format transakcji (finance.json)
```json
{
    "spending": [
        {
            "id": "number",
            "name": "string",
            "amount": "number",
            "currency": "string",
            "categoryId": "number",
            "date": "YYYY-MM-DD",
            "note": "string"
        }
    ],
    "incomes": [
        {
            "id": "number",
            "currency": "string",
            "amount": "number",
            "date": "YYYY-MM-DD",
            "note": "string"
        }
    ]
}
```

### 2.3 Format kategorii (categories.json)
```json
{
    "categories": [
        {
            "id": "number",
            "name": "string"
        }
    ]
}
```

## 3. API i Funkcje

### 3.1 Zarządzanie Użytkownikami (users_repository.py)
```python
is_user() -> bool
get_user() -> dict
register(data: dict) -> bool
login(login: str, password: str) -> bool
```

### 3.2 Zarządzanie Finansami (finance_repository.py)
```python
get_all_spending() -> list
add_spending(data: dict) -> dict
remove_spending_by_id(id: int) -> None
update_spending(id: int, data: dict) -> None
get_all_incomes() -> list
add_income(data: dict) -> dict
```

### 3.3 Zarządzanie Kategoriami (categories_repository.py)
```python
get_all_categories() -> list
get_category_by_id(id: int) -> dict
add_category(name: str) -> None
remove_category_by_id(id: int) -> None
```

### 3.4 Konwerter Walut (currency_converter.py)
```python
convert_currency(amount: float, from_currency: str, to_currency: str) -> float
get_exchange_rate(from_currency: str, to_currency: str) -> float
add_currency_rate(from_currency: str, to_currency: str, rate: float) -> None
```

## 4. Bezpieczeństwo

### 4.1 Szyfrowanie haseł
- Wykorzystanie biblioteki bcrypt
- Automatyczne generowanie salt
- 12 rund hashowania

### 4.2 Walidacja danych
- Sprawdzanie poprawności dat
- Walidacja typów danych
- Sanityzacja danych wejściowych

## 5. Obsługa Walut

### 5.1 Wspierane waluty
- PLN (złoty polski)
- EUR (euro)
- USD (dolar amerykański)

### 5.2 System kursów walut
```json
{
    "rates": {
        "PLN": {
            "EUR": 0.23,
            "USD": 0.25
        },
        "EUR": {
            "PLN": 4.35,
            "USD": 1.09
        },
        "USD": {
            "PLN": 4.0,
            "EUR": 0.92
        }
    }
}
```

## 6. Wymagania Systemowe

### 6.1 Minimalne wymagania
- Python 3.8 lub nowszy
- 100MB wolnej przestrzeni dyskowej
- Dostęp do internetu (do aktualizacji kursów walut)

### 6.2 Zależności
```
bcrypt
flask
pywebview
json
datetime
```

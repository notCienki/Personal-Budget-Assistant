# Personalny-Asystent-Budzetu-Domowego-PWI2024

Oficjalne repozytorium projektu programistycznego z przedmiotu PWI grupy Z7.

# Personalny Asystent Budżetu Domowego

## Spis treści

1. [Wprowadzenie](#wprowadzenie)
2. [Instalacja](#instalacja)
3. [Funkcjonalności](#funkcjonalności)
4. [Instrukcja użytkowania](#instrukcja-użytkowania)
5. [Specyfikacja techniczna](#specyfikacja-techniczna)
6. [FAQ](#faq)

## Wprowadzenie

Personalny Asystent Budżetu Domowego to zaawansowane narzędzie do zarządzania finansami osobistymi, które umożliwia:

- Śledzenie wydatków i przychodów
- Kategoryzację transakcji
- Automatyczne przeliczanie walut
- Generowanie raportów finansowych
- Bezpieczne przechowywanie danych

## Instalacja

### Wymagania systemowe

- Python 3.8 lub nowszy
- 20 MB wolnego miejsca na dysku

### Proces instalacji

1. Pobierz aplikację z repozytorium
2. Zainstaluj wymagane zależności:

```bash
pip install flask
pip install pywebview
pip install bcrypt
pip install fpdf
pip install matplotlib
```

3. Uruchom aplikację:

```bash
python py .\src\server\main.py
```

## Funkcjonalności

### 1. System zarządzania użytkownikami

- Bezpieczna rejestracja i logowanie
- Szyfrowanie haseł

### 2. Zarządzanie wydatkami

- Dodawanie wydatków z szczegółowymi informacjami
- Kategoryzacja wydatków
- Historia wydatków
- Możliwość dodawania notatek
- Usuwanie wpisów

### 3. Zarządzanie przychodami

- Rejestrowanie różnych źródeł przychodów
- Historia przychodów
- Usuwanie wpisów

### 4. Generowanie raportu

- Podsumowanie przychodów i wydatków
- Wyliczenie salda końcowego
- Szczegółowy wykaz przychodów
- Szczegółowy wykaz wydatków

### 5. System kategorii

Predefiniowane kategorie:

- Transport 🚗
- Zdrowie 🏥
- Edukacja 📚
- Ubrania 👔
- Jedzenie 🍎
- Zakupy 🛒
- Rozrywka 🎮
- Rachunki 📄
- Inne ❓
- Wspólne 👥

### 5. Obsługa walut

Wspierane waluty:

- PLN (złoty polski) 
- EUR (euro)
- USD (dolar amerykański)
- GBP (brytyjski funt)
- JPY (jen)
- CNY (renminbi)
- AUD (dolar australijski)
- CAD (dolar kanadyjski)
- CHF (frank szwajcarski)
- SEK (korona szwedzka)

## Instrukcja użytkowania

### Rejestracja i logowanie

1. **Rejestracja**

   ```
   Po wejściu do aplikacji po raz pierwszy, uzupełnij formularz rejestracyjny i kliknij przycisk Zarejestruj.
   ```

2. **Logowanie**
   ```
   Po każdorazowym otwarciu aplikacji wpisz swój login oraz hasło.
   ```

### Podstawowe operacje

1. **Dodawanie wydatku**

   ```
   Strona główna -> Wypełnij formularz -> Dodaj wydatek
   ```

2. **Dodawanie przychodu**

   ```
   Przychody -> Wypełnij formularz -> Dodaj przychód
   ```

3. **Usuwanie wydatku**
   ```
   Strona główna -> Wydatki z bieżącego miesiąca -> Usuń 
   ```

4. **Usuwanie przychodu**
   ```
   Przychody -> Przychody z bieżącego miesiąca -> Usuń 
   ```

5. **Dodawanie kategorii**
   ```
   Zarządzanie kategoriami -> Dodaj nową kategorię -> Podaj nazwę kategorii -> Dodaj
   ```
  
6. **Usuwanie kategorii**
   ```
   Zarządzanie kategoriami -> Istniejące kategorie -> Usuń 
   ```

7. **Przeliczanie walut**
   ```
   Przelicznik walut -> Wprowadź kwotę -> Wybierz waluty -> Przelicz
   ```

8. **Generowanie raportu**
   ```
   Przychody-> Przegląd przychodów -> Wygeneruj raport z ostatniego miesiąca 
   ```
   

## Specyfikacja techniczna

### Architektura systemu

- Frontend: Webview/Flask
- Backend: Python
- Baza danych: JSON
- Szyfrowanie: bcrypt

### Zabezpieczenia

- Szyfrowanie haseł
- Walidacja danych wejściowych

### Format danych

- Wszystkie dane przechowywane są w formacie JSON

## FAQ

### Czy mogę eksportować swoje dane?

Tak, dane można eksportować do formatu PDF.

### Czy moje dane są bezpieczne?

Tak, wszystkie dane są przechowywane lokalnie na Twoim komputerze i zabezpieczone szyfrowaniem.

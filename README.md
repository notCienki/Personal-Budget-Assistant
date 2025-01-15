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
- 100 MB wolnego miejsca na dysku

### Proces instalacji
1. Pobierz aplikację z repozytorium
2. Zainstaluj wymagane zależności:
```bash
pip install -r requirements.txt
```
3. Uruchom aplikację:
```bash
python main.py
```

## Funkcjonalności

### 1. System zarządzania użytkownikami
- Bezpieczna rejestracja i logowanie
- Szyfrowanie haseł
- Możliwość resetowania hasła

### 2. Zarządzanie wydatkami
- Dodawanie wydatków z szczegółowymi informacjami
- Kategoryzacja wydatków
- Możliwość dodawania notatek
- Edycja i usuwanie wpisów

### 3. Zarządzanie przychodami
- Rejestrowanie różnych źródeł przychodów
- Automatyczne sumowanie
- Historia przychodów

### 4. System kategorii
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

## Instrukcja użytkowania

### Pierwsze kroki
1. **Rejestracja**
   ```
   Menu główne -> Rejestracja -> Wypełnij formularz
   ```

2. **Logowanie**
   ```
   Menu główne -> Logowanie -> Wprowadź dane
   ```

### Podstawowe operacje
1. **Dodawanie wydatku**
   ```
   Menu główne -> Dodaj wydatek -> Wypełnij formularz
   ```

2. **Dodawanie przychodu**
   ```
   Menu główne -> Dodaj przychód -> Wypełnij formularz
   ```

3. **Przeglądanie historii**
   ```
   Menu główne -> Historia -> Wybierz zakres dat
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
- Automatyczne kopie zapasowe

### Format danych
- Wszystkie dane przechowywane są w formacie JSON
- Automatyczna walidacja integralności danych
- Regularne kopie zapasowe

## FAQ

### Czy mogę eksportować swoje dane?
Tak, dane można eksportować do formatu CSV lub JSON.

### Czy moje dane są bezpieczne?
Tak, wszystkie dane są przechowywane lokalnie na Twoim komputerze i zabezpieczone szyfrowaniem.

# Personalny-Asystent-Budzetu-Domowego-PWI2024
Oficjalne repozytorium projektu programistycznego z przedmiotu PWI grupy Z7.
# Personalny Asystent Budżetu Domowego

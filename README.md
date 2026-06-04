# 🇯🇵 日本語暗記 — NihongoCards

Piękna, nowoczesna aplikacja desktopowa do nauki języka japońskiego (i nie tylko!) za pomocą interaktywnych fiszek z wbudowanym systemem poziomów (XP) oraz automatyczną wizualizacją aktywności w stylu kalendarza GitHub.

Aplikacja została zbudowana w języku **Python** przy użyciu frameworka **Flet (Flutter dla Pythona)**, oferując płynne animacje, ciemny motyw oraz dynamiczne motywy kolorystyczne.

---

## 🚀 Główne Funkcje

*   🎴 **Interaktywne Fiszki:** System nauki z oceną trudności zapamiętania (Again, Hard, Good, Easy).
*   📊 **Heatmapa Aktywności:** Automatycznie generowany wykres kalendarzowy (przy użyciu bibliotek `july` oraz `matplotlib`) prezentujący historię powtórek na przestrzeni roku w stylu wykresu kontrybucji GitHub.
*   📈 **System XP i Poziomów:** Zdobywaj punkty doświadczenia (XP) za poprawne odpowiedzi oraz ukończenie sesji nauki, aby awansować na kolejne poziomy.
*   📁 **Zarządzanie Taliami:** 
    *   Wygodne przeglądanie i dodawanie nowych talii.
    *   Importowanie gotowych talii z plików `.json`.
    *   Przeglądanie szczegółów talii (lista kart, edycja oraz usuwanie fiszek).
*   🎨 **Personalizacja Motywu:** Możliwość zmiany głównego akcentu kolorystycznego (niebieski, zielony, czerwony) bezpośrednio w panelu ustawień aplikacji.
*   💾 **Lokalna Baza Danych:** Wszystkie statystyki, postępy, zdobyte XP oraz historia nauki są bezpiecznie zapisywane lokalnie w bazie danych SQLite.

---

## 🛠️ Stos Technologiczny

*   **Język:** Python 3.11+
*   **Interfejs użytkownika (GUI):** [Flet](https://flet.dev/) (silnik Flutter)
*   **Baza danych:** SQLite
*   **Wizualizacja danych:** Matplotlib, Pandas, July
*   **Przechowywanie konfiguracji:** JSON

---

## 📦 Instalacja i Uruchomienie

### 1. Klonowanie repozytorium lub pobranie plików
Upewnij się, że masz zainstalowanego Pythona (zalecana wersja 3.11+).

### 2. Instalacja zależności
Zainstaluj wymagane pakiety za pomocą menedżera pakietów `pip`:

```bash
pip install -r requirements.txt
```

*Zawartość `requirements.txt` obejmuje m.in. `flet`, `matplotlib`, `pandas`, `july`.*

### 3. Uruchomienie aplikacji
Uruchom główny skrypt aplikacji:

```bash
python main.py
```

---

## 📁 Struktura Projektu

Oto krótki przewodnik po strukturze katalogów aplikacji:

```text
├── core/                   # Logika biznesowa i obsługa wyjątków
│   ├── study_session.py    # Logika pojedynczej sesji nauki (algorytm powtórek)
│   └── exceptions.py       # Niestandardowe klasy wyjątków aplikacji
│
├── data/                   # Przechowywanie danych i repozytoria
│   ├── database.py         # Inicjalizacja SQLite oraz schemat bazy danych
│   ├── repository.py       # Operacje odczytu/zapisu na bazie danych (CRUD)
│   ├── models.py           # Definicje modeli (Deck, Card, Stat)
│   ├── settings.json       # Plik konfiguracyjny (np. aktualny motyw)
│   ├── flashcards.db       # Lokalny plik bazy danych SQLite (generowany przy starcie)
│   └── io/                 # Import i eksport talii (JSON)
│
├── decks/                  # Przykładowe talie do zaimportowania w formacie JSON
│   ├── Hiragana.json       # Talia ze znakami Hiragany
│   └── ...
│
├── UI/                     # Warstwa prezentacji (interfejs użytkownika)
│   ├── page.py             # Główny kontener aplikacji i nawigacja
│   ├── theme.py            # Globalne zmienne motywu (kolory, palety)
│   ├── components/         # Ponadwymiarowe komponenty Flet (przycisk hover, karty talii)
│   └── views/              # Widoki poszczególnych ekranów (Menu, Nauka, Statystyki, Ustawienia)
│
├── main.py                 # Punkt wejściowy aplikacji
└── requirements.txt        # Wymagane biblioteki Pythona
```

---

## 📝 Format Pliku Talii (JSON)

Możesz łatwo przygotować własne talie i zaimportować je do aplikacji. Plik JSON powinien mieć następujący format:

```json
{
  "name": "Moja Talia",
  "cards": [
    {
      "front": "あ",
      "back": "a",
      "reading": "a",
      "card_type": "Kana",
      "example": "あめ (deszcz)"
    },
    {
      "front": "い",
      "back": "i",
      "reading": "i",
      "card_type": "Kana",
      "example": "いぬ (pies)"
    }
  ]
}
```

---

## 💡 Jak Używać Aplikacji

1.  **Menu Główne:** Zobacz swój aktualny poziom oraz punkty XP. Wybierz opcję **Start** aby przejść do wyboru talii, lub **Decks** by zarządzać swoimi fiszkami.
2.  **Zarządzanie Taliami:** Kliknij *Add Deck* aby utworzyć nową pustą talię, lub *Import Deck*, aby załadować plik JSON z dysku.
3.  **Nauka:** Kliknij na kartę, aby zobaczyć odpowiedź, a następnie wybierz poziom trudności (Again/Hard/Good/Easy), by zaktualizować status powtóki.
4.  **Statystyki:** Sprawdź swoją systematyczność na wykresie aktywności. Każda ukończona powtórka dodaje punkty na Twojej heatmapie.
5.  **Ustawienia:** Spersonalizuj wygląd programu, wybierając ulubiony kolor motywu.

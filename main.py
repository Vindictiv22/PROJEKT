from os import system
import time  # Moduł do odliczania czasu w sekundach
from saves import GameState
import json
import random
class MainGame:
    """Główna klasa zarządzająca zasobami gry"""
    
    def __init__(self):
        self._game_running = True # Zacznik działania gry, ustawienie go na false zakańcza grę
        self._input_string = "" # łańcuch z tekstem gracza
        self.game_mode = 0 # poziom trudności
        self.game_state = GameState()
        
        # System punktów
        self.score = 0  # Całkowity wynik gracza
        self._start_time = 0.0  # Moment wyświetlenia słowa na ekranie
        self._current_word = "testowe"  # Słowo do wpisania (na potrzeby testów)

        self._baza_slow = self._wczytaj_baze_slow()
        self._aktualne_slowo = ""

    def _wczytaj_baze_slow(self):
        """Wczytuje plik JSON z dysku"""
        try:
            with open('baza_slow.json', 'r', encoding='utf-8') as plik:
                return json.load(plik)
        except FileNotFoundError:
            # Zabezpieczenie na wypadek, gdyby pliku brakowało
            print("Błąd: Nie znaleziono pliku slowa.json! Tworzę awaryjną bazę.")
            return {"latwe": ["test"], "srednie": ["testowanie"], "trudne": ["autotestowanie"], "ultratrudne" : ["skibidi"]}

    def main_loop(self):
        """Główna pętla gry zarządza kolejnością wykonywania się funkcji"""
        self._main_menu()
        self._losuj_nowe_slowo()

        while self._game_running:
            self._game_output()
            self._game_input()
            self._screen_update()
            self._losuj_nowe_slowo()

    def _main_menu(self):
        """menu główne gry"""
        self._screen_update()
        print("MISTRZ KLAWIATURY\n=================\n"
            "wybierz poziom trudności:\n1 - łatwy | 2 - średni | 3 - trudny | 4 - skibidi\n")
        self.game_mode = input()
        print("'save' wykonuje zatespis\n'quit' zakańcza grę\n'read' wczytuje poprzedni zapis\n")
        self._game_input()
        self._screen_update()

    def _losuj_nowe_slowo(self):
        """Losuje słowo na podstawie aktualnego game_mode"""
        lista_slow = self._baza_slow[self.game_mode]
        self._aktualne_slowo = random.choice(lista_slow)


    def _game_input(self):
        """zarządzanie wejściem programu"""
        self._input_string  = input()
        if self._input_string.lower() == 'quit': # warunki zakończenia gry
            self._game_running = False
        elif self._input_string.lower() == 'save': # warunek zapisu gry
            self._make_save()
        elif self._input_string.lower() == 'read': # warunek wczytania zapisu
            self._save_read()
        else:
            # Obliczanie czasu spędzonego na wpisywaniu
            end_time = time.time()
            elapsed_time = int(end_time - self._start_time)
            
            # Wywołanie funkcji obliczającej punkty
            self._calculate_score(elapsed_time)

    def _calculate_score(self, elapsed_time):
        """Osobna metoda odpowiedzialna za system punktów"""
        # Sprawdzenie poprawności słowa (brak printów i brak time.sleep)
        if self._input_string == self._current_word:
            gained_points = len(self._current_word) - elapsed_time
            
            if gained_points < 2:
                gained_points = 2
                
            self.score += gained_points
        else:
            self.score -= 2
            
            if self.score < 0:
                self.score = 0
            self._losuj_nowe_slowo()

    def _screen_update(self):
        """aktualizacja stanu ekranu"""
        system("cls")

    def _game_output(self): 
        """tutaj będzie pobierane słowo z klasy zarządzającej słowami"""
        # Wyświetlanie aktualnej liczby punktów na górze ekranu gry
        print(f"PUNKTY: {self.score}")
        print("=================")
        print(f"wpisz słowo: {self._current_word}")
        
        # Zapisujemy czas pokazania słowa
        self._start_time = time.time()
  
        print("wpisz słowo: ", self._aktualne_slowo)

    # Ogólnie to wiem że dwie poniższe metody są trochę nieprzemyślane pod kątem tego,
    # że każda zmienna jest oddzielnie zapisywana/wczytywana przez dodatkowy słownik.
    # Najprościej by było poprostu zastąpić wszystkie pojedyńcze zmienne jednym dużym słownikiem,
    # do którego wszystko by było przepisywane za jednym razem.

    def _make_save(self):
        """zapis stanu gry"""
        self.game_state.data["game_mode"] = self.game_mode
        self.game_state.data["score"] = self.score  
        self.game_state.file_save()

    def _save_read(self):
        """metoda wczytująca to co przekaże obiekt game_state"""
        data = self.game_state.file_read()
        self.game_mode = data["game_mode"]
        self.score = data.get("score", 0)  

def main():
    if __name__ == '__main__':
        game = MainGame()
        game.main_loop()

main()
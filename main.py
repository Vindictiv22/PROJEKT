from os import system
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
        print("'save' wykonuje zapis\n'quit' zakańcza grę\n'read' wczytuje poprzedni zapis\n")
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
            self._losuj_nowe_slowo()

    def _screen_update(self):
        """aktualizacja stanu ekranu"""
        system("cls")

    def _game_output(self): 
        """tutaj będzie pobierane słowo z klasy zarządzającej słowami"""
  
        print("wpisz słowo: ", self._aktualne_slowo)

    # Ogólnie to wiem że dwie poniższe metody są trochę nieprzemyślane pod kątem tego,
    # że każda zmienna jest oddzielnie zapisywana/wczytywana przez dodatkowy słownik.
    # Najprościej by było poprostu zastąpić wszystkie pojedyńcze zmienne jednym dużym słownikiem,
    # do którego wszystko by było przepisywane za jednym razem.

    def _make_save(self):
        """zapis stanu gry"""
        # tutaj trzeba wrzucać wszystkie pola które mają być zapisywane 
        self.game_state.data["game_mode"] = self.game_mode
        self.game_state.file_save()

    def _save_read(self):
        """metoda wczytująca to co przekaże obiekt game_state"""
        data = self.game_state.file_read()
        # tutaj są przerzucane wartości ze słownika do pól klasy   
        self.game_mode = data["game_mode"]

def main():
    if __name__ == '__main__':
        game = MainGame()
        game.main_loop()

main()
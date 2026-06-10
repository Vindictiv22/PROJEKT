import json
import os
import random
import time
from saves import GameState
import time


class MainGame:
    """Główna klasa zarządzająca zasobami gry"""

    def __init__(self):
        self._game_running = True
        self._input_string = ""
        self.game_mode = "1"  # Zmiana na string, aby pasował do input()
        self._game_running = True # Zacznik działania gry, ustawienie go na false zakańcza grę
        self.game_mode = 0 # poziom trudności
        self.game_tryb = 0 # tryb gry - nauka/wyzwanie
        self.game_state = GameState()
        self.slowa = 0

        # System punktów
        self.score = -2  # Całkowity wynik gracza
        self._start_time = 0.0  # Moment wyświetlenia słowa na ekranie

        # System combo
        self.combo_counter = 0

        self._baza_slow = self._wczytaj_baze_slow()
        self._aktualne_slowo = ""

    def _wczytaj_baze_slow(self):
        """Wczytuje plik JSON z dysku"""
        try:
            with open("baza_slow.json", "r", encoding="utf-8") as plik:
                return json.load(plik)
        except FileNotFoundError:
            print("Błąd: Nie znaleziono pliku. Tworzę awaryjną bazę.")
            return {
                "1": ["test"],
                "2": ["testowanie"],
                "3": ["autotestowanie"],
            }

    def main_loop(self):
        """Główna pętla gry"""
        self._main_menu()
        self._losuj_nowe_slowo()

        while self._game_running:
            self._game_output()
            self._game_input()
            self._screen_update()
            if self.score >= 10_000:
                self._mistrz_klawiatury()
                

    def _mistrz_klawiatury(self):
        print("GRATULACJE ZOSTAŁEŚ MISTRZEM KLAWIATURY\n"
        "TEAZ MOŻESZ ROZPOCZĄĆ SWOJĄ PRZYGODĘ PONOWNIE\n")
        self.score=0

    def _main_menu(self):
        """Menu główne gry"""
        self._screen_update()
        print(
            "MISTRZ KLAWIATURY\n=================\n"
            "wybierz poziom trudności:\n1 - łatwy | 2 - średni | 3 - trudny \n"
        )
        self.game_mode = input()
        print("Wybierz tryb gry\nnauka - tryb bez presji czasu | wyzwanie - tryb w którym zdobywasz punkty\n")
        self.game_tryb = input()
        print(
            "\n'save' wykonuje zapis\n'quit' zakańcza grę\n'read' wczytuje poprzedni zapis\n"
        )
        print("Naciśnij ENTER, aby rozpocząć grę...")
        self._game_input()
        self._screen_update()

    def _losuj_nowe_slowo(self):
        """Losuje słowo na podstawie aktualnego game_mode"""
        lista_slow = self._baza_slow[self.game_mode]
        self._aktualne_slowo = random.choice(lista_slow)

    def _game_input(self):
        """Zarządzanie wejściem programu"""
        self._input_string = input()
        komenda = self._input_string.lower().strip()

        if komenda == "quit":
            self._game_running = False
        elif komenda == "save":
            self._make_save()
            print("Gra została zapisana! Naciśnij ENTER...")
            input()
        elif komenda == "read":
            self._save_read()
            print("Gra została wczytana! Naciśnij ENTER...")
            input()
            self._losuj_nowe_slowo()
        else:
            end_time = time.time()
            elapsed_time = int(end_time - self._start_time)
            self._calculate_score(elapsed_time)
            self._losuj_nowe_slowo()  # Losuj nowe słowo PO wpisaniu starego

    def _calculate_score(self, elapsed_time):
        """Metoda odpowiedzialna za system punktów z combem"""
        if self._input_string == self._aktualne_slowo:
            self.combo_counter += 1  # Zwiększamy combo za dobrą odpowiedź
            
            # Bazowe punkty
            gained_points = len(self._input_string) - elapsed_time
            if gained_points < 2:
                gained_points = 2

            # Nakładanie mnożnika combo
            if self.combo_counter >= 20:
                gained_points = int(gained_points * 3.0)
            elif self.combo_counter >= 15:
                gained_points = int(gained_points * 2.5)
            elif self.combo_counter >= 10:
                gained_points = int(gained_points * 2.0)
            elif self.combo_counter >= 5:
                gained_points = int(gained_points * 1.5)

            self.score += gained_points
        else:
            self.combo_counter = 0  # Błąd resetuje combo do zera
            self.score -= 2
            if self.score < 0:
                self.score = 0

    def _screen_update(self):
        """Aktualizacja stanu ekranu"""
        os.system("cls" if os.name == "nt" else "clear")

    def _game_output(self):
        """Wyświetlanie stanu gry"""
        if self.game_tryb =='wyzwanie':
            print(f"PUNKTY: {self.score}")
            if self.combo_counter >= 5:
                print(f" COMBO X{self.combo_counter}! ")
        print("=================")
        print(f"wpisz słowo: {self._aktualne_slowo}")
        
        
        # Zapisujemy czas pokazania słowa
        if self.game_tryb == 'wyzwanie':
            self._start_time = time.time()
       
    def _make_save(self):
        """Zapis stanu gry"""
        self.game_state.data["game_mode"] = self.game_mode
        self.game_state.data["score"] = self.score
        self.game_state.file_save()

    def _save_read(self):
        """Metoda wczytująca stan gry"""
        data = self.game_state.file_read()
        if data:
            self.game_mode = str(data.get("game_mode", "1"))
            self.score = data.get("score", 0)

if __name__ == "__main__":
    game = MainGame()
    game.main_loop()

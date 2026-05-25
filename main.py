from os import system
from saves import GameState
import time

max_punkty = 1000
rate_of_change_punkty = -20

class MainGame:
    """Główna klasa zarządzająca zasobami gry"""
    
    def __init__(self):
        self._game_running = True # Zacznik działania gry, ustawienie go na false zakańcza grę
        self._input_string = "" # łańcuch z tekstem gracza
        self.game_mode = 0 # poziom trudności
        self.game_tryb = 0 # tryb gry - nauka/wyzwanie
        self.game_state = GameState()
        self.punkty = 0 #punkry gracza
        self.slowa = 0

    def main_loop(self):
        """Główna pętla gry zarządza kolejnością wykonywania się funkcji"""
        self._main_menu()
        czas = time.time()
        while self._game_running:
            if time.time() - czas >= 10.00:
                break
            self._game_output()
            self._game_input()
            self._screen_update()
        self._punktacja()
        

    def _main_menu(self):
        """menu główne gry"""
        self._screen_update()
        print("MISTRZ KLAWIATURY\n=================\n"
            "wybierz poziom trudności:\n1 - łatwy | 2 - średni | 3 - trudny\n")
        self.game_mode = input()
        print("Wybierz tryb gry\nnauka - tryb bez presji czasu | wyzwanie - tryb w którym zdobywasz punkty\n")
        self.game_tryb = input()
        print("'save' wykonuje zapis\n'quit' zakańcza grę\n'read' wczytuje poprzedni zapis\n")
        self._game_input()
        self._screen_update()
        self._tryb_gry()

    def _game_input(self):
        """zarządzanie wejściem programu"""
        self._input_string  = input()
        if self._input_string.lower() == 'quit': # warunki zakończenia gry
            self._game_running = False
        elif self._input_string.lower() == 'save': # warunek zapisu gry
            self._make_save()
        elif self._input_string.lower() == 'read': # warunek wczytania zapisu
            self._save_read()

    def _screen_update(self):
        """aktualizacja stanu ekranu"""
        system("cls")

    def _game_output(self): 
        """tutaj będzie pobierane słowo z klasy zarządzającej słowami"""
        print("wpisz słowo: ")

    # Ogólnie to wiem że dwie poniższe metody są trochę nieprzemyślane pod kątem tego,
    # że każda zmienna jest oddzielnie zapisywana/wczytywana przez dodatkowy słownik.
    # Najprościej by było poprostu zastąpić wszystkie pojedyńcze zmienne jednym dużym słownikiem,
    # do którego wszystko by było przepisywane za jednym razem.

    def _tryb_gry(self):
        if self.game_tryb == 'wyzwanie':
            self.czas = time.time()

    def _punktacja(self):
        nowe_punkty=0
        if self.slowa == 0:
            time_diff = time.time() - self.czas
            nowe_punkty += max_punkty + (rate_of_change_punkty*time_diff)
            print("Wpisałeś wszystkie słowa!!!!!\nudało ci się zdobyć ",nowe_punkty," punktów")
            self.punkty+=nowe_punkty
            

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
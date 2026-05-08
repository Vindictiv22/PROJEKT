from os import system

class MainGame:
    """Główna klasa zarządzająca zasobami gry"""
    
    def __init__(self):
        self._game_running = True # Zacznik działania gry, ustawienie go na false zakańcza grę
        self._input_string = "" # łańcuch z tekstem gracza
        self._game_mode = 0 # poziom trudności

    def main_loop(self):
        """Główna pętla gry zarządza kolejnością wykonywania się funkcji"""
        self._main_menu()
        while self._game_running:
            self._game_output()
            self._input_mgmt()
            input()
            self._screen_reset()

    def _main_menu(self):
        """menu główne gry"""
        self._screen_reset()
        print("MISTRZ KLAWIATURY\n=================\nwybierz poziom trudności:"
            "\n0 - domyślny")
        input()
        self._screen_reset()

    def _input_mgmt(self):
        """zarządzanie wejściem programu"""
        _input_string = input()
        if _input_string.lower() in ['q', 'quit']: # warunki  zakończenia gry
            self._game_running = False
        else:
            pass

    def _screen_update(self):
        """aktualizacja stanu ekranu"""
        system("cls")

    def _game_output(self): 
        """tutaj będzie pobierane słowo z klasy zarządzającej słowami"""
        print("wpisz słowo: ")

def main():
    if __name__ == '__main__':
        game = MainGame()
        game.main_loop()

main()
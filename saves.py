from pathlib import Path
import json

class GameState:
    """klasa obsługująca odczyt i zapis stanu gry"""
    def __init__(self):
        self._path = Path('data/saved.json')
        self.data = {'game_mode': 0}

    def file_read(self):
        """metoda odczytująca stan gry z pliku"""
        contents = self._path.read_text()
        self.data = json.loads(contents)
        return self.data

    def file_save(self):
        """metoda zapisująca stan gry do pliku"""
        print("zapisuję")
        print(self.data)
        contents = json.dumps(self.data)
        self._path.write_text(contents)
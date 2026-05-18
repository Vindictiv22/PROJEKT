from pathlib import Path
import json
from typing import Any

class GameState:
    """klasa obsługująca odczyt i zapis stanu gry"""
    def __init__(self):
        self._path = Path('data/saved.json')
        self.data : dict[str, Any] = {'game_mode': 0} 
        # ^słownik na wszystkie dane które mją być zapisane
        # ten dziwny zapis jest tylko po to żeby edytor mi nie wyrzucał błędów

    def file_read(self):
        """metoda odczytująca stan gry z pliku"""
        contents = self._path.read_text()
        self.data = json.loads(contents)
        return self.data

    def file_save(self):
        """metoda zapisująca stan gry do pliku"""
        contents = json.dumps(self.data)
        self._path.write_text(contents)
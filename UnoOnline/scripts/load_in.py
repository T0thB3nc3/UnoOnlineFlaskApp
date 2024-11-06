import os
from typing import List, Optional
# Kártya definiálása
class Card:
    def __init__(self, szin: str, ertek: Optional[int] = None, akcio: Optional[str] = None):
        self.szin = szin
        self.ertek = ertek
        self.akcio = akcio

    def __repr__(self):
        return f"Card(szin='{self.szin}', ertek={self.ertek}, akcio='{self.akcio}')"
    
# Kártyák beolvasása
def load_cards_from_folder(mappa: str) -> List[Card]:
    cards = []
    for filename in os.listdir(mappa):
        if filename.endswith(".jpg"):
            parts = filename.strip().split('_')
            if len(parts) >= 2:
                szin = parts[0]
                second_part = parts[1].split('.')[0]  # Remove file extension
                try:
                    ertek = int(second_part)
                    akcio = None
                except ValueError:
                    ertek = None
                    akcio = second_part
                card = Card(szin, ertek, akcio)
                cards.append(card)
                print(filename + 'kártya beolvasva!')
    return cards
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
        if filename.endswith(".svg"):
            parts = filename.strip().split('_')
            if len(parts) >= 2:
                szin = parts[0]
                second_part = parts[1:-1]
                second_part.append(parts[-1].split('.')[0])# fájlkiterjesztés lehúzása
                try:
                    ertek = int(second_part[0])
                    akcio = None
                except ValueError:
                    ertek = None
                    akcio = "_".join(x for x in second_part)
                card = Card(szin, ertek, akcio)
                cards.append(card)
                print(filename + ' kártya beolvasva!')
    return cards

def load_avatars(mappa: str):
    avatars = [os.path.splitext(file)[0] for file in os.listdir(mappa) if file.endswith('.svg')]
    return avatars

# Teszt futtatása
cards = (load_cards_from_folder('WebApp/static/cards'))
for i in cards:
    print(i)
avatars = load_avatars('WebApp/static/images/avatars')
for i in avatars:
    print(i)
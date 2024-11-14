import random
# Kártyák és színek alapdefiníciói
COLORS = ['Red', 'Green', 'Blue', 'Yellow']
ACTION_CARDS = ['Skip', 'Reverse', 'Draw Two', 'Wild', 'Wild Draw Four']
NUMBERS = [str(i) for i in range(0, 10)]
DECK = [f"{color} {num}" for color in COLORS for num in NUMBERS] + \
       [f"{color} {action}" for color in COLORS for action in ACTION_CARDS]

class Game:
    def __init__(self):
        self.deck = random.sample(DECK, len(DECK))  # Megkeverjük a paklit
        self.players = []  # A játékosok
        self.current_player = 0
        self.direction = 1  # 1 jelenti az óramutató járásával megegyező irányt, -1 az ellenkező irányt
        self.discard_pile = [] # kijátszott kártyák listája
        self.skip_next = False  # Skip akciók hatása
        self.winner = None
        self.uno_called = {}  # Tároljuk, hogy ki mondott UNO-t
        self.current_color = None  # A jelenlegi szín
        self.bot_players = ['Bot 1', 'Bot 2', 'Bot 3']  # Botok (később más játékosok) !TODO

    def start_game(self, num_players):
        self.players = ['Player'] + self.bot_players[:num_players - 1]
        self.deal_cards()
        self.discard_pile.append(self.deck.pop())  # Kezdő lap a feldobott pakliból

    def deal_cards(self):
        self.player_hands = {player: [self.deck.pop() for _ in range(7)] for player in self.players}

    def play_card(self, player, card, color=None):
        if card in self.player_hands[player]:
            # Ha a kártya "Wild" vagy "Wild Draw Four", akkor színt választunk
            if 'Wild' in card:
                self.current_color = color
                self.discard_pile.append(card)
                self.player_hands[player].remove(card)
                if 'Draw Four' in card:
                    self.draw_four(player)
                return True
            
            # Ha nem wild kártya, akkor normál játékkártyát rakunk
            if self.valid_card(card):
                self.player_hands[player].remove(card)
                self.discard_pile.append(card)
                
                # Akciók kezelése
                if "Skip" in card:
                    self.skip_next = True
                elif "Reverse" in card:
                    self.direction *= -1
                elif "Draw Two" in card:
                    self.draw_two(player)
                
                if len(self.player_hands[player]) == 1:
                    self.uno_called[player] = True
                return True
        return False

    def valid_card(self, card):
        if self.current_color is not None and card is not None and len(card.split()) == 2: # Csak akkor folytassuk, ha a szín be van állítva ÉS a formátum megfelelő
        # A kártya akkor érvényes, ha megegyezik a szín VAGY szám a feldobott pakli tetejével
            card_color, card_action = card.split()
            if self.current_color == card_color or card_action in self.discard_pile[-1] or 'Wild' in card_action:
                return True
        return False

    def next_player(self):
        if self.skip_next:
            self.skip_next = False
            return self.players[self.current_player]
        
        # A következő játékos meghatározása
        self.current_player = (self.current_player + self.direction) % len(self.players)
        return self.players[self.current_player]


    def draw_card(self, player):
        if len(self.deck) > 0:
            card = self.deck.pop()
            self.player_hands[player].append(card)
            return card
        else:
            return None  # Ha a pakli üres

    def draw_two(self):
        # Ha Draw Two kártyát játszanak, a következő játékos 2 kártyát húz
        next_player = self.players[(self.current_player + self.direction) % len(self.players)]
        self.player_hands[next_player].append(self.deck.pop())
        self.player_hands[next_player].append(self.deck.pop())

    def draw_four(self):
        # Ha Draw Four kártyát játszanak, a következő játékos 4 kártyát húz
        next_player = self.players[(self.current_player + self.direction) % len(self.players)]
        for _ in range(4):
            self.player_hands[next_player].append(self.deck.pop())

    def call_uno(self, player):
        if len(self.player_hands[player]) == 1:
            self.uno_called[player] = True
            return True
        return False

    def check_uno_penalty(self, player):
        if len(self.player_hands[player]) == 1 and player not in self.uno_called:
            # Ha valaki UNO-t mondott, de nem jelezte, akkor 2 kártyát húz
            self.player_hands[player].append(self.deck.pop()) # Tudom lehetne for ciklussal, de nincs az az Isten, hogy én 2 lapnak for ciklust írjak
            self.player_hands[player].append(self.deck.pop())
            return False
        return True

    def bot_play(self, player): # többjátékos esetén törlésre kerül !TODO
        # A botok egyszerű algoritmus alapján játszanak: első érvényes kártyát kijátszák, ha nem tudnak, akkor húznak
        valid_cards = [card for card in self.player_hands[player] if self.valid_card(card)]
        if valid_cards:
            card = valid_cards[0]
            self.play_card(player, card)
        else:
            card = self.draw_card(player)  # Ha nincs érvényes kártya, akkor húz
        self.next_player() # Kör átadása a következő játékosnak
        return card
           
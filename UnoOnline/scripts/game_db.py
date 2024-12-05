import sqlite3

class dbHandler:
    def __init__(self, db_file="scripts/db/game_database.db"):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_room(self, room_id):
        """Létrehoz egy szobát az adott ID-val."""
        try:
            self.cursor.execute("INSERT INTO Room (ID) VALUES (?)", (room_id,))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Szoba {room_id} már létezik vagy az ID érvénytelen.")
    
    def create_player(self, name, room_id):
        """Létrehoz egy játékost az adott szobában."""
        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id,))
        room = self.cursor.fetchone()
        if not room:
            raise ValueError(f"Szoba {room_id} nem létezik.")
        if room[0] >= 4:
            raise ValueError(f"Szoba {room_id} már tele van.")
        
        self.cursor.execute("INSERT INTO Player (Name, RoomID) VALUES (?, ?)", (name, room_id))
        self.cursor.execute("UPDATE Room SET PlayersCount = PlayersCount + 1 WHERE ID = ?", (room_id,))
        self.connection.commit()

    def delete_player(self, player_id):
        """Töröl egy játékost az ID alapján."""
        # Ha benne volt egy szobában, akkor törölje onnan
        ## Megkeresi a szobakódot
        self.cursor.execute(f"SELECT RoomID FROM Player WHERE ID = {player_id}")
        room_id = self.cursor.fetchone()
        ## Megkeresi a játékosszámot, ls eggyel csökkenti
        self.cursor.execute("UPDATE Room SET PlayersCount = PlayersCount - 1 WHERE ID = ?", (room_id,))
        # Kitörli a táblából
        self.cursor.execute("DELETE FROM Player WHERE ID = ?", (player_id,))
        self.connection.commit()

    def join_room(self, player_id, room_id):
        """Játékos belép egy 6-ossal kezdődő szobába."""
        if not str(room_id).startswith("6"):
            raise ValueError("Csak 6-ossal kezdődő szobába lehet belépni.")

        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id,))
        room = self.cursor.fetchone()
        if not room:
            raise ValueError(f"Szoba {room_id} nem létezik.")
        if room[0] >= 4:
            raise ValueError(f"Szoba {room_id} már tele van.")
        
        # Debugging: Ellenőrzés, hogy a játékos valóban létezik
        self.cursor.execute("SELECT RoomID FROM Player WHERE ID = ?", (player_id,))
        player = self.cursor.fetchone()
        if not player:
            raise ValueError(f"Játékos {player_id} nem található.")

        print(f"Assigning Player {player_id} to Room {room_id}...")  # Debugging
        
        if self.cursor.execute(f"SELECT RoomID from Player WHERE ID = {player_id}").fetchone() != room_id:
            self.cursor.execute("UPDATE Player SET RoomID = ? WHERE ID = ?", (room_id, player_id))
            self.cursor.execute("UPDATE Room SET PlayersCount = PlayersCount + 1 WHERE ID = ?", (room_id,))
        self.connection.commit()

        # Debugging: Ellenőrizzük a módosítást
        self.cursor.execute("SELECT RoomID FROM Player WHERE ID = ?", (player_id,))
        result = self.cursor.fetchone()
        print(f"Player {player_id} assigned to RoomID {result[0]}")  # Debugging

    def join_lobby(self, player_id):
        """Hozzárendeli a játékost egy lobby szobához, vagy új szobát hoz létre, ha szükséges."""
        
        # Ellenőrizzük, hogy van-e olyan lobby, ahol kevesebb mint 3 játékos van.
        self.cursor.execute("SELECT ID FROM Room WHERE ID LIKE '1%' AND PlayersCount < 3 LIMIT 1")
        available_room = self.cursor.fetchone()

        if available_room:
            # Ha létezik szoba, akkor a játékost hozzáadjuk ahhoz
            room_id = available_room[0]
            print(f"Játékos {player_id} csatlakoztatása a szobához {room_id}...")  # Debugging print
            if self.cursor.execute(f"SELECT RoomID from Player WHERE ID = {player_id}").fetchone() != room_id:
                self.cursor.execute("UPDATE Player SET RoomID = ? WHERE ID = ?", (room_id, player_id))
                self.cursor.execute("UPDATE Room SET PlayersCount = PlayersCount + 1 WHERE ID = ?", (room_id,))
        else:
            # Ha nincs elérhető szoba, akkor új lobby szobát hozunk létre
            print(f"Nincs elérhető lobby a {player_id} számára. Új szoba létrehozása.")  # Debugging print
            self.cursor.execute("INSERT INTO Room (PlayersCount) VALUES (1)")  # Új szoba létrehozása 1 játékossal
            new_room_id = self.cursor.lastrowid  # Az új szoba ID-ja
            self.cursor.execute("UPDATE Player SET RoomID = ? WHERE ID = ?", (new_room_id, player_id))
            self.cursor.execute("UPDATE Room SET PlayersCount = PlayersCount + 1 WHERE ID = ?", (new_room_id,))
            
        self.connection.commit()


    def end_session(self, room_id):
        """Befejez egy menetet: törli a játékosokat és a szobát."""
        self.cursor.execute("DELETE FROM Player WHERE RoomID = ?", (room_id,))
        self.cursor.execute("DELETE FROM Room WHERE ID = ?", (room_id,))
        self.connection.commit()

    def delete_room(self, room_id):
        """Töröl egy üres szobát."""
        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id,))
        room = self.cursor.fetchone()
        if not room:
            raise ValueError(f"Szoba {room_id} nem létezik.")
        if room[0] > 0:
            raise ValueError(f"Szoba {room_id} nem üres.")
        self.cursor.execute("DELETE FROM Room WHERE ID = ?", (room_id,))
        self.connection.commit()

    def close(self):
        """Lezárja az adatbázis kapcsolatot."""
        self.connection.close()

import unittest
import sqlite3
from scripts.game_db import dbHandler  # Importáljuk a megfelelő osztályt

class TestGameDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Sets up the database for testing."""
        cls.db_file = "test_game_database.db"
        cls.db_handler = dbHandler(cls.db_file)  # Új példány az osztályból

    def setUp(self):
        """Creates tables before each test."""
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Room (
                ID INTEGER PRIMARY KEY UNIQUE,   
                PlayersCount INTEGER DEFAULT 0,
                CHECK(ID BETWEEN 100000 AND 699999)
            );
        ''')
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Player (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                RoomID INTEGER NOT NULL,
                Name TEXT NOT NULL,
                FOREIGN KEY (RoomID) REFERENCES Room(ID) ON DELETE CASCADE
            );
        ''')
        self.connection.commit()

    def tearDown(self):
        """Clears the database after each test."""
        self.cursor.execute("DELETE FROM Player")
        self.cursor.execute("DELETE FROM Room")
        self.connection.commit()
        self.connection.close()

    def test_create_room(self):
        """Tests creating a room."""
        self.db_handler.create_room(100001)
        self.cursor.execute("SELECT ID FROM Room WHERE ID = 100001")
        room = self.cursor.fetchone()
        self.assertIsNotNone(room)
        self.assertEqual(room[0], 100001)

    def test_create_player(self):
        """Tests creating a player in a room."""
        self.db_handler.create_room(100002)
        self.db_handler.create_player("Player1", 100002)
        self.cursor.execute("SELECT Name FROM Player WHERE Name = 'Player1'")
        player = self.cursor.fetchone()
        self.assertIsNotNone(player)
        self.assertEqual(player[0], "Player1")

    def test_delete_player(self):
        """Tests deleting a player from a room."""
        self.db_handler.create_room(100003)
        self.db_handler.create_player("Player2", 100003)
        self.db_handler.delete_player(1)
        self.cursor.execute("SELECT ID FROM Player WHERE ID = 1")
        player = self.cursor.fetchone()
        self.assertIsNone(player)

    def test_join_lobby(self):
        """Tests a player joining a lobby or creating a new one if necessary."""
        # Töröljük a Player táblát a tiszta állapotért
        self.cursor.execute("DELETE FROM Player")
        self.connection.commit()

        # Létrehozunk egy szobát a lobbyba
        self.db_handler.create_room(100001)  # Létrehozzuk a lobby szobát

        # Létrehozunk egy játékost
        self.db_handler.create_player("Player15", 100001)
        self.cursor.execute("SELECT ID FROM Player WHERE Name = 'Player15'")
        player = self.cursor.fetchone()
        self.assertIsNotNone(player, "Player creation failed.")
        player_id = player[0]
        # Ellenőrizzük, hogy a szobához lett-e adva
        self.cursor.execute("SELECT RoomID FROM Player WHERE Name = 'Player15'")
        room_id = self.cursor.fetchone()
        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id))
        updated_room = self.cursor.fetchone()
        self.assertEqual(updated_room[0], 1, f"PlayersCount should be 1, but got {updated_room[0]}.")

        # Most próbáljuk beléptetni a játékost a lobbyba
        self.db_handler.join_lobby(player_id)  # Csatlakozás egy lobbiszobához

        # Ellenőrizzük, hogy valóban egy szobába került-e a játékos
        self.cursor.execute("SELECT RoomID FROM Player WHERE ID = ?", (player_id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Player should be assigned to a room.")
        room_id = result[0]

        # Ellenőrizzük, hogy a játékos a lobby szobájában van-e
        self.assertTrue(str(room_id).startswith('1'), "Player should be assigned to a lobby room starting with 1.")

        # Ellenőrizzük a szoba játékosszámát
        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id,))
        updated_room = self.cursor.fetchone()
        self.assertEqual(updated_room[0], 2, f"PlayersCount should be 2, but got {updated_room[0]}.")

        # Ellenőrizzük a lobby szoba létrehozását, ha új szoba lett létrehozva
        if updated_room[0] == 1:
            self.cursor.execute("SELECT ID FROM Room WHERE ID = 100001")
            existing_room = self.cursor.fetchone()
            self.assertIsNone(existing_room, "Lobby room 100001 should not exist anymore.")
        else:
            self.assertIsNotNone(updated_room, "New room should have been created.")

    def test_join_room(self):
        """Tests a player joining a random 6xxxxx room."""
        room_id = 600001

        # Létrehozunk egy szobát, ha még nem létezik
        self.db_handler.create_room(room_id)
        
        # Létrehozunk egy játékost a szobához
        self.db_handler.create_player("Player4", room_id)
        # Szobaméret változásának ellenőrzése
        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id,))
        updated_room = self.cursor.fetchone()
        self.assertEqual(updated_room[0], 1, f"PlayersCount should be 1, but got {updated_room[0]}.")

        # Lekérdezzük a játékos ID-ját közvetlenül a create_player után
        self.cursor.execute("SELECT ID FROM Player WHERE Name = 'Player4'")
        player = self.cursor.fetchone()
        self.assertIsNotNone(player, "Player creation failed.")
        player_id = player[0]  # A játékos ID-ja

        # Ellenőrizzük, hogy a szoba játékosszáma nem haladja-e meg a 4-et
        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id,))
        room = self.cursor.fetchone()
        self.assertIsNotNone(room)
        self.assertLess(room[0], 4, f"Room {room_id} is full.")  # A szobának kevesebb mint 4 játékosa kell legyen

        # Most próbáljuk beléptetni a játékost a szobába
        self.db_handler.join_room(player_id, room_id)  # Csatlakozás a szobához

        # Ellenőrizzük, hogy a játékos szobája tényleg a 600001-es szoba
        self.cursor.execute("SELECT RoomID FROM Player WHERE ID = ?", (player_id,))
        result = self.cursor.fetchone()
        print(f"Player RoomID: {result}")  # Debugging print
        self.assertIsNotNone(result, "Player should have a RoomID assigned.")
        room_id_result = result[0]
        self.assertEqual(room_id_result, room_id, "Player should be assigned to the correct room.")

        # Ellenőrizzük a szoba játékosszámát, hogy nőtt-e 1-el
        self.cursor.execute("SELECT PlayersCount FROM Room WHERE ID = ?", (room_id,))
        updated_room = self.cursor.fetchone()
        self.assertEqual(updated_room[0], 2, f"PlayersCount should be 2, but got {updated_room[0]}.")

    def test_end_session(self):
        """Tests ending a session (deleting all players and room)."""
        self.db_handler.create_room(100007)
        self.db_handler.create_player("Player5", 100007)
        self.db_handler.end_session(100007)  # Ends the session for room 100007
        self.cursor.execute("SELECT ID FROM Room WHERE ID = 100007")
        room = self.cursor.fetchone()
        self.assertIsNone(room)

    def test_delete_room(self):
        """Tests deleting an empty room."""
        self.db_handler.create_room(100008)
        self.db_handler.delete_room(100008)  # Should delete the room if it's empty
        self.cursor.execute("SELECT ID FROM Room WHERE ID = 100008")
        room = self.cursor.fetchone()
        self.assertIsNone(room)

if __name__ == "__main__":
    unittest.main()

-- Tábla törlése, ha létezik
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Room;

-- Room tábla újra létrehozása
CREATE TABLE Room (
    ID INTEGER PRIMARY KEY UNIQUE,   -- Egyedi azonosító, elsődleges kulcs
    PlayersCount INTEGER DEFAULT 0 CHECK(PlayersCount BETWEEN 0 AND 4), -- Játékosok száma (0-4 között)
    CHECK(ID BETWEEN 100000 AND 699999)  -- Az ID értéke 100000 és 699999 között lehet
);

-- Player tábla újra létrehozása
CREATE TABLE Player (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Generált egyedi azonosító
    RoomID INTEGER,               -- Idegen kulcs a Room.ID oszlopra
    Name TEXT NOT NULL,                    -- Játékos neve
    FOREIGN KEY (RoomID) REFERENCES Room(ID) ON DELETE CASCADE  -- Kapcsolat a Room táblával
);

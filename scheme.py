import sqlite3


if __name__ == "__main__":
    # Подключаемся к базе данных (или создаем, если ее нет)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Создание таблицы операторов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Operator (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL
    )
    ''')

    # Создание таблицы рабочих зон
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Work_Zone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        x REAL NOT NULL,
        y REAL NOT NULL,
        width REAL NOT NULL,
        height REAL NOT NULL,
        zone_name TEXT NOT NULL
    )
    ''')

    # Создание таблицы зон для складирования листов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Storage_Area (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        x REAL NOT NULL,
        y REAL NOT NULL,
        width REAL NOT NULL,
        height REAL NOT NULL,
        location_name TEXT NOT NULL,
        work_zone_id INTEGER NOT NULL,
        FOREIGN KEY (work_zone_id) REFERENCES Work_Zone(id)
    )
    ''')

    # Создание таблицы состояний (State)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS State (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')

    # Создание таблицы заданий (Task)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operator_id INTEGER NOT NULL,
        creation_date TEXT DEFAULT CURRENT_TIMESTAMP,
        comment TEXT,
        start_date TEXT DEFAULT "",
        end_date TEXT   DEFAULT "",
        sheet_count INTEGER NOT NULL,
        from_id INTEGER NOT NULL,
        to_id INTEGER NOT NULL,
        state_id INTEGER NOT NULL,
        FOREIGN KEY (operator_id) REFERENCES Operator(id),
        FOREIGN KEY (from_id) REFERENCES Storage_Area(id),
        FOREIGN KEY (to_id) REFERENCES Storage_Area(id),
        FOREIGN KEY (state_id) REFERENCES State(id)
    )
    ''')

    cursor.execute('''
        INSERT INTO Operator (full_name) VALUES (?)
        ''',
        ["Ruslan", ],
    )

    # Заполнение таблицы State начальными данными (состояния)
    cursor.executemany('''
    INSERT INTO State (id, name) VALUES (?, ?)
    ''', [
        (0, 'Не начато'),
        (1, 'В процессе'),
        (2, 'Завершено')
    ])

    cursor.executemany("""
    INSERT INTO Work_Zone (x, y, width, height, zone_name) VALUES (?, ?, ?, ?, ?)
    """, [
        (3 / 4, 0, 1 / 4, 1 / 3, "ZONE work#1"),
        (1 / 4, 1 / 3, 2 / 4, 1 / 3, "ZONE work#2"),
        (0, 2 / 3, 3 / 4, 1 / 3, "ZONE work#3")
    ])
    conn.commit()
    cursor.executemany("""
        INSERT INTO Storage_Area (x, y, width, height, location_name, work_zone_id) VALUES (?, ?, ?, ?, ?, ?)
        """, [
        (0.05, 0.07, 1 / 12, 1 / 15, "place1", 1),
        (0.05, 0.07, 1 / 12, 1 / 15, "place2", 2),
        (0.05, 0.07, 1 / 12, 1 / 15, "place3", 3)
    ])
    conn.commit()
    cursor.executemany("""
            INSERT INTO Task (operator_id, sheet_count, from_id, to_id, state_id) VALUES (?, ?, ?, ?, ?)
            """, [
        (1, 24, 1, 2, 0),
        (1, 24, 2, 3, 0),
        (1, 24, 3, 1, 0),
        (1, 24, 1, 3, 0),


    ])
    conn.commit()

    conn.close()
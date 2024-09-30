import sqlite3

# Подключение к базе данных (если файла нет, он будет создан)
conn = sqlite3.connect('game_database.db')

# Создание объекта курсора
cursor = conn.cursor()

# SQL-запросы для создания таблиц
create_tables_queries = [
    '''
    CREATE TABLE IF NOT EXISTS Characters (
        character_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT NOT NULL UNIQUE,
        level INTEGER NOT NULL,
        experience INTEGER NOT NULL,
        credits INTEGER NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Attributes (
        attribute_id INTEGER PRIMARY KEY AUTOINCREMENT,
        attribute_name TEXT NOT NULL UNIQUE,
        credit_cost_for_upgrade INTEGER NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS CharacterAttributes (
        character_id INTEGER,
        attribute_id INTEGER,
        attribute_level INTEGER NOT NULL,
        FOREIGN KEY (character_id) REFERENCES Characters(character_id),
        FOREIGN KEY (attribute_id) REFERENCES Attributes(attribute_id),
        PRIMARY KEY (character_id, attribute_id)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT NOT NULL UNIQUE,
        credit_cost_for_upgrade INTEGER NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS CharacterSkills (
        character_id INTEGER,
        skill_id INTEGER,
        skill_level INTEGER NOT NULL,
        FOREIGN KEY (character_id) REFERENCES Characters(character_id),
        FOREIGN KEY (skill_id) REFERENCES Skills(skill_id),
        PRIMARY KEY (character_id, skill_id)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Abilities (
        ability_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ability_name TEXT NOT NULL UNIQUE,
        credit_cost_to_learn INTEGER NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS CharacterAbilities (
        character_id INTEGER,
        ability_id INTEGER,
        learned INTEGER NOT NULL CHECK (learned IN (0, 1)),
        FOREIGN KEY (character_id) REFERENCES Characters(character_id),
        FOREIGN KEY (ability_id) REFERENCES Abilities(ability_id),
        PRIMARY KEY (character_id, ability_id)
    )
    '''
]

# Выполнение запросов на создание таблиц
for query in create_tables_queries:
    cursor.execute(query)

# Сохранение изменений
conn.commit()

# Закрытие соединения
conn.close()

print("База данных создана успешно.")
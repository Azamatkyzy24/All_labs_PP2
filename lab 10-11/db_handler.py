import psycopg2 

conn = psycopg2.connect(
    database='snake_game',
    user='postgres', 
    host='localhost', 
    password='1465',
    port=5432
)

conn.autocommit = True

current_user = ''

# Создание таблиц
query_create_table_users = """
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(255) UNIQUE
    )
"""

query_create_table_user_scores = """
    CREATE TABLE IF NOT EXISTS user_scores(
        user_id SERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(255),
        score INT,
        level INT
    )
"""

# Выполнение SQL-запросов
def execute_query(query): 
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Ввод имени пользователя
def input_user(username):
    global current_user
    if username:
        current_user = username
    else:
        print("Invalid username!")

# Добавление нового пользователя
def add_user(name):
    command = 'INSERT INTO users(username) VALUES (%s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Проверка существования пользователя в базе
def check_user_exists(name):
    command = 'SELECT * FROM users WHERE username = %s'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            result = cur.fetchall()
            return bool(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Добавление нового счета для пользователя
def add_new_score(score, level):
    command = "INSERT INTO user_scores(username, score, level) VALUES (%s, %s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user, score, level))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Обработка счета пользователя
def process_score(score, level):
    user_exists = check_user_exists(current_user)
    if not user_exists:
        add_user(current_user)
    add_new_score(score, level)

# Получение самого высокого уровня для пользователя
def show_highest_level():
    command = 'SELECT MAX(level) FROM user_scores WHERE username = %s'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user,))
            result = cur.fetchall()
            return result if result[0][0] else [(0,)]  # Если результата нет, вернуть [(0,)]
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return [(0,)]  # Возвращаем дефолтное значение при ошибке
from flask import Flask, request, render_template_string
import sqlite3
import os

# Создаём экземпляр Flask-приложения
app = Flask(__name__)

print("App is running!")

# Вывод маршрутов
print(app.url_map)

# Функция инициализации базы данных
def init_db():
    """
    Создаёт базу данных, если её нет, и добавляет в неё пользователей.
    """
    print("Initializing database...")
    conn = sqlite3.connect('users.db')
    c = conn.cursor()    

    # Создание таблицы пользователей, если её нет
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, is_admin INTEGER)')
    
    # Проверяем, есть ли записи в таблице
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        # Добавляем пользователей: администратора и обычного пользователя
        c.execute("INSERT INTO users (username, password, is_admin) VALUES ('admin', 'password123', 1)")
        c.execute("INSERT INTO users (username, password, is_admin) VALUES ('user', 'user123', 0)")
        print("Users 'admin' and 'user' added to the database.")
    
    conn.commit()
    conn.close()

    # Проверяем, создался ли файл базы данных
    if os.path.exists('users.db'):
        print("Database file created: users.db")
    else:
        print("Database file not created!")

init_db()

# Маршрут для главной страницы
@app.route('/')
def home():
    """
    Главная страница с ссылками на другие разделы приложения.
    """
    return '''
        <h1>Welcome to the Vulnerable App!</h1>
        <p><a href="/login">Go to Login Page</a></p>
        <p><a href="/comments">Go to Comments Page</a></p>
        <p><a href="/search">Go to Search Page</a></p>
    '''

# Уязвимость SQL-инъекции
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Форма входа с уязвимостью SQL-инъекции.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Подключаемся к базе данных
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Уязвимость: динамическая вставка данных в SQL-запрос без параметризованных запросов
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing query: {query}") # Логируем выполняемый запрос (для отладки)
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            clean_username = user[0]  # Возьмём имя пользователя из базы данных
            if user[2] == 1:   # Проверяем, является ли пользователь администратором
                return f"Login successful! Welcome, {clean_username}! You are an administrator."
            else:
                return f"Login successful! Welcome, {clean_username}! You are a regular user."
        else:
            return "Invalid credentials!"

    # HTML-форма входа
    return '''
        <form method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Уязвимость XSS (открытая форма для комментариев)
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    """
    Раздел комментариев с уязвимостью XSS (код сохраняется и выполняется при загрузке страницы).
    """
    if request.method == 'POST':
        comment = request.form['comment']
        # Сохраняем комментарий в файл (без фильтрации, что создаёт XSS-уязвимость)
        with open('comments.txt', 'a') as f:
            f.write(comment + '\n')

    comments = ''
    if os.path.exists('comments.txt'):
        with open('comments.txt', 'r') as f:
            comments = f.read()

    # Отображаем комментарии на странице (включая потенциально вредоносный код)
    return '''
        <h1>Comments</h1>
        <form method="POST">
            <input type="text" name="comment" placeholder="Leave a comment">
            <input type="submit" value="Submit">
        </form>
        
    ''' + comments

# Уязвимость RCE (Remote Code Execution) через поле поиска
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']

        # Проверка на пустой ввод
        if not query.strip():
            return "No command provided!"

        # Уязвимость: передача введённого текста напрямую в системную команду
        command = f"{query.strip()}"
        print(f"Executing command: {command}") # Логируем выполняемую команду
        try:
            result = os.popen(command).read() # Выполняем системную команду
        except Exception as e:
            result = f"Error executing command: {e}"

        return f"<pre>{result}</pre>"

    # HTML-форма поиска
    return '''
        <h1>Search</h1>
        <form method="POST">
            Search: <input type="text" name="query"><br>
            <input type="submit" value="Search">
        </form>
    '''

# Вывод зарегистрированных маршрутов
for rule in app.url_map.iter_rules():
    print(f"Registered route: {rule}")

# Запуск приложения
if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, use_reloader=False)
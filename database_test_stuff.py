import sqlite3

test_author = "test_author"
test_message = "LAST ANOTHER TEST MESSAGE"

connection = sqlite3.connect('messages.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, author text NOT NULL, message text NOT NULL);')
cursor.execute(f'INSERT INTO messages (author, message) VALUES("test_author", "LAST ANOTHER TEST MESSAGE");')
#for i in cursor.execute("SELECT * FROM messages ORDER BY id DESC;"):
#cursor.execute('DROP TABLE users;')
cursor.execute('CREATE TABLE IF NOT EXISTS users(user text PRIMARY KEY, address text);')
print(cursor.execute('INSERT INTO users VALUES("UserA", "");'))
cursor.execute('INSERT INTO users VALUES("UserB", "");')
connection.commit()
connection.close()
import sqlite3

test_author = "test_author"
test_message = "LAST ANOTHER TEST MESSAGE"

connection = sqlite3.connect('messages.db')
cursor = connection.cursor()
cursor.execute(f'INSERT INTO messages (author, message) VALUES("test_author", "LAST ANOTHER TEST MESSAGE");')
#for i in cursor.execute("SELECT * FROM messages ORDER BY id DESC;"):
connection.close()
import sqlite3

connection = sqlite3.connect('messages.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, author text NOT NULL, message text NOT NULL);')

"""
Add message to database
"""
def add_message(author, message):
    cursor.execute(f'INSERT INTO messages (author, message) VALUES("{author}", "{message}")')

"""
Get last four messages from database
"""
def get_most_recent_msgs():
    msg = ''
    for i in cursor.execute("SELECT TOP 4 * FROM messages ORDER BY id DESC")
        msg += f"{i[1]}: {i[2]}\n"
    return msg[:-1]

connection.close()
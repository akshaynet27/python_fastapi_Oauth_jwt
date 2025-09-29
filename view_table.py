import sqlite3
from tabulate import tabulate

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print("Tables:", cursor.fetchall())

cursor.execute("SELECT * FROM sellers")  # Replace 'products' with your table name
rows = cursor.fetchall()
columns = []
for description in cursor.description:
    columns.append(description[0])

print(tabulate(rows, headers=columns, tablefmt="grid"))
conn.close()
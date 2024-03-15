import sqlite3

CONN = sqlite3.connect("db/student.db") # making con
CURSOR = CONN.cursor() # interact with the db
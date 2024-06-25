import sqlite3

def verify_database():
    conn = sqlite3.connect('pokemon_cards.db')
    c = conn.cursor()

    c.execute("SELECT * FROM cards LIMIT 5")
    rows = c.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == '__main__':
    verify_database()

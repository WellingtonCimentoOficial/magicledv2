import sqlite3

def create_database():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    try:
        cursor.execute("CREATE TABLE devices (device text, token text)")
        db.commit()
        db.close()
    except:
        pass


db = sqlite3.connect("database.db")
cursor = db.cursor()


def add_token(device, token):
    try:
        cursor.execute("INSERT INTO devices VALUES (?, ?)", (device, token))
        db.commit()
        return True
    except Exception as e:
        print(e)

def rem_token(device):
    try:
        cursor.execute("DELETE FROM devices WHERE device = '" + device + "'")
        db.commit()
        return True
    except:
        print("Erro ao deletar o dispositivo")

def list_devices():
    cursor.execute("SELECT device FROM devices")
    return cursor.fetchall()

def list_device(device):
    for token in cursor.execute("SELECT token FROM devices WHERE device = '" + device + "'"):
        return token[0]
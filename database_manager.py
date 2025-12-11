import sqlite3
import hashlib

class DatabaseManager:
    def __init__(self, dbName="dormitory.db"):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()
        self.createTables()

    def createTables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                passwordHash TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dorms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ownerId INTEGER,
                location TEXT,
                details TEXT,
                price REAL,
                contactInfo TEXT,
                imagePath TEXT,
                FOREIGN KEY(ownerId) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def registerUser(self, firstName, lastName, email, password):
        passwordHash = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (firstName, lastName, email, passwordHash) VALUES (?, ?, ?, ?)",
                                (firstName, lastName, email, passwordHash))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verifyUser(self, email, password):
        passwordHash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE email = ? AND passwordHash = ?", (email, passwordHash))
        return self.cursor.fetchone()

    def addDorm(self, ownerId, location, details, price, contactInfo, imagePath):
        self.cursor.execute("""
            INSERT INTO dorms (ownerId, location, details, price, contactInfo, imagePath)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ownerId, location, details, price, contactInfo, imagePath))
        self.conn.commit()

    def getAllDorms(self):
        self.cursor.execute("SELECT * FROM dorms")
        return self.cursor.fetchall()

    def getDormById(self, dormId):
        self.cursor.execute("SELECT * FROM dorms WHERE id = ?", (dormId,))
        return self.cursor.fetchone()

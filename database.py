import sqlite3
import json

class Database:
    def __init__(self, database_file,  logger):
        self.database_file = database_file
        self.conn = sqlite3.connect(self.database_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.logger = logger

    def init_db(self):
        """Initialize the database and create tables if they do not exist."""
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS Servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                last_ping_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS Pings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                FOREIGN KEY(server_id) REFERENCES Servers(id)
            );

            CREATE TABLE IF NOT EXISTS Connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id INTEGER NOT NULL,
                ping_id INTEGER NOT NULL,
                connection TEXT NOT NULL,
                last_update REAL,
                FOREIGN KEY(server_id) REFERENCES Servers(id),
                FOREIGN KEY(ping_id) REFERENCES Pings(id)
            );
            """
        )
        self.conn.commit()

    def insert_ping(self, server, timestamp, connection_data):
        try:
            # Get or create server
            self.cursor.execute('INSERT OR IGNORE INTO Servers (name) VALUES (?)', (server,))
            self.cursor.execute('SELECT id FROM Servers WHERE name = ?', (server,))
            server_id = self.cursor.fetchone()[0]
    
            # Insert ping
            self.cursor.execute('INSERT INTO Pings (server_id, timestamp) VALUES (?, ?)',
                                (server_id, timestamp))
            ping_id = self.cursor.lastrowid
    
            # Update server's last_ping_id
            self.cursor.execute('UPDATE Servers SET last_ping_id = ? WHERE id = ?', (ping_id, server_id))
    
            # Get existing connections for this server
            self.cursor.execute('SELECT connection FROM Connections WHERE server_id = ?', (server_id,))
            existing_connections = set(row[0] for row in self.cursor.fetchall())
    
            # Insert or update connections
            connections = json.loads(connection_data)
            for connection, last_update in connections.items():
                if last_update is None:
                    last_update = 0  # Use 0 to represent a down connection
                self.cursor.execute('''
                    INSERT OR REPLACE INTO Connections (server_id, ping_id, connection, last_update)
                    VALUES (?, ?, ?, ?)
                ''', (server_id, ping_id, connection, last_update))
    
                if connection in existing_connections:
                    existing_connections.remove(connection)
    
            # Remove connections that are no longer reported
            for connection in existing_connections:
                self.cursor.execute('DELETE FROM Connections WHERE server_id = ? AND connection = ?',
                                    (server_id, connection))
    
            self.conn.commit()
        except Exception as e:
            self.logger.error(f"Error inserting ping: {e}")
            self.conn.rollback()

    def get_server_statuses(self):
        query = """
            SELECT
                s.name AS server,
                p.timestamp AS last_ping_time,
                c.connection,
                c.last_update
            FROM
                Servers s
            JOIN
                Pings p ON s.last_ping_id = p.id
            JOIN
                Connections c ON p.id = c.ping_id
            ORDER BY
                s.name, c.connection;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def end(self):
        self.conn.commit()
        self.conn.close()

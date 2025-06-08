import sqlite3

class DatabaseManager:
    def __init__(self, db_path='josaa_updates.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables (as defined in schema above)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS josaa_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                pdf_url TEXT,
                pdf_content TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scraped_at TIMESTAMP,
                is_processed BOOLEAN DEFAULT FALSE,
                is_sent BOOLEAN DEFAULT FALSE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authorization_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                update_id INTEGER,
                drafted_message TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                processed_by TEXT,
                FOREIGN KEY (update_id) REFERENCES josaa_updates(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def is_update_new(self, url):
        """Check if update already exists in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM josaa_updates WHERE url = ?", (url,))
        result = cursor.fetchone()
        conn.close()
        return result is None
    
    def save_update(self, update_data):
        """Save new update to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO josaa_updates (title, url, pdf_url, pdf_content, summary, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            update_data['title'],
            update_data['url'],
            update_data.get('pdf_url'),
            update_data.get('pdf_content'),
            update_data.get('summary'),
            update_data['scraped_at']
        ))
        update_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return update_id
    
    def create_authorization_request(self, update_id, drafted_message):
        """Create authorization request for admin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO authorization_requests (update_id, drafted_message)
            VALUES (?, ?)
        ''', (update_id, drafted_message))
        conn.commit()
        conn.close()
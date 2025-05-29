import sqlite3
import json
from models.user import User, Role
from models.file_record import FileRecord, UploadStatus
from datetime import datetime
import bcrypt
from validators.custom_serializer import custom_serialize


class DatabaseService:
    def __init__(self, db_path="storage/app.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS file_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uploader TEXT NOT NULL,
                    path TEXT NOT NULL,
                    metadata TEXT,
                    status TEXT NOT NULL,
                    approved_by TEXT,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY(uploader) REFERENCES users(username)
                )
            """)

    # User methods
    def add_user(self, user: User):
        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                (user.username, hashed_password, user.role.value)
            )

    def login(self, username: str, password: str) -> User | None:
        cur = self.conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and bcrypt.checkpw(password.encode(), row["password"]):
            return User(username=row["username"], password=row["password"], role=Role(row["role"]))
        return None


    def get_user(self, username: str) -> User | None:
        cur = self.conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            return User(username=row["username"], role=Role(row["role"]), password=row["password"])
        return None


    def add_file_record(self, record: FileRecord):
        metadata_json = None
        if record.metadata is not None:
            try:
                # Create a copy of metadata to avoid modifying the original
                metadata_copy = record.metadata.copy() if isinstance(record.metadata, dict) else record.metadata
                metadata_json = json.dumps(metadata_copy, indent=2, default=custom_serialize)
            except Exception as e:
                print(f"Warning: Could not serialize metadata: {e}")
                metadata_json = None

        with self.conn:
            cur = self.conn.execute(
                """INSERT INTO file_records 
                (uploader, path, metadata, status) 
                VALUES (?, ?, ?, ?)""",
                (
                    record.uploader.username,
                    record.path,
                    metadata_json,
                    record.status.value
                )
            )
            record.id = cur.lastrowid

    def update_file_record(self, record: FileRecord):
        metadata_json = None
        if record.metadata is not None:
            try:
                # Create a copy of metadata to avoid modifying the original
                metadata_copy = record.metadata.copy() if isinstance(record.metadata, dict) else record.metadata
                metadata_json = json.dumps(metadata_copy, indent=2, default=custom_serialize)
            except Exception as e:
                print(f"Warning: Could not serialize metadata: {e}")
                metadata_json = None
        with self.conn:
            self.conn.execute(
                """UPDATE file_records SET 
                metadata = ?, status = ? WHERE id = ?""",
                (
                    metadata_json,
                    record.status.value,
                    record.id
                )
            )


    def get_file_record(self, record_id: int) -> FileRecord | None:
        cur = self.conn.execute("SELECT * FROM file_records WHERE id = ?", (record_id,))
        row = cur.fetchone()
        if row:
            upload_user = self.get_user(row["uploader"])
            approved_by = self.get_user(row["approved_by"]) if row["approved_by"] else None
            metadata = json.loads(row["metadata"]) if row["metadata"] else None
            record = FileRecord(upload_user, row["path"])
            record.uploader = upload_user
            record.id = row["id"]
            record.metadata = metadata
            record.status = UploadStatus(row["status"])
            record.approved_by = approved_by

            record.created_at = datetime.fromisoformat(row["created_at"]) if row["created_at"] else None
            return record
        return None

    def list_file_records(self):
        cur = self.conn.execute("SELECT id FROM file_records")
        records = []
        for row in cur:
            record = self.get_file_record(row["id"])
            if record:
                records.append(record)
        return records
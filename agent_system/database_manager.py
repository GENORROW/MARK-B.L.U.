# agent_system/database_manager.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
import json
import hashlib
import secrets
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from contextlib import contextmanager
from agent_system.agent_identity import AgentIdentity

class AdminAuth:
    """Handles admin authentication and access control."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_admin_table()
    
    def _init_admin_table(self):
        """Initialize admin credentials table."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def create_admin(self, username: str, password: str) -> bool:
        """
        Create a new admin user.
        
        Args:
            username: Admin username
            password: Admin password (will be hashed)
            
        Returns:
            bool: True if successful, False if username exists
        """
        salt = secrets.token_hex(32)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO admins (username, password_hash, salt)
                    VALUES (?, ?, ?)
                """, (username, password_hash, salt))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_admin(self, username: str, password: str) -> bool:
        """
        Verify admin credentials.
        
        Args:
            username: Admin username
            password: Admin password
            
        Returns:
            bool: True if credentials are valid
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password_hash, salt FROM admins WHERE username = ?
            """, (username,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            stored_hash, salt = result
            input_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            
            if input_hash == stored_hash:
                # Update last login
                cursor.execute("""
                    UPDATE admins SET last_login = CURRENT_TIMESTAMP
                    WHERE username = ?
                """, (username,))
                conn.commit()
                return True
            
            return False
    
    def admin_exists(self, username: str) -> bool:
        """
        Check if an admin user exists.
        
        Args:
            username: Admin username to check
            
        Returns:
            bool: True if admin exists
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM admins WHERE username = ?
            """, (username,))
            count = cursor.fetchone()[0]
            return count > 0
    
    def list_admins(self) -> List[Dict]:
        """List all admin users (no passwords)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT admin_id, username, created_at, last_login
                FROM admins
            """)
            
            admins = []
            for row in cursor.fetchall():
                admins.append({
                    'admin_id': row[0],
                    'username': row[1],
                    'created_at': row[2],
                    'last_login': row[3]
                })
            
            return admins


class IdentityDatabase:
    """Centralized database for managing drone identities."""
    
    def __init__(self, db_path: str = "data/drone_identities.db"):
        """
        Initialize the identity database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database schema
        self._init_database()
        
        # Initialize admin auth
        self.auth = AdminAuth(db_path)
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Drone identities table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS identities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial TEXT NOT NULL,
                    timeslot INTEGER NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    qrng_seed TEXT NOT NULL,
                    badge TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(serial, timeslot)
                )
            """)
            
            # Communication logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS communication_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sender_serial TEXT NOT NULL,
                    receiver_serial TEXT NOT NULL,
                    sender_timeslot INTEGER NOT NULL,
                    receiver_timeslot INTEGER NOT NULL,
                    message_hash TEXT NOT NULL,
                    encrypted_message TEXT NOT NULL,
                    verified BOOLEAN DEFAULT 0,
                    FOREIGN KEY (sender_serial) REFERENCES identities(serial),
                    FOREIGN KEY (receiver_serial) REFERENCES identities(serial)
                )
            """)
            
            # Fleet metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fleet_metadata (
                    fleet_id TEXT PRIMARY KEY,
                    num_drones INTEGER NOT NULL,
                    current_timeslot INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_serial_timeslot 
                ON identities(serial, timeslot)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_communication_timestamp 
                ON communication_logs(timestamp)
            """)
            
            conn.commit()
    
    def store_identity(self, identity: AgentIdentity) -> bool:
        """
        Store a drone identity in the database.
        
        Args:
            identity: AgentIdentity object to store
            
        Returns:
            bool: True if successful
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO identities (serial, timeslot, timestamp, qrng_seed, badge)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    identity.serial,
                    identity.timeslot,
                    identity.timestamp.isoformat(),
                    identity.qrng_seed.hex(),
                    identity.badge.hex()
                ))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Identity already exists for this serial/timeslot
            return False
    
    def store_multiple_identities(self, identities: List[AgentIdentity]) -> Tuple[int, int]:
        """
        Store multiple drone identities.
        
        Args:
            identities: List of AgentIdentity objects
            
        Returns:
            Tuple[int, int]: (successful_count, failed_count)
        """
        successful = 0
        failed = 0
        
        for identity in identities:
            if self.store_identity(identity):
                successful += 1
            else:
                failed += 1
        
        return successful, failed
    
    def get_identity(self, serial: str, timeslot: int) -> Optional[AgentIdentity]:
        """
        Retrieve a specific drone identity.
        
        Args:
            serial: Drone serial number
            timeslot: Timeslot number
            
        Returns:
            AgentIdentity or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT serial, timeslot, timestamp, qrng_seed, badge
                FROM identities
                WHERE serial = ? AND timeslot = ?
            """, (serial, timeslot))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return AgentIdentity(
                serial=row['serial'],
                timeslot=row['timeslot'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                qrng_seed=bytes.fromhex(row['qrng_seed']),
                badge=bytes.fromhex(row['badge'])
            )
    
    def get_current_identity(self, serial: str) -> Optional[AgentIdentity]:
        """
        Get the most recent identity for a drone.
        
        Args:
            serial: Drone serial number
            
        Returns:
            AgentIdentity or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT serial, timeslot, timestamp, qrng_seed, badge
                FROM identities
                WHERE serial = ?
                ORDER BY timeslot DESC
                LIMIT 1
            """, (serial,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            return AgentIdentity(
                serial=row['serial'],
                timeslot=row['timeslot'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                qrng_seed=bytes.fromhex(row['qrng_seed']),
                badge=bytes.fromhex(row['badge'])
            )
    
    def get_all_identities_for_timeslot(self, timeslot: int) -> List[AgentIdentity]:
        """
        Get all drone identities for a specific timeslot.
        
        Args:
            timeslot: Timeslot number
            
        Returns:
            List of AgentIdentity objects
        """
        identities = []
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT serial, timeslot, timestamp, qrng_seed, badge
                FROM identities
                WHERE timeslot = ?
                ORDER BY serial
            """, (timeslot,))
            
            for row in cursor.fetchall():
                identities.append(AgentIdentity(
                    serial=row['serial'],
                    timeslot=row['timeslot'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    qrng_seed=bytes.fromhex(row['qrng_seed']),
                    badge=bytes.fromhex(row['badge'])
                ))
        
        return identities
    
    def log_communication(self, sender_serial: str, receiver_serial: str,
                         sender_timeslot: int, receiver_timeslot: int,
                         encrypted_message: bytes, verified: bool = False) -> int:
        """
        Log a communication event between drones.
        
        Args:
            sender_serial: Sender drone serial
            receiver_serial: Receiver drone serial
            sender_timeslot: Sender's timeslot
            receiver_timeslot: Receiver's timeslot
            encrypted_message: Encrypted message bytes
            verified: Whether communication was verified
            
        Returns:
            int: Log ID
        """
        message_hash = hashlib.sha256(encrypted_message).hexdigest()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO communication_logs 
                (sender_serial, receiver_serial, sender_timeslot, receiver_timeslot,
                 message_hash, encrypted_message, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                sender_serial, receiver_serial, sender_timeslot, receiver_timeslot,
                message_hash, encrypted_message.hex(), verified
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_communication_logs(self, limit: int = 100, 
                              sender: Optional[str] = None,
                              receiver: Optional[str] = None) -> List[Dict]:
        """
        Retrieve communication logs.
        
        Args:
            limit: Maximum number of logs to retrieve
            sender: Filter by sender serial (optional)
            receiver: Filter by receiver serial (optional)
            
        Returns:
            List of communication log dictionaries
        """
        query = """
            SELECT log_id, timestamp, sender_serial, receiver_serial,
                   sender_timeslot, receiver_timeslot, message_hash, verified
            FROM communication_logs
            WHERE 1=1
        """
        params = []
        
        if sender:
            query += " AND sender_serial = ?"
            params.append(sender)
        
        if receiver:
            query += " AND receiver_serial = ?"
            params.append(receiver)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        logs = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            for row in cursor.fetchall():
                logs.append({
                    'log_id': row['log_id'],
                    'timestamp': row['timestamp'],
                    'sender_serial': row['sender_serial'],
                    'receiver_serial': row['receiver_serial'],
                    'sender_timeslot': row['sender_timeslot'],
                    'receiver_timeslot': row['receiver_timeslot'],
                    'message_hash': row['message_hash'],
                    'verified': bool(row['verified'])
                })
        
        return logs
    
    def update_fleet_metadata(self, fleet_id: str, num_drones: int, current_timeslot: int):
        """Update fleet metadata."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fleet_metadata (fleet_id, num_drones, current_timeslot)
                VALUES (?, ?, ?)
                ON CONFLICT(fleet_id) DO UPDATE SET
                    num_drones = excluded.num_drones,
                    current_timeslot = excluded.current_timeslot,
                    last_updated = CURRENT_TIMESTAMP
            """, (fleet_id, num_drones, current_timeslot))
            conn.commit()
    
    def get_database_stats(self) -> Dict:
        """Get database statistics."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Count identities
            cursor.execute("SELECT COUNT(*) FROM identities")
            total_identities = cursor.fetchone()[0]
            
            # Count unique drones
            cursor.execute("SELECT COUNT(DISTINCT serial) FROM identities")
            unique_drones = cursor.fetchone()[0]
            
            # Count communications
            cursor.execute("SELECT COUNT(*) FROM communication_logs")
            total_communications = cursor.fetchone()[0]
            
            # Get max timeslot
            cursor.execute("SELECT MAX(timeslot) FROM identities")
            max_timeslot = cursor.fetchone()[0] or 0
            
            # Count admins
            cursor.execute("SELECT COUNT(*) FROM admins")
            total_admins = cursor.fetchone()[0]
            
            return {
                'total_identities': total_identities,
                'unique_drones': unique_drones,
                'total_communications': total_communications,
                'max_timeslot': max_timeslot,
                'total_admins': total_admins,
                'database_path': self.db_path
            }
    
    def get_total_identities(self) -> int:
        """Get total count of identities in database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM identities")
            return cursor.fetchone()[0]
    
    def get_recent_identities(self, limit: int = 100) -> List[Tuple]:
        """
        Get recent identities from database.
        
        Args:
            limit: Maximum number of identities to return
            
        Returns:
            List of tuples: (id, serial, timeslot, badge, timestamp)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, serial, timeslot, badge, timestamp
                FROM identities
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
    
    def get_recent_communications(self, limit: int = 100) -> List[Tuple]:
        """
        Get recent communications from database.
        
        Args:
            limit: Maximum number of communications to return
            
        Returns:
            List of tuples: (log_id, sender, receiver, sender_slot, receiver_slot, message, timestamp)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT log_id, sender_serial, receiver_serial, sender_timeslot, 
                       receiver_timeslot, encrypted_message, timestamp
                FROM communication_logs
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
    
    def export_to_json(self, output_file: str, timeslot: Optional[int] = None):
        """
        Export identities to JSON file.
        
        Args:
            output_file: Output JSON file path
            timeslot: Optional specific timeslot to export
        """
        if timeslot is not None:
            identities = self.get_all_identities_for_timeslot(timeslot)
        else:
            # Export all identities
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT serial, timeslot, timestamp, qrng_seed, badge FROM identities")
                identities = [
                    AgentIdentity(
                        serial=row['serial'],
                        timeslot=row['timeslot'],
                        timestamp=datetime.fromisoformat(row['timestamp']),
                        qrng_seed=bytes.fromhex(row['qrng_seed']),
                        badge=bytes.fromhex(row['badge'])
                    )
                    for row in cursor.fetchall()
                ]
        
        # Convert to dictionaries
        data = [identity.to_dict() for identity in identities]
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[✓] Exported {len(data)} identities to {output_file}")


def demo_database():
    """Demonstrate database functionality."""
    print("=== Database Manager Demo ===\n")
    
    # Create database
    db = IdentityDatabase("data/demo_identities.db")
    
    # Create admin user
    print("[*] Creating admin user...")
    if db.auth.create_admin("admin", "secure_password_123"):
        print("[✓] Admin user created successfully")
    else:
        print("[!] Admin user already exists")
    
    # Verify admin
    print("\n[*] Testing admin authentication...")
    if db.auth.verify_admin("admin", "secure_password_123"):
        print("[✓] Admin authentication successful")
    else:
        print("[✗] Admin authentication failed")
    
    # Create some test identities
    print("\n[*] Creating test identities...")
    from agent_system.drone_identity import DroneAgent
    
    test_drones = []
    for i in range(3):
        drone = DroneAgent(f"TEST-DRONE-{i+1:03d}")
        test_drones.append(drone)
    
    # Generate identities for 2 timeslots
    for timeslot in range(1, 3):
        identities = []
        for drone in test_drones:
            identity = drone.generate_identity(timeslot)
            identities.append(identity)
        
        success, failed = db.store_multiple_identities(identities)
        print(f"[✓] Timeslot {timeslot}: Stored {success} identities")
    
    # Query database
    print("\n[*] Querying database...")
    current_id = db.get_current_identity("TEST-DRONE-001")
    if current_id:
        print(f"[✓] Current identity for TEST-DRONE-001:")
        print(f"    Timeslot: {current_id.timeslot}")
        print(f"    Badge: {current_id.badge.hex()[:32]}...")
    
    # Show stats
    print("\n[*] Database statistics:")
    stats = db.get_database_stats()
    for key, value in stats.items():
        print(f"    {key}: {value}")
    
    # Export to JSON
    print("\n[*] Exporting to JSON...")
    db.export_to_json("data/demo_export.json")
    
    print("\n[✓] Database demo complete!")


if __name__ == "__main__":
    demo_database()

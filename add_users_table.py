#!/usr/bin/env python3
"""
Script to add users table to existing Medicino database.
Run this if you have an existing database and want to add authentication.
"""

import sqlite3
import os

DATABASE = 'medicino.db'

def add_users_table():
    """Add users table to existing database."""
    if not os.path.exists(DATABASE):
        print("Database not found. Please run the main application first.")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if users table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone():
        print("Users table already exists!")
        conn.close()
        return
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add user_id column to diagnosis_history if it doesn't exist
    cursor.execute("PRAGMA table_info(diagnosis_history)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'user_id' not in columns:
        cursor.execute('ALTER TABLE diagnosis_history ADD COLUMN user_id INTEGER')
        print("Added user_id column to diagnosis_history table.")
    
    conn.commit()
    conn.close()
    print("Users table created successfully!")
    print("You can now register and login to the application.")

if __name__ == '__main__':
    add_users_table() 
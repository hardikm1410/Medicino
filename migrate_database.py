#!/usr/bin/env python3
"""
Database Migration Script for Medicino
This script helps migrate from the old SQLite3 database structure to the new SQLAlchemy-based structure.
"""

import sqlite3
import os
import sys
from datetime import datetime
from app_enhanced import create_app
from models import db, User, Medicine, Condition, DiagnosisHistory

def backup_old_database():
    """Create a backup of the old database"""
    if os.path.exists('medicino.db'):
        backup_name = f'medicino_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        os.rename('medicino.db', backup_name)
        print(f"✅ Old database backed up as: {backup_name}")
        return backup_name
    return None

def migrate_users(old_conn):
    """Migrate users from old database"""
    print("🔄 Migrating users...")
    cursor = old_conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    migrated_count = 0
    for user_data in users:
        try:
            # Assuming old structure: id, username, email, password_hash, created_at
            user = User(
                username=user_data[1],
                email=user_data[2],
                password_hash=user_data[3],
                created_at=datetime.fromisoformat(user_data[4]) if user_data[4] else datetime.now()
            )
            db.session.add(user)
            migrated_count += 1
        except Exception as e:
            print(f"⚠️  Error migrating user {user_data[1]}: {e}")
    
    db.session.commit()
    print(f"✅ Migrated {migrated_count} users")

def migrate_medicines(old_conn):
    """Migrate medicines from old database"""
    print("🔄 Migrating medicines...")
    cursor = old_conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    
    migrated_count = 0
    for medicine_data in medicines:
        try:
            # Assuming old structure: id, name, description, price, category, created_at
            medicine = Medicine(
                name=medicine_data[1],
                description=medicine_data[2],
                price=float(medicine_data[3]) if medicine_data[3] else 0.0,
                category=medicine_data[4],
                created_at=datetime.fromisoformat(medicine_data[5]) if medicine_data[5] else datetime.now()
            )
            db.session.add(medicine)
            migrated_count += 1
        except Exception as e:
            print(f"⚠️  Error migrating medicine {medicine_data[1]}: {e}")
    
    db.session.commit()
    print(f"✅ Migrated {migrated_count} medicines")

def migrate_conditions(old_conn):
    """Migrate conditions from old database"""
    print("🔄 Migrating conditions...")
    cursor = old_conn.cursor()
    cursor.execute("SELECT * FROM symptoms_database")
    conditions = cursor.fetchall()
    
    migrated_count = 0
    for condition_data in conditions:
        try:
            # Assuming old structure: id, condition_name, symptoms, severity, treatment
            condition = Condition(
                name=condition_data[1],
                symptoms=condition_data[2],
                severity=condition_data[3],
                modern_treatment=condition_data[4],
                created_at=datetime.now()
            )
            db.session.add(condition)
            migrated_count += 1
        except Exception as e:
            print(f"⚠️  Error migrating condition {condition_data[1]}: {e}")
    
    db.session.commit()
    print(f"✅ Migrated {migrated_count} conditions")

def migrate_diagnosis_history(old_conn):
    """Migrate diagnosis history from old database"""
    print("🔄 Migrating diagnosis history...")
    cursor = old_conn.cursor()
    cursor.execute("SELECT * FROM diagnosis_history")
    histories = cursor.fetchall()
    
    migrated_count = 0
    for history_data in histories:
        try:
            # Assuming old structure: id, user_id, symptoms, diagnosis, confidence_score, created_at
            history = DiagnosisHistory(
                user_id=history_data[1] if history_data[1] else None,
                symptoms=history_data[2],
                diagnosis=history_data[3],
                confidence_score=float(history_data[4]) if history_data[4] else 0.0,
                created_at=datetime.fromisoformat(history_data[5]) if history_data[5] else datetime.now()
            )
            db.session.add(history)
            migrated_count += 1
        except Exception as e:
            print(f"⚠️  Error migrating diagnosis history {history_data[0]}: {e}")
    
    db.session.commit()
    print(f"✅ Migrated {migrated_count} diagnosis history records")

def run_migration():
    """Run the complete migration process"""
    print("🚀 Starting Medicino Database Migration...")
    
    # Check if old database exists
    if not os.path.exists('medicino.db'):
        print("❌ No old database found. Creating fresh database...")
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Fresh database created successfully")
        return
    
    # Create backup
    backup_file = backup_old_database()
    
    # Create new database
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ New database structure created")
        
        # Connect to old database
        try:
            old_conn = sqlite3.connect(backup_file)
            print(f"✅ Connected to backup database: {backup_file}")
            
            # Migrate data
            migrate_users(old_conn)
            migrate_medicines(old_conn)
            migrate_conditions(old_conn)
            migrate_diagnosis_history(old_conn)
            
            old_conn.close()
            print("🎉 Migration completed successfully!")
            print(f"📁 Old database backed up as: {backup_file}")
            print("💡 You can delete the backup file once you've verified the migration")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            print("🔄 Restoring old database...")
            if backup_file and os.path.exists(backup_file):
                os.rename(backup_file, 'medicino.db')
                print("✅ Old database restored")
            sys.exit(1)

def verify_migration():
    """Verify the migration was successful"""
    print("🔍 Verifying migration...")
    
    app = create_app()
    with app.app_context():
        try:
            user_count = User.query.count()
            medicine_count = Medicine.query.count()
            condition_count = Condition.query.count()
            history_count = DiagnosisHistory.query.count()
            
            print(f"✅ Users: {user_count}")
            print(f"✅ Medicines: {medicine_count}")
            print(f"✅ Conditions: {condition_count}")
            print(f"✅ Diagnosis History: {history_count}")
            
            if user_count > 0 or medicine_count > 0 or condition_count > 0:
                print("🎉 Migration verification successful!")
            else:
                print("⚠️  No data found. This might be a fresh installation.")
                
        except Exception as e:
            print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_migration()
    else:
        run_migration() 
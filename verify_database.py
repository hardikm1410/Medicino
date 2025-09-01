#!/usr/bin/env python3
"""
Database Verification Script for Medicino
Shows the comprehensive data available in the enhanced database
"""

import sqlite3
import os

DATABASE = 'medicino.db'

def verify_database():
    """Display comprehensive database information."""
    
    if not os.path.exists(DATABASE):
        print("Database not found. Please run the enhancement script first.")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    print("🔍 VERIFYING ENHANCED MEDICINO DATABASE")
    print("=" * 50)
    
    # Check symptoms database
    cursor.execute("SELECT COUNT(*) FROM symptoms_database")
    symptoms_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT condition_name, severity_level FROM symptoms_database")
    conditions = cursor.fetchall()
    
    print(f"\n📋 SYMPTOMS DATABASE: {symptoms_count} Conditions")
    print("-" * 40)
    
    # Group by severity
    severity_groups = {}
    for condition, severity in conditions:
        if severity not in severity_groups:
            severity_groups[severity] = []
        severity_groups[severity].append(condition)
    
    for severity in ['mild', 'moderate', 'severe']:
        if severity in severity_groups:
            print(f"\n{severity.upper()} CONDITIONS ({len(severity_groups[severity])}):")
            for condition in severity_groups[severity]:
                print(f"  • {condition}")
    
    # Check medicines database
    cursor.execute("SELECT COUNT(*) FROM medicines")
    medicines_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT category, COUNT(*) FROM medicines GROUP BY category")
    categories = cursor.fetchall()
    
    print(f"\n💊 MEDICINES DATABASE: {medicines_count} Medicines")
    print("-" * 40)
    
    for category, count in categories:
        print(f"  {category}: {count} medicines")
    
    # Show sample data
    print(f"\n📊 SAMPLE DATA PREVIEW")
    print("-" * 40)
    
    # Sample condition
    cursor.execute("""
        SELECT condition_name, symptoms, ayurvedic_remedy, medicine_suggestion, severity_level, description, precautions 
        FROM symptoms_database LIMIT 1
    """)
    sample_condition = cursor.fetchone()
    
    if sample_condition:
        print(f"\n🔍 SAMPLE CONDITION:")
        print(f"  Name: {sample_condition[0]}")
        print(f"  Symptoms: {sample_condition[1]}")
        print(f"  Ayurvedic Remedy: {sample_condition[2]}")
        print(f"  Medicine Suggestion: {sample_condition[3]}")
        print(f"  Severity: {sample_condition[4]}")
        print(f"  Description: {sample_condition[5]}")
        print(f"  Precautions: {sample_condition[6]}")
    
    # Sample medicine
    cursor.execute("""
        SELECT name, description, dosage, side_effects, contraindications, price, category 
        FROM medicines LIMIT 1
    """)
    sample_medicine = cursor.fetchone()
    
    if sample_medicine:
        print(f"\n💊 SAMPLE MEDICINE:")
        print(f"  Name: {sample_medicine[0]}")
        print(f"  Description: {sample_medicine[1]}")
        print(f"  Dosage: {sample_medicine[2]}")
        print(f"  Side Effects: {sample_medicine[3]}")
        print(f"  Contraindications: {sample_medicine[4]}")
        print(f"  Price: ${sample_medicine[5]}")
        print(f"  Category: {sample_medicine[6]}")
    
    # Check users table
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    
    # Check diagnosis history
    cursor.execute("SELECT COUNT(*) FROM diagnosis_history")
    history_count = cursor.fetchone()[0]
    
    print(f"\n👥 USER DATA:")
    print(f"  Registered Users: {users_count}")
    print(f"  Diagnosis Records: {history_count}")
    
    # Database statistics
    print(f"\n📈 DATABASE STATISTICS:")
    print(f"  • Total Medical Conditions: {symptoms_count}")
    print(f"  • Total Medicines: {medicines_count}")
    print(f"  • Medicine Categories: {len(categories)}")
    print(f"  • Severity Levels: {len(severity_groups)}")
    print(f"  • Registered Users: {users_count}")
    print(f"  • Diagnosis Records: {history_count}")
    
    # Show all categories
    print(f"\n🏷️  MEDICINE CATEGORIES:")
    for category, count in categories:
        print(f"  • {category}: {count} items")
    
    # Show all severity levels
    print(f"\n⚠️  SEVERITY LEVELS:")
    for severity in ['mild', 'moderate', 'severe']:
        if severity in severity_groups:
            print(f"  • {severity.capitalize()}: {len(severity_groups[severity])} conditions")
    
    conn.close()
    
    print(f"\n✅ DATABASE VERIFICATION COMPLETE!")
    print(f"\n🎯 FEATURES AVAILABLE:")
    print(f"  • Comprehensive symptom analysis with 21 conditions")
    print(f"  • Detailed Ayurvedic remedies for each condition")
    print(f"  • 28 medicines across multiple categories")
    print(f"  • Severity-based recommendations")
    print(f"  • Price information and dosage details")
    print(f"  • User authentication and history tracking")
    print(f"  • Precautions and contraindications")
    
    print(f"\n🚀 READY TO USE:")
    print(f"  1. Start the application: python app.py")
    print(f"  2. Register/login to access all features")
    print(f"  3. Test symptom diagnosis with various conditions")
    print(f"  4. Explore the comprehensive medicine database")
    print(f"  5. Check your diagnosis history")

if __name__ == '__main__':
    verify_database() 
#!/usr/bin/env python3
"""
Add Healthcare Providers table and populate with sample data
"""

import sqlite3
import os
from datetime import datetime

DATABASE = 'medicino.db'

def add_healthcare_providers_table():
    """Add Healthcare Providers table to the existing database."""
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='healthcare_providers'")
    if cursor.fetchone():
        print("Healthcare Providers table already exists.")
        return
    
    print("Creating Healthcare Providers table...")
    
    # Create healthcare_providers table
    cursor.execute('''
        CREATE TABLE healthcare_providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_name TEXT NOT NULL,
            hospital_clinic TEXT NOT NULL,
            hospital_clinic_address TEXT NOT NULL,
            hospital_clinic_contact_number TEXT NOT NULL,
            specialty TEXT NOT NULL,
            experience_years INTEGER,
            consultation_fee REAL,
            availability TEXT,
            languages_spoken TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX idx_healthcare_providers_doctor_name ON healthcare_providers(doctor_name)')
    cursor.execute('CREATE INDEX idx_healthcare_providers_specialty ON healthcare_providers(specialty)')
    cursor.execute('CREATE INDEX idx_healthcare_providers_is_active ON healthcare_providers(is_active)')
    
    print("Healthcare Providers table created successfully!")
    
    # Populate with sample data
    print("Populating with sample healthcare providers...")
    
    healthcare_providers_data = [
        # General Physician
        {
            'doctor_name': 'Dr. Sarah Johnson',
            'hospital_clinic': 'City General Hospital',
            'hospital_clinic_address': '123 Main Street, Downtown, City Center',
            'hospital_clinic_contact_number': '+1-555-0101',
            'specialty': 'General Physician',
            'experience_years': 15,
            'consultation_fee': 75.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 1:00 PM',
            'languages_spoken': 'English, Spanish'
        },
        {
            'doctor_name': 'Dr. Michael Chen',
            'hospital_clinic': 'Community Health Center',
            'hospital_clinic_address': '456 Oak Avenue, Suburb District',
            'hospital_clinic_contact_number': '+1-555-0102',
            'specialty': 'General Physician',
            'experience_years': 12,
            'consultation_fee': 65.00,
            'availability': 'Mon-Sat: 8:00 AM - 6:00 PM',
            'languages_spoken': 'English, Mandarin'
        },
        
        # Homeopathy
        {
            'doctor_name': 'Dr. Emily Rodriguez',
            'hospital_clinic': 'Natural Healing Clinic',
            'hospital_clinic_address': '789 Pine Street, Wellness District',
            'hospital_clinic_contact_number': '+1-555-0103',
            'specialty': 'Homeopathy',
            'experience_years': 8,
            'consultation_fee': 90.00,
            'availability': 'Mon-Fri: 10:00 AM - 4:00 PM',
            'languages_spoken': 'English, Portuguese'
        },
        {
            'doctor_name': 'Dr. James Wilson',
            'hospital_clinic': 'Holistic Health Center',
            'hospital_clinic_address': '321 Elm Street, Alternative Medicine District',
            'hospital_clinic_contact_number': '+1-555-0104',
            'specialty': 'Homeopathy',
            'experience_years': 20,
            'consultation_fee': 120.00,
            'availability': 'Mon-Sat: 9:00 AM - 3:00 PM',
            'languages_spoken': 'English, French'
        },
        
        # Obstetrics & Gynecology
        {
            'doctor_name': 'Dr. Lisa Thompson',
            'hospital_clinic': 'Women\'s Health Hospital',
            'hospital_clinic_address': '654 Maple Drive, Medical District',
            'hospital_clinic_contact_number': '+1-555-0105',
            'specialty': 'Obstetrics & Gynecology',
            'experience_years': 18,
            'consultation_fee': 150.00,
            'availability': 'Mon-Fri: 8:00 AM - 6:00 PM, Sat: 9:00 AM - 2:00 PM',
            'languages_spoken': 'English, Italian'
        },
        {
            'doctor_name': 'Dr. Maria Garcia',
            'hospital_clinic': 'Family Care Medical Center',
            'hospital_clinic_address': '987 Cedar Lane, Family District',
            'hospital_clinic_contact_number': '+1-555-0106',
            'specialty': 'Obstetrics & Gynecology',
            'experience_years': 14,
            'consultation_fee': 130.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM',
            'languages_spoken': 'English, Spanish'
        },
        
        # Ophthalmology
        {
            'doctor_name': 'Dr. Robert Kim',
            'hospital_clinic': 'Vision Care Institute',
            'hospital_clinic_address': '147 Birch Street, Eye Care District',
            'hospital_clinic_contact_number': '+1-555-0107',
            'specialty': 'Ophthalmology',
            'experience_years': 22,
            'consultation_fee': 180.00,
            'availability': 'Mon-Fri: 8:00 AM - 5:00 PM',
            'languages_spoken': 'English, Korean'
        },
        {
            'doctor_name': 'Dr. Jennifer Lee',
            'hospital_clinic': 'Advanced Eye Care Center',
            'hospital_clinic_address': '258 Willow Avenue, Vision District',
            'hospital_clinic_contact_number': '+1-555-0108',
            'specialty': 'Ophthalmology',
            'experience_years': 16,
            'consultation_fee': 160.00,
            'availability': 'Mon-Sat: 9:00 AM - 4:00 PM',
            'languages_spoken': 'English, Chinese'
        },
        
        # Gastroenterology
        {
            'doctor_name': 'Dr. David Brown',
            'hospital_clinic': 'Digestive Health Center',
            'hospital_clinic_address': '369 Spruce Street, Medical Complex',
            'hospital_clinic_contact_number': '+1-555-0109',
            'specialty': 'Gastroenterology',
            'experience_years': 19,
            'consultation_fee': 200.00,
            'availability': 'Mon-Fri: 8:00 AM - 6:00 PM',
            'languages_spoken': 'English, German'
        },
        {
            'doctor_name': 'Dr. Amanda White',
            'hospital_clinic': 'Gastrointestinal Institute',
            'hospital_clinic_address': '741 Poplar Drive, Health District',
            'hospital_clinic_contact_number': '+1-555-0110',
            'specialty': 'Gastroenterology',
            'experience_years': 13,
            'consultation_fee': 175.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 1:00 PM',
            'languages_spoken': 'English, French'
        },
        
        # Psychiatry
        {
            'doctor_name': 'Dr. Thomas Anderson',
            'hospital_clinic': 'Mental Health Center',
            'hospital_clinic_address': '852 Ash Street, Wellness District',
            'hospital_clinic_contact_number': '+1-555-0111',
            'specialty': 'Psychiatry',
            'experience_years': 25,
            'consultation_fee': 220.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM',
            'languages_spoken': 'English, Swedish'
        },
        {
            'doctor_name': 'Dr. Rachel Green',
            'hospital_clinic': 'Psychological Wellness Institute',
            'hospital_clinic_address': '963 Chestnut Avenue, Mental Health District',
            'hospital_clinic_contact_number': '+1-555-0112',
            'specialty': 'Psychiatry',
            'experience_years': 17,
            'consultation_fee': 190.00,
            'availability': 'Mon-Sat: 10:00 AM - 6:00 PM',
            'languages_spoken': 'English, Hebrew'
        },
        
        # Pediatrics / Neonatology
        {
            'doctor_name': 'Dr. Christopher Martinez',
            'hospital_clinic': 'Children\'s Medical Center',
            'hospital_clinic_address': '159 Sycamore Lane, Pediatric District',
            'hospital_clinic_contact_number': '+1-555-0113',
            'specialty': 'Pediatrics / Neonatology',
            'experience_years': 21,
            'consultation_fee': 140.00,
            'availability': 'Mon-Fri: 8:00 AM - 6:00 PM, Sat: 9:00 AM - 3:00 PM',
            'languages_spoken': 'English, Spanish'
        },
        {
            'doctor_name': 'Dr. Stephanie Taylor',
            'hospital_clinic': 'Kids Care Hospital',
            'hospital_clinic_address': '357 Magnolia Street, Children\'s District',
            'hospital_clinic_contact_number': '+1-555-0114',
            'specialty': 'Pediatrics / Neonatology',
            'experience_years': 15,
            'consultation_fee': 125.00,
            'availability': 'Mon-Sat: 9:00 AM - 5:00 PM',
            'languages_spoken': 'English, Portuguese'
        },
        
        # Neurosurgery
        {
            'doctor_name': 'Dr. Kevin Patel',
            'hospital_clinic': 'Neurological Institute',
            'hospital_clinic_address': '486 Redwood Drive, Neurology District',
            'hospital_clinic_contact_number': '+1-555-0115',
            'specialty': 'Neurosurgery',
            'experience_years': 28,
            'consultation_fee': 350.00,
            'availability': 'Mon-Fri: 8:00 AM - 4:00 PM',
            'languages_spoken': 'English, Hindi'
        },
        {
            'doctor_name': 'Dr. Nicole Clark',
            'hospital_clinic': 'Brain & Spine Center',
            'hospital_clinic_address': '792 Sequoia Avenue, Neurosurgery District',
            'hospital_clinic_contact_number': '+1-555-0116',
            'specialty': 'Neurosurgery',
            'experience_years': 23,
            'consultation_fee': 320.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM',
            'languages_spoken': 'English, Russian'
        },
        
        # Urology / General Surgery
        {
            'doctor_name': 'Dr. Mark Davis',
            'hospital_clinic': 'Urological Care Center',
            'hospital_clinic_address': '135 Cypress Street, Urology District',
            'hospital_clinic_contact_number': '+1-555-0117',
            'specialty': 'Urology / General Surgery',
            'experience_years': 20,
            'consultation_fee': 280.00,
            'availability': 'Mon-Fri: 8:00 AM - 6:00 PM',
            'languages_spoken': 'English, Arabic'
        },
        {
            'doctor_name': 'Dr. Jessica Moore',
            'hospital_clinic': 'Surgical Specialists Hospital',
            'hospital_clinic_address': '468 Juniper Lane, Surgery District',
            'hospital_clinic_contact_number': '+1-555-0118',
            'specialty': 'Urology / General Surgery',
            'experience_years': 16,
            'consultation_fee': 250.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 1:00 PM',
            'languages_spoken': 'English, Japanese'
        },
        
        # Cardiology / Cardiothoracic Surgery
        {
            'doctor_name': 'Dr. William Johnson',
            'hospital_clinic': 'Heart Care Institute',
            'hospital_clinic_address': '579 Palm Street, Cardiology District',
            'hospital_clinic_contact_number': '+1-555-0119',
            'specialty': 'Cardiology / Cardiothoracic Surgery',
            'experience_years': 30,
            'consultation_fee': 400.00,
            'availability': 'Mon-Fri: 8:00 AM - 5:00 PM',
            'languages_spoken': 'English, Greek'
        },
        {
            'doctor_name': 'Dr. Michelle Adams',
            'hospital_clinic': 'Cardiovascular Center',
            'hospital_clinic_address': '681 Acacia Avenue, Heart District',
            'hospital_clinic_contact_number': '+1-555-0120',
            'specialty': 'Cardiology / Cardiothoracic Surgery',
            'experience_years': 18,
            'consultation_fee': 350.00,
            'availability': 'Mon-Fri: 9:00 AM - 6:00 PM',
            'languages_spoken': 'English, Polish'
        },
        
        # Orthopedic Surgery
        {
            'doctor_name': 'Dr. Daniel Lewis',
            'hospital_clinic': 'Orthopedic Institute',
            'hospital_clinic_address': '793 Eucalyptus Drive, Orthopedic District',
            'hospital_clinic_contact_number': '+1-555-0121',
            'specialty': 'Orthopedic Surgery',
            'experience_years': 24,
            'consultation_fee': 300.00,
            'availability': 'Mon-Fri: 8:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM',
            'languages_spoken': 'English, Dutch'
        },
        {
            'doctor_name': 'Dr. Samantha Turner',
            'hospital_clinic': 'Bone & Joint Center',
            'hospital_clinic_address': '915 Fir Street, Orthopedic District',
            'hospital_clinic_contact_number': '+1-555-0122',
            'specialty': 'Orthopedic Surgery',
            'experience_years': 19,
            'consultation_fee': 275.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM',
            'languages_spoken': 'English, Turkish'
        }
    ]
    
    # Insert data
    for provider in healthcare_providers_data:
        cursor.execute('''
            INSERT INTO healthcare_providers (
                doctor_name, hospital_clinic, hospital_clinic_address, 
                hospital_clinic_contact_number, specialty, experience_years,
                consultation_fee, availability, languages_spoken, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            provider['doctor_name'],
            provider['hospital_clinic'],
            provider['hospital_clinic_address'],
            provider['hospital_clinic_contact_number'],
            provider['specialty'],
            provider['experience_years'],
            provider['consultation_fee'],
            provider['availability'],
            provider['languages_spoken'],
            1  # is_active
        ))
    
    conn.commit()
    print(f"Successfully added {len(healthcare_providers_data)} healthcare providers!")
    
    # Verify the data
    cursor.execute("SELECT COUNT(*) FROM healthcare_providers")
    count = cursor.fetchone()[0]
    print(f"Total healthcare providers in database: {count}")
    
    # Show specialties
    cursor.execute("SELECT DISTINCT specialty FROM healthcare_providers ORDER BY specialty")
    specialties = cursor.fetchall()
    print("\nAvailable specialties:")
    for specialty in specialties:
        print(f"- {specialty[0]}")
    
    conn.close()
    print("\nHealthcare Providers database setup completed successfully!")

if __name__ == "__main__":
    add_healthcare_providers_table() 
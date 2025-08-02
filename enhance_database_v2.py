#!/usr/bin/env python3
"""
Enhanced Database Setup for Medicino v2.0
This script creates a comprehensive medical database with:
- Enhanced symptoms and conditions with better medicine mappings
- Comprehensive medicine database with detailed information
- Better synchronization between symptoms and medicines
- Additional healthcare data
"""

import sqlite3
import os
from datetime import datetime

DATABASE = 'medicino.db'

def create_enhanced_database():
    """Create and populate the enhanced database with comprehensive medical data."""
    
    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("Removed existing database.")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating enhanced database tables...")
    
    # Users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            date_of_birth DATE,
            gender TEXT,
            is_active BOOLEAN DEFAULT 1,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Enhanced Medicines table
    cursor.execute('''
        CREATE TABLE medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            generic_name TEXT,
            description TEXT,
            dosage TEXT,
            side_effects TEXT,
            contraindications TEXT,
            price REAL,
            category TEXT,
            prescription_required BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Enhanced Symptoms database table
    cursor.execute('''
        CREATE TABLE symptoms_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            severity_level TEXT,
            description TEXT,
            precautions TEXT,
            category TEXT,
            body_system TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medicine-Symptom mapping table for better synchronization
    cursor.execute('''
        CREATE TABLE medicine_symptom_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            symptom_id INTEGER,
            effectiveness_score REAL DEFAULT 0.8,
            usage_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medicine_id) REFERENCES medicines (id),
            FOREIGN KEY (symptom_id) REFERENCES symptoms_database (id)
        )
    ''')
    
    # Diagnosis history table
    cursor.execute('''
        CREATE TABLE diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symptoms TEXT NOT NULL,
            diagnosed_condition TEXT,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            confidence_score REAL,
            severity_level TEXT,
            user_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Healthcare Providers table
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
    cursor.execute('CREATE INDEX idx_medicines_name ON medicines(name)')
    cursor.execute('CREATE INDEX idx_medicines_category ON medicines(category)')
    cursor.execute('CREATE INDEX idx_symptoms_condition ON symptoms_database(condition_name)')
    cursor.execute('CREATE INDEX idx_symptoms_category ON symptoms_database(category)')
    cursor.execute('CREATE INDEX idx_symptoms_body_system ON symptoms_database(body_system)')
    cursor.execute('CREATE INDEX idx_mapping_medicine ON medicine_symptom_mapping(medicine_id)')
    cursor.execute('CREATE INDEX idx_mapping_symptom ON medicine_symptom_mapping(symptom_id)')
    cursor.execute('CREATE INDEX idx_providers_specialty ON healthcare_providers(specialty)')
    
    print("Enhanced tables created successfully!")
    
    # Populate enhanced symptoms database
    print("Populating enhanced symptoms database...")
    
    enhanced_symptoms_data = [
        # Respiratory System
        {
            'condition_name': 'Common Cold',
            'symptoms': 'runny nose, sneezing, sore throat, cough, congestion, mild fever, fatigue, headache',
            'ayurvedic_remedy': 'Tulsi tea, ginger tea, honey with warm water, steam inhalation with eucalyptus oil, turmeric milk',
            'medicine_suggestion': 'Paracetamol, Vitamin C, Decongestants, Cough Syrup, Zinc Supplements',
            'severity_level': 'mild',
            'description': 'A viral infection affecting the upper respiratory tract',
            'precautions': 'Rest, stay hydrated, avoid cold foods, maintain good hygiene, avoid smoking',
            'category': 'Respiratory',
            'body_system': 'Respiratory'
        },
        {
            'condition_name': 'Influenza (Flu)',
            'symptoms': 'high fever, body aches, fatigue, headache, cough, sore throat, chills, weakness',
            'ayurvedic_remedy': 'Ginger-turmeric tea, honey-lemon water, rest, warm soups, steam therapy',
            'medicine_suggestion': 'Oseltamivir, Paracetamol, Ibuprofen, Decongestants, Rest',
            'severity_level': 'moderate',
            'description': 'Viral infection with more severe symptoms than common cold',
            'precautions': 'Rest, hydration, isolation, avoid contact with others, seek medical attention if severe',
            'category': 'Respiratory',
            'body_system': 'Respiratory'
        },
        {
            'condition_name': 'Bronchitis',
            'symptoms': 'persistent cough, chest discomfort, fatigue, mild fever, shortness of breath, wheezing',
            'ayurvedic_remedy': 'Tulsi-ginger tea, honey, steam inhalation, rest, warm fluids',
            'medicine_suggestion': 'Bronchodilators, Cough Suppressants, Antibiotics (if bacterial), Expectorants',
            'severity_level': 'moderate',
            'description': 'Inflammation of the bronchial tubes',
            'precautions': 'Rest, avoid smoking, stay hydrated, use humidifier, avoid cold air',
            'category': 'Respiratory',
            'body_system': 'Respiratory'
        },
        
        # Cardiovascular System
        {
            'condition_name': 'Hypertension (High Blood Pressure)',
            'symptoms': 'headache, dizziness, chest pain, shortness of breath, vision problems, fatigue',
            'ayurvedic_remedy': 'Garlic, Arjuna bark, Sarpagandha, meditation, yoga, reduced salt intake',
            'medicine_suggestion': 'ACE Inhibitors, Beta Blockers, Calcium Channel Blockers, Diuretics, Lifestyle Changes',
            'severity_level': 'serious',
            'description': 'Persistently elevated blood pressure',
            'precautions': 'Regular monitoring, low-salt diet, exercise, stress management, avoid smoking',
            'category': 'Cardiovascular',
            'body_system': 'Cardiovascular'
        },
        {
            'condition_name': 'Angina',
            'symptoms': 'chest pain, pressure, tightness, shortness of breath, pain in arms/shoulders/neck',
            'ayurvedic_remedy': 'Arjuna bark, Guggulu, garlic, meditation, stress reduction',
            'medicine_suggestion': 'Nitroglycerin, Beta Blockers, Calcium Channel Blockers, Aspirin, Statins',
            'severity_level': 'serious',
            'description': 'Chest pain due to reduced blood flow to heart',
            'precautions': 'Immediate medical attention, avoid strenuous activity, stress management',
            'category': 'Cardiovascular',
            'body_system': 'Cardiovascular'
        },
        
        # Digestive System
        {
            'condition_name': 'Gastritis',
            'symptoms': 'stomach pain, nausea, vomiting, bloating, loss of appetite, heartburn',
            'ayurvedic_remedy': 'Aloe vera juice, ginger tea, licorice, fennel seeds, coconut water',
            'medicine_suggestion': 'Antacids, H2 Blockers, Proton Pump Inhibitors, Anti-nausea Medication',
            'severity_level': 'moderate',
            'description': 'Inflammation of the stomach lining',
            'precautions': 'Avoid spicy foods, eat smaller meals, avoid alcohol, stress management',
            'category': 'Digestive',
            'body_system': 'Digestive'
        },
        {
            'condition_name': 'Irritable Bowel Syndrome (IBS)',
            'symptoms': 'abdominal pain, bloating, diarrhea, constipation, gas, mucus in stool',
            'ayurvedic_remedy': 'Triphala, ginger, peppermint tea, probiotics, stress management',
            'medicine_suggestion': 'Antispasmodics, Fiber Supplements, Probiotics, Anti-diarrheal, Laxatives',
            'severity_level': 'moderate',
            'description': 'Chronic disorder affecting the large intestine',
            'precautions': 'Diet modification, stress management, regular exercise, food diary',
            'category': 'Digestive',
            'body_system': 'Digestive'
        },
        
        # Nervous System
        {
            'condition_name': 'Migraine',
            'symptoms': 'severe headache, nausea, vomiting, sensitivity to light/sound, aura, dizziness',
            'ayurvedic_remedy': 'Brahmi, Shankhpushpi, ginger tea, cold compress, dark room rest',
            'medicine_suggestion': 'Triptans, NSAIDs, Anti-nausea Medication, Preventive Medications',
            'severity_level': 'moderate',
            'description': 'Recurrent severe headaches with neurological symptoms',
            'precautions': 'Identify triggers, stress management, regular sleep, avoid certain foods',
            'category': 'Neurological',
            'body_system': 'Nervous'
        },
        {
            'condition_name': 'Anxiety Disorder',
            'symptoms': 'excessive worry, restlessness, fatigue, difficulty concentrating, irritability, sleep problems',
            'ayurvedic_remedy': 'Brahmi, Ashwagandha, Jatamansi, meditation, yoga, breathing exercises',
            'medicine_suggestion': 'SSRIs, Benzodiazepines, Buspirone, Beta Blockers, Therapy',
            'severity_level': 'moderate',
            'description': 'Mental health disorder characterized by excessive anxiety',
            'precautions': 'Therapy, stress management, regular exercise, avoid caffeine, support groups',
            'category': 'Mental Health',
            'body_system': 'Nervous'
        },
        
        # Musculoskeletal System
        {
            'condition_name': 'Osteoarthritis',
            'symptoms': 'joint pain, stiffness, swelling, reduced range of motion, grating sensation',
            'ayurvedic_remedy': 'Guggulu, Shallaki, ginger, turmeric, warm oil massage, exercise',
            'medicine_suggestion': 'NSAIDs, Acetaminophen, Glucosamine, Physical Therapy, Joint Supplements',
            'severity_level': 'moderate',
            'description': 'Degenerative joint disease causing cartilage breakdown',
            'precautions': 'Weight management, low-impact exercise, joint protection, proper posture',
            'category': 'Musculoskeletal',
            'body_system': 'Musculoskeletal'
        },
        {
            'condition_name': 'Back Pain',
            'symptoms': 'lower back pain, stiffness, muscle spasms, pain radiating to legs, difficulty moving',
            'ayurvedic_remedy': 'Ksheerabala oil massage, ginger, turmeric, warm compress, yoga',
            'medicine_suggestion': 'NSAIDs, Muscle Relaxants, Physical Therapy, Heat/Cold Therapy',
            'severity_level': 'moderate',
            'description': 'Pain in the lower back region',
            'precautions': 'Proper lifting, good posture, core strengthening, avoid prolonged sitting',
            'category': 'Musculoskeletal',
            'body_system': 'Musculoskeletal'
        },
        
        # Endocrine System
        {
            'condition_name': 'Diabetes Type 2',
            'symptoms': 'increased thirst, frequent urination, increased hunger, weight loss, fatigue, blurred vision',
            'ayurvedic_remedy': 'Gurmar, Neem, Jamun seeds, bitter gourd, fenugreek, exercise',
            'medicine_suggestion': 'Metformin, Sulfonylureas, DPP-4 Inhibitors, Insulin, Blood Sugar Monitoring',
            'severity_level': 'serious',
            'description': 'Metabolic disorder affecting blood sugar regulation',
            'precautions': 'Diet control, regular exercise, blood sugar monitoring, foot care',
            'category': 'Endocrine',
            'body_system': 'Endocrine'
        },
        {
            'condition_name': 'Hypothyroidism',
            'symptoms': 'fatigue, weight gain, cold sensitivity, dry skin, hair loss, depression',
            'ayurvedic_remedy': 'Kanchanara, Guggulu, Ashwagandha, iodine-rich foods, exercise',
            'medicine_suggestion': 'Levothyroxine, Thyroid Hormone Replacement, Regular Monitoring',
            'severity_level': 'moderate',
            'description': 'Underactive thyroid gland',
            'precautions': 'Regular medication, thyroid monitoring, balanced diet, stress management',
            'category': 'Endocrine',
            'body_system': 'Endocrine'
        },
        
        # Skin Conditions
        {
            'condition_name': 'Eczema',
            'symptoms': 'dry, itchy skin, red patches, inflammation, scaling, oozing, thickened skin',
            'ayurvedic_remedy': 'Neem, turmeric, coconut oil, aloe vera, oatmeal baths, stress management',
            'medicine_suggestion': 'Topical Corticosteroids, Moisturizers, Antihistamines, Immunosuppressants',
            'severity_level': 'moderate',
            'description': 'Chronic inflammatory skin condition',
            'precautions': 'Moisturize regularly, avoid triggers, gentle skin care, stress management',
            'category': 'Dermatological',
            'body_system': 'Integumentary'
        },
        {
            'condition_name': 'Acne',
            'symptoms': 'pimples, blackheads, whiteheads, inflammation, scarring, oily skin',
            'ayurvedic_remedy': 'Neem, turmeric, aloe vera, tea tree oil, proper diet, stress management',
            'medicine_suggestion': 'Benzoyl Peroxide, Salicylic Acid, Retinoids, Antibiotics, Hormonal Therapy',
            'severity_level': 'mild',
            'description': 'Skin condition affecting hair follicles and oil glands',
            'precautions': 'Gentle cleansing, avoid picking, proper diet, stress management',
            'category': 'Dermatological',
            'body_system': 'Integumentary'
        },
        
        # Eye Conditions
        {
            'condition_name': 'Conjunctivitis',
            'symptoms': 'red eyes, itching, burning, discharge, swollen eyelids, light sensitivity',
            'ayurvedic_remedy': 'Rose water, honey, aloe vera, cold compress, proper hygiene',
            'medicine_suggestion': 'Antibiotic Eye Drops, Antihistamine Drops, Artificial Tears, Warm Compress',
            'severity_level': 'mild',
            'description': 'Inflammation of the conjunctiva (eye membrane)',
            'precautions': 'Good hygiene, avoid touching eyes, separate towels, avoid contact lenses',
            'category': 'Ophthalmological',
            'body_system': 'Sensory'
        },
        
        # Women's Health
        {
            'condition_name': 'Dysmenorrhea',
            'symptoms': 'menstrual cramps, lower abdominal pain, back pain, nausea, fatigue, headache',
            'ayurvedic_remedy': 'Ginger tea, cinnamon, fennel seeds, warm compress, yoga, meditation',
            'medicine_suggestion': 'NSAIDs, Birth Control Pills, Heat Therapy, Pain Relievers',
            'severity_level': 'moderate',
            'description': 'Painful menstrual periods',
            'precautions': 'Regular exercise, stress management, proper diet, heat therapy',
            'category': 'Women\'s Health',
            'body_system': 'Reproductive'
        },
        
        # Men's Health
        {
            'condition_name': 'Benign Prostatic Hyperplasia (BPH)',
            'symptoms': 'frequent urination, weak urine stream, difficulty starting urination, incomplete emptying',
            'ayurvedic_remedy': 'Saw palmetto, pumpkin seeds, zinc, exercise, stress management',
            'medicine_suggestion': 'Alpha Blockers, 5-Alpha Reductase Inhibitors, Surgery if needed',
            'severity_level': 'moderate',
            'description': 'Enlarged prostate gland',
            'precautions': 'Regular checkups, limit caffeine, avoid alcohol, exercise',
            'category': 'Men\'s Health',
            'body_system': 'Reproductive'
        }
    ]
    
    # Insert symptoms data
    cursor.executemany('''
        INSERT INTO symptoms_database (
            condition_name, symptoms, ayurvedic_remedy, medicine_suggestion, 
            severity_level, description, precautions, category, body_system
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(item['condition_name'], item['symptoms'], item['ayurvedic_remedy'],
           item['medicine_suggestion'], item['severity_level'], item['description'],
           item['precautions'], item['category'], item['body_system']) 
          for item in enhanced_symptoms_data])
    
    print(f"Added {len(enhanced_symptoms_data)} enhanced conditions to symptoms database")
    
    # Populate enhanced medicines database
    print("Populating enhanced medicines database...")
    
    enhanced_medicines_data = [
        # Pain Relief & Fever
        {
            'name': 'Paracetamol (Acetaminophen)',
            'generic_name': 'Acetaminophen',
            'description': 'Pain reliever and fever reducer',
            'dosage': '500-1000mg every 4-6 hours, max 4000mg/day',
            'side_effects': 'Nausea, liver damage (high doses), allergic reactions',
            'contraindications': 'Liver disease, alcohol abuse, pregnancy (consult doctor)',
            'price': 5.99,
            'category': 'Pain Relief',
            'prescription_required': False
        },
        {
            'name': 'Ibuprofen',
            'generic_name': 'Ibuprofen',
            'description': 'Non-steroidal anti-inflammatory drug for pain and inflammation',
            'dosage': '200-400mg every 4-6 hours, max 1200mg/day',
            'side_effects': 'Stomach upset, ulcers, kidney problems, allergic reactions',
            'contraindications': 'Stomach ulcers, kidney disease, pregnancy (3rd trimester)',
            'price': 7.99,
            'category': 'Pain Relief',
            'prescription_required': False
        },
        {
            'name': 'Aspirin',
            'generic_name': 'Acetylsalicylic Acid',
            'description': 'Pain reliever, fever reducer, and blood thinner',
            'dosage': '325-650mg every 4-6 hours',
            'side_effects': 'Stomach irritation, bleeding, allergic reactions',
            'contraindications': 'Bleeding disorders, stomach ulcers, children under 12',
            'price': 4.99,
            'category': 'Pain Relief',
            'prescription_required': False
        },
        
        # Respiratory Medications
        {
            'name': 'Pseudoephedrine',
            'generic_name': 'Pseudoephedrine',
            'description': 'Decongestant for nasal congestion',
            'dosage': '30-60mg every 4-6 hours',
            'side_effects': 'Increased heart rate, insomnia, nervousness',
            'contraindications': 'High blood pressure, heart disease, thyroid problems',
            'price': 8.99,
            'category': 'Respiratory',
            'prescription_required': False
        },
        {
            'name': 'Dextromethorphan',
            'generic_name': 'Dextromethorphan',
            'description': 'Cough suppressant',
            'dosage': '15-30mg every 4-8 hours',
            'side_effects': 'Drowsiness, dizziness, nausea',
            'contraindications': 'MAOI use, respiratory depression',
            'price': 6.99,
            'category': 'Respiratory',
            'prescription_required': False
        },
        {
            'name': 'Guaifenesin',
            'generic_name': 'Guaifenesin',
            'description': 'Expectorant to loosen mucus',
            'dosage': '200-400mg every 4 hours',
            'side_effects': 'Nausea, vomiting, headache',
            'contraindications': 'None significant',
            'price': 5.99,
            'category': 'Respiratory',
            'prescription_required': False
        },
        
        # Digestive Health
        {
            'name': 'Omeprazole',
            'generic_name': 'Omeprazole',
            'description': 'Proton pump inhibitor for acid reflux',
            'dosage': '20-40mg daily',
            'side_effects': 'Headache, diarrhea, stomach pain',
            'contraindications': 'Pregnancy, liver disease',
            'price': 15.99,
            'category': 'Digestive',
            'prescription_required': True
        },
        {
            'name': 'Ranitidine',
            'generic_name': 'Ranitidine',
            'description': 'H2 blocker for acid reflux',
            'dosage': '150mg twice daily',
            'side_effects': 'Headache, constipation, diarrhea',
            'contraindications': 'Kidney disease, pregnancy',
            'price': 12.99,
            'category': 'Digestive',
            'prescription_required': False
        },
        {
            'name': 'Loperamide',
            'generic_name': 'Loperamide',
            'description': 'Anti-diarrheal medication',
            'dosage': '2-4mg initially, then 2mg after each loose stool',
            'side_effects': 'Constipation, stomach pain, drowsiness',
            'contraindications': 'Bacterial diarrhea, inflammatory bowel disease',
            'price': 8.99,
            'category': 'Digestive',
            'prescription_required': False
        },
        
        # Cardiovascular
        {
            'name': 'Amlodipine',
            'generic_name': 'Amlodipine',
            'description': 'Calcium channel blocker for high blood pressure',
            'dosage': '5-10mg daily',
            'side_effects': 'Swelling, dizziness, headache',
            'contraindications': 'Severe aortic stenosis, pregnancy',
            'price': 18.99,
            'category': 'Cardiovascular',
            'prescription_required': True
        },
        {
            'name': 'Lisinopril',
            'generic_name': 'Lisinopril',
            'description': 'ACE inhibitor for high blood pressure',
            'dosage': '10-40mg daily',
            'side_effects': 'Dry cough, dizziness, fatigue',
            'contraindications': 'Pregnancy, angioedema history',
            'price': 16.99,
            'category': 'Cardiovascular',
            'prescription_required': True
        },
        
        # Mental Health
        {
            'name': 'Sertraline',
            'generic_name': 'Sertraline',
            'description': 'SSRI antidepressant',
            'dosage': '50-200mg daily',
            'side_effects': 'Nausea, insomnia, sexual dysfunction',
            'contraindications': 'MAOI use, pregnancy',
            'price': 25.99,
            'category': 'Mental Health',
            'prescription_required': True
        },
        {
            'name': 'Alprazolam',
            'generic_name': 'Alprazolam',
            'description': 'Benzodiazepine for anxiety',
            'dosage': '0.25-0.5mg three times daily',
            'side_effects': 'Drowsiness, dependence, memory problems',
            'contraindications': 'Pregnancy, respiratory depression',
            'price': 22.99,
            'category': 'Mental Health',
            'prescription_required': True
        },
        
        # Supplements
        {
            'name': 'Vitamin D3',
            'generic_name': 'Cholecalciferol',
            'description': 'Vitamin D supplement for bone health',
            'dosage': '1000-4000 IU daily',
            'side_effects': 'Nausea, kidney stones (high doses)',
            'contraindications': 'Hypercalcemia, kidney disease',
            'price': 9.99,
            'category': 'Supplements',
            'prescription_required': False
        },
        {
            'name': 'Omega-3 Fish Oil',
            'generic_name': 'Fish Oil',
            'description': 'Essential fatty acids for heart health',
            'dosage': '1000-2000mg daily',
            'side_effects': 'Fishy burps, stomach upset',
            'contraindications': 'Fish allergy, bleeding disorders',
            'price': 14.99,
            'category': 'Supplements',
            'prescription_required': False
        },
        {
            'name': 'Probiotics',
            'generic_name': 'Lactobacillus',
            'description': 'Beneficial bacteria for gut health',
            'dosage': '1-10 billion CFU daily',
            'side_effects': 'Gas, bloating (initially)',
            'contraindications': 'Severe illness, compromised immune system',
            'price': 19.99,
            'category': 'Supplements',
            'prescription_required': False
        },
        
        # Topical Medications
        {
            'name': 'Hydrocortisone Cream',
            'generic_name': 'Hydrocortisone',
            'description': 'Topical steroid for skin inflammation',
            'dosage': 'Apply 1-2 times daily',
            'side_effects': 'Skin thinning, irritation',
            'contraindications': 'Fungal infections, open wounds',
            'price': 6.99,
            'category': 'Dermatological',
            'prescription_required': False
        },
        {
            'name': 'Benzoyl Peroxide',
            'generic_name': 'Benzoyl Peroxide',
            'description': 'Topical treatment for acne',
            'dosage': 'Apply 1-2 times daily',
            'side_effects': 'Skin irritation, dryness, bleaching',
            'contraindications': 'Sensitive skin, pregnancy',
            'price': 7.99,
            'category': 'Dermatological',
            'prescription_required': False
        }
    ]
    
    # Insert medicines data
    cursor.executemany('''
        INSERT INTO medicines (
            name, generic_name, description, dosage, side_effects, 
            contraindications, price, category, prescription_required
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(item['name'], item['generic_name'], item['description'], item['dosage'],
           item['side_effects'], item['contraindications'], item['price'],
           item['category'], item['prescription_required']) 
          for item in enhanced_medicines_data])
    
    print(f"Added {len(enhanced_medicines_data)} enhanced medicines to database")
    
    # Create medicine-symptom mappings for better synchronization
    print("Creating medicine-symptom mappings...")
    
    # Get medicine and symptom IDs for mapping
    cursor.execute("SELECT id, name FROM medicines")
    medicines = cursor.fetchall()
    
    cursor.execute("SELECT id, condition_name, medicine_suggestion FROM symptoms_database")
    symptoms = cursor.fetchall()
    
    # Create mappings based on medicine suggestions in symptoms
    mappings = []
    for symptom_id, condition_name, medicine_suggestion in symptoms:
        if medicine_suggestion:
            suggested_medicines = [med.strip() for med in medicine_suggestion.split(',')]
            for suggested_med in suggested_medicines:
                for med_id, med_name in medicines:
                    if suggested_med.lower() in med_name.lower() or med_name.lower() in suggested_med.lower():
                        mappings.append((med_id, symptom_id, 0.9, f"Effective for {condition_name}"))
                        break
    
    # Insert mappings
    if mappings:
        cursor.executemany('''
            INSERT INTO medicine_symptom_mapping (
                medicine_id, symptom_id, effectiveness_score, usage_notes
            ) VALUES (?, ?, ?, ?)
        ''', mappings)
        
        print(f"Created {len(mappings)} medicine-symptom mappings")
    
    # Populate healthcare providers (reusing the data from previous script)
    print("Populating healthcare providers...")
    
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
        
        # Cardiology
        {
            'doctor_name': 'Dr. William Johnson',
            'hospital_clinic': 'Heart Care Institute',
            'hospital_clinic_address': '579 Palm Street, Cardiology District',
            'hospital_clinic_contact_number': '+1-555-0119',
            'specialty': 'Cardiology',
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
            'specialty': 'Cardiology',
            'experience_years': 18,
            'consultation_fee': 350.00,
            'availability': 'Mon-Fri: 9:00 AM - 6:00 PM',
            'languages_spoken': 'English, Polish'
        },
        
        # Neurology
        {
            'doctor_name': 'Dr. Kevin Patel',
            'hospital_clinic': 'Neurological Institute',
            'hospital_clinic_address': '486 Redwood Drive, Neurology District',
            'hospital_clinic_contact_number': '+1-555-0115',
            'specialty': 'Neurology',
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
            'specialty': 'Neurology',
            'experience_years': 23,
            'consultation_fee': 320.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM',
            'languages_spoken': 'English, Russian'
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
        
        # Dermatology
        {
            'doctor_name': 'Dr. Emily Rodriguez',
            'hospital_clinic': 'Skin Care Clinic',
            'hospital_clinic_address': '147 Birch Street, Dermatology District',
            'hospital_clinic_contact_number': '+1-555-0123',
            'specialty': 'Dermatology',
            'experience_years': 14,
            'consultation_fee': 180.00,
            'availability': 'Mon-Fri: 9:00 AM - 5:00 PM',
            'languages_spoken': 'English, Portuguese'
        },
        {
            'doctor_name': 'Dr. James Wilson',
            'hospital_clinic': 'Advanced Dermatology Center',
            'hospital_clinic_address': '258 Willow Avenue, Skin District',
            'hospital_clinic_contact_number': '+1-555-0124',
            'specialty': 'Dermatology',
            'experience_years': 20,
            'consultation_fee': 200.00,
            'availability': 'Mon-Sat: 9:00 AM - 4:00 PM',
            'languages_spoken': 'English, French'
        }
    ]
    
    # Insert healthcare providers
    cursor.executemany('''
        INSERT INTO healthcare_providers (
            doctor_name, hospital_clinic, hospital_clinic_address, 
            hospital_clinic_contact_number, specialty, experience_years,
            consultation_fee, availability, languages_spoken
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(provider['doctor_name'], provider['hospital_clinic'], provider['hospital_clinic_address'],
           provider['hospital_clinic_contact_number'], provider['specialty'], provider['experience_years'],
           provider['consultation_fee'], provider['availability'], provider['languages_spoken'])
          for provider in healthcare_providers_data])
    
    print(f"Added {len(healthcare_providers_data)} healthcare providers")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("\n🎉 Enhanced database setup completed successfully!")
    print(f"📊 Enhanced database contains:")
    print(f"   • {len(enhanced_symptoms_data)} medical conditions with detailed symptoms")
    print(f"   • {len(enhanced_medicines_data)} medicines with comprehensive information")
    print(f"   • {len(mappings)} medicine-symptom mappings for better synchronization")
    print(f"   • {len(healthcare_providers_data)} healthcare providers")
    print(f"   • Enhanced categories and body system classifications")
    print(f"   • Prescription requirement flags")
    print(f"   • Generic names and detailed dosage information")
    
    print("\n🔧 Key Improvements:")
    print("   • Better medicine-symptom synchronization")
    print("   • Enhanced symptom categorization by body system")
    print("   • More detailed medicine information")
    print("   • Improved healthcare provider database")
    print("   • Better indexing for performance")
    
    print("\n🚀 Next Steps:")
    print("1. Run 'python app.py' to start the application")
    print("2. Test the enhanced symptom diagnosis")
    print("3. Verify medicine-symptom connections")
    print("4. Test the Find Doctor functionality")
    print("5. Check all API endpoints")

if __name__ == '__main__':
    create_enhanced_database() 
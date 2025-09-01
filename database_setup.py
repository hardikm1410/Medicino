#!/usr/bin/env python3
"""
Comprehensive Database Setup for Medicino
This script populates the database with extensive medical data including:
- Symptoms and conditions with Ayurvedic remedies
- Medicine database with detailed information
- Comprehensive symptom mappings
"""

import sqlite3
import os
from datetime import datetime

DATABASE = 'medicino.db'

def create_database():
    """Create and populate the database with comprehensive medical data."""
    
    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("Removed existing database.")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating database tables...")
    
    # Users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medicines table
    cursor.execute('''
        CREATE TABLE medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            dosage TEXT,
            side_effects TEXT,
            contraindications TEXT,
            price REAL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            user_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Symptoms database table
    cursor.execute('''
        CREATE TABLE symptoms_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            severity_level TEXT,
            description TEXT,
            precautions TEXT
        )
    ''')
    
    print("Tables created successfully!")
    
    # Populate symptoms database with comprehensive data
    print("Populating symptoms database...")
    
    symptoms_data = [
        # Respiratory Conditions
        {
            'condition_name': 'Common Cold',
            'symptoms': 'runny nose, sneezing, sore throat, cough, congestion, mild fever, fatigue',
            'ayurvedic_remedy': 'Tulsi tea, ginger tea, honey with warm water, steam inhalation with eucalyptus oil',
            'medicine_suggestion': 'Paracetamol, Vitamin C supplements, Decongestants',
            'severity_level': 'mild',
            'description': 'A viral infection affecting the upper respiratory tract',
            'precautions': 'Rest, stay hydrated, avoid cold foods, maintain good hygiene'
        },
        {
            'condition_name': 'Bronchitis',
            'symptoms': 'persistent cough, chest discomfort, wheezing, shortness of breath, fatigue, mild fever',
            'ayurvedic_remedy': 'Vasaka leaf decoction, Sitopaladi churna, Kantakari tea',
            'medicine_suggestion': 'Bronchodilators, Expectorants, Antibiotics if bacterial',
            'severity_level': 'moderate',
            'description': 'Inflammation of the bronchial tubes causing cough and breathing difficulties',
            'precautions': 'Avoid smoking, stay hydrated, use humidifier, rest'
        },
        {
            'condition_name': 'Pneumonia',
            'symptoms': 'high fever, severe cough, chest pain, difficulty breathing, fatigue, loss of appetite',
            'ayurvedic_remedy': 'Kanakasava, Vasavaleha, Sitopaladi churna',
            'medicine_suggestion': 'Antibiotics, Oxygen therapy, Hospitalization if severe',
            'severity_level': 'severe',
            'description': 'Serious lung infection requiring immediate medical attention',
            'precautions': 'Seek immediate medical care, complete antibiotic course, rest'
        },
        
        # Digestive Conditions
        {
            'condition_name': 'Gastritis',
            'symptoms': 'stomach pain, nausea, vomiting, loss of appetite, bloating, heartburn',
            'ayurvedic_remedy': 'Amla powder, Licorice root, Ginger tea, Aloe vera juice',
            'medicine_suggestion': 'Antacids, Proton pump inhibitors, H2 blockers',
            'severity_level': 'moderate',
            'description': 'Inflammation of the stomach lining causing digestive discomfort',
            'precautions': 'Avoid spicy foods, eat smaller meals, avoid alcohol and smoking'
        },
        {
            'condition_name': 'Food Poisoning',
            'symptoms': 'nausea, vomiting, diarrhea, stomach cramps, fever, dehydration',
            'ayurvedic_remedy': 'Ginger tea, Cumin water, Coriander seeds, ORS solution',
            'medicine_suggestion': 'Oral rehydration solution, Anti-emetics, Anti-diarrheals',
            'severity_level': 'moderate',
            'description': 'Illness caused by consuming contaminated food or water',
            'precautions': 'Stay hydrated, rest, avoid solid foods initially, seek medical care if severe'
        },
        {
            'condition_name': 'Irritable Bowel Syndrome',
            'symptoms': 'abdominal pain, bloating, diarrhea, constipation, gas, mucus in stool',
            'ayurvedic_remedy': 'Triphala churna, Isabgol, Hing, Jeera water',
            'medicine_suggestion': 'Fiber supplements, Anti-spasmodics, Probiotics',
            'severity_level': 'moderate',
            'description': 'Chronic digestive disorder affecting the large intestine',
            'precautions': 'Identify trigger foods, manage stress, regular exercise, fiber-rich diet'
        },
        
        # Cardiovascular Conditions
        {
            'condition_name': 'Hypertension',
            'symptoms': 'headache, dizziness, chest pain, shortness of breath, vision problems, fatigue',
            'ayurvedic_remedy': 'Arjuna bark powder, Sarpagandha, Jatamansi, Garlic',
            'medicine_suggestion': 'ACE inhibitors, Beta blockers, Calcium channel blockers',
            'severity_level': 'severe',
            'description': 'High blood pressure requiring medical management',
            'precautions': 'Regular monitoring, low-salt diet, exercise, stress management'
        },
        {
            'condition_name': 'Angina',
            'symptoms': 'chest pain, pressure in chest, pain radiating to arms, shortness of breath, fatigue',
            'ayurvedic_remedy': 'Arjuna bark, Guggulu, Pushkarmool, Garlic',
            'medicine_suggestion': 'Nitroglycerin, Beta blockers, Calcium channel blockers',
            'severity_level': 'severe',
            'description': 'Chest pain due to reduced blood flow to heart',
            'precautions': 'Immediate medical attention, avoid strenuous activity, quit smoking'
        },
        
        # Neurological Conditions
        {
            'condition_name': 'Migraine',
            'symptoms': 'severe headache, nausea, vomiting, sensitivity to light, aura, dizziness',
            'ayurvedic_remedy': 'Brahmi, Shankhpushpi, Jatamansi, Ginger tea',
            'medicine_suggestion': 'Triptans, NSAIDs, Anti-emetics, Preventive medications',
            'severity_level': 'moderate',
            'description': 'Recurrent severe headaches often with visual disturbances',
            'precautions': 'Identify triggers, maintain regular sleep, avoid stress, stay hydrated'
        },
        {
            'condition_name': 'Tension Headache',
            'symptoms': 'mild to moderate headache, pressure around head, neck pain, stress',
            'ayurvedic_remedy': 'Brahmi, Shankhpushpi, Lavender oil, Peppermint oil',
            'medicine_suggestion': 'Paracetamol, Ibuprofen, Muscle relaxants',
            'severity_level': 'mild',
            'description': 'Common headache caused by stress and muscle tension',
            'precautions': 'Stress management, regular breaks, good posture, relaxation techniques'
        },
        
        # Musculoskeletal Conditions
        {
            'condition_name': 'Arthritis',
            'symptoms': 'joint pain, stiffness, swelling, reduced range of motion, fatigue',
            'ayurvedic_remedy': 'Guggulu, Shallaki, Ashwagandha, Turmeric with milk',
            'medicine_suggestion': 'NSAIDs, DMARDs, Physical therapy, Joint supplements',
            'severity_level': 'moderate',
            'description': 'Inflammation of joints causing pain and stiffness',
            'precautions': 'Regular exercise, weight management, joint protection, balanced diet'
        },
        {
            'condition_name': 'Back Pain',
            'symptoms': 'lower back pain, stiffness, muscle spasms, radiating pain, difficulty moving',
            'ayurvedic_remedy': 'Ashwagandha, Guggulu, Shallaki, Sesame oil massage',
            'medicine_suggestion': 'NSAIDs, Muscle relaxants, Physical therapy, Heat/cold therapy',
            'severity_level': 'moderate',
            'description': 'Common condition affecting the lower back muscles and spine',
            'precautions': 'Good posture, regular exercise, proper lifting techniques, ergonomic setup'
        },
        
        # Skin Conditions
        {
            'condition_name': 'Eczema',
            'symptoms': 'itchy skin, red patches, dry skin, inflammation, scaling, oozing',
            'ayurvedic_remedy': 'Neem paste, Turmeric paste, Coconut oil, Aloe vera gel',
            'medicine_suggestion': 'Topical corticosteroids, Moisturizers, Antihistamines',
            'severity_level': 'moderate',
            'description': 'Chronic skin condition causing inflammation and itching',
            'precautions': 'Avoid triggers, moisturize regularly, gentle skin care, stress management'
        },
        {
            'condition_name': 'Acne',
            'symptoms': 'pimples, blackheads, whiteheads, inflammation, scarring, oily skin',
            'ayurvedic_remedy': 'Neem paste, Turmeric paste, Aloe vera, Sandalwood paste',
            'medicine_suggestion': 'Benzoyl peroxide, Salicylic acid, Retinoids, Antibiotics',
            'severity_level': 'mild',
            'description': 'Common skin condition affecting hair follicles and oil glands',
            'precautions': 'Gentle cleansing, avoid touching face, healthy diet, stress management'
        },
        
        # Endocrine Conditions
        {
            'condition_name': 'Diabetes',
            'symptoms': 'increased thirst, frequent urination, fatigue, blurred vision, slow healing',
            'ayurvedic_remedy': 'Gudmar, Jamun seeds, Bitter gourd, Fenugreek seeds',
            'medicine_suggestion': 'Metformin, Insulin, Sulfonylureas, DPP-4 inhibitors',
            'severity_level': 'severe',
            'description': 'Chronic condition affecting blood sugar regulation',
            'precautions': 'Regular monitoring, balanced diet, exercise, medication compliance'
        },
        {
            'condition_name': 'Thyroid Disorder',
            'symptoms': 'fatigue, weight changes, mood swings, hair loss, temperature sensitivity',
            'ayurvedic_remedy': 'Ashwagandha, Kanchanara, Guggulu, Brahmi',
            'medicine_suggestion': 'Levothyroxine, Anti-thyroid medications, Regular monitoring',
            'severity_level': 'moderate',
            'description': 'Disorder affecting thyroid hormone production',
            'precautions': 'Regular check-ups, medication compliance, balanced diet, stress management'
        },
        
        # Mental Health Conditions
        {
            'condition_name': 'Anxiety',
            'symptoms': 'excessive worry, restlessness, difficulty concentrating, sleep problems, panic attacks',
            'ayurvedic_remedy': 'Brahmi, Jatamansi, Shankhpushpi, Ashwagandha',
            'medicine_suggestion': 'SSRIs, Benzodiazepines, Cognitive behavioral therapy',
            'severity_level': 'moderate',
            'description': 'Mental health condition characterized by excessive worry and fear',
            'precautions': 'Stress management, regular exercise, therapy, medication compliance'
        },
        {
            'condition_name': 'Depression',
            'symptoms': 'persistent sadness, loss of interest, fatigue, sleep changes, appetite changes',
            'ayurvedic_remedy': 'Ashwagandha, Brahmi, Jatamansi, Saffron',
            'medicine_suggestion': 'SSRIs, SNRIs, Psychotherapy, Lifestyle changes',
            'severity_level': 'severe',
            'description': 'Serious mental health condition requiring professional treatment',
            'precautions': 'Seek professional help, maintain routine, social support, medication compliance'
        },
        
        # Eye Conditions
        {
            'condition_name': 'Conjunctivitis',
            'symptoms': 'red eyes, itching, discharge, swelling, sensitivity to light, blurred vision',
            'ayurvedic_remedy': 'Rose water, Honey drops, Triphala eyewash, Coriander water',
            'medicine_suggestion': 'Antibiotic eye drops, Antihistamines, Artificial tears',
            'severity_level': 'mild',
            'description': 'Inflammation of the conjunctiva causing eye irritation',
            'precautions': 'Good hygiene, avoid touching eyes, separate towels, seek medical care'
        },
        
        # Ear Conditions
        {
            'condition_name': 'Ear Infection',
            'symptoms': 'ear pain, hearing loss, fever, drainage, dizziness, pressure in ear',
            'ayurvedic_remedy': 'Garlic oil, Onion juice, Warm compress, Tulsi drops',
            'medicine_suggestion': 'Antibiotics, Pain relievers, Ear drops, Decongestants',
            'severity_level': 'moderate',
            'description': 'Infection of the middle ear requiring medical treatment',
            'precautions': 'Seek medical care, avoid water in ears, complete antibiotic course'
        },
        
        # Urinary Conditions
        {
            'condition_name': 'Urinary Tract Infection',
            'symptoms': 'frequent urination, burning sensation, cloudy urine, pelvic pain, fever',
            'ayurvedic_remedy': 'Cranberry juice, Coriander seeds, Barley water, Coconut water',
            'medicine_suggestion': 'Antibiotics, Increased fluid intake, Pain relievers',
            'severity_level': 'moderate',
            'description': 'Infection of the urinary system requiring antibiotic treatment',
            'precautions': 'Stay hydrated, good hygiene, complete antibiotic course, seek medical care'
        },
        
        
        {
            "condition_name": "Common Cold",
            "symptoms": "runny nose, sneezing, sore throat, cough, congestion, mild fever, fatigue",
            "ayurvedic_remedy": "Tulsi tea, ginger tea, honey with warm water, steam inhalation with eucalyptus oil",
            "medicine_suggestion": "Paracetamol, Vitamin C supplements, Decongestants",
            "severity_level": "mild",
            "description": "A viral infection affecting the upper respiratory tract",
            "precautions": "Rest, stay hydrated, avoid cold foods, maintain good hygiene"
        },
        {
            "condition_name": "Influenza",
            "symptoms": "high fever, body aches, chills, headache, sore throat, dry cough, fatigue",
            "ayurvedic_remedy": "Ginger-turmeric tea, licorice root decoction, warm milk with saffron",
            "medicine_suggestion": "Oseltamivir, Ibuprofen, Antihistamines",
            "severity_level": "moderate",
            "description": "A contagious respiratory illness caused by influenza viruses",
            "precautions": "Get vaccinated, rest, avoid contact with others, stay hydrated"
        },
        {
            "condition_name": "Migraine",
            "symptoms": "throbbing headache, nausea, sensitivity to light, sensitivity to sound, vomiting",
            "ayurvedic_remedy": "Shirodhara with brahmi oil, peppermint tea, avoid spicy foods",
            "medicine_suggestion": "Sumatriptan, Ibuprofen, Antiemetics",
            "severity_level": "moderate",
            "description": "A neurological condition causing severe headaches",
            "precautions": "Avoid triggers, maintain regular sleep, reduce stress, stay hydrated"
        },
        {
            "condition_name": "Allergic Rhinitis",
            "symptoms": "sneezing, itchy nose, watery eyes, nasal congestion, postnasal drip",
            "ayurvedic_remedy": "Neti pot with saline, turmeric milk, licorice tea",
            "medicine_suggestion": "Antihistamines, Nasal corticosteroids, Decongestants",
            "severity_level": "mild",
            "description": "An allergic reaction to airborne allergens like pollen or dust",
            "precautions": "Avoid allergens, use air purifiers, keep windows closed during pollen season"
        },
        {
            "condition_name": "Gastritis",
            "symptoms": "stomach pain, bloating, nausea, vomiting, loss of appetite",
            "ayurvedic_remedy": "Aloe vera juice, fennel tea, avoid spicy foods",
            "medicine_suggestion": "Antacids, Proton pump inhibitors, H2 blockers",
            "severity_level": "moderate",
            "description": "Inflammation of the stomach lining",
            "precautions": "Eat smaller meals, avoid alcohol, reduce stress, avoid irritant foods"
        },
        {
            "condition_name": "Bronchitis",
            "symptoms": "persistent cough, mucus production, chest discomfort, fatigue, shortness of breath",
            "ayurvedic_remedy": "Tulsi steam inhalation, licorice root tea, ginger-honey mix",
            "medicine_suggestion": "Cough suppressants, Bronchodilators, Antibiotics (if bacterial)",
            "severity_level": "moderate",
            "description": "Inflammation of the bronchial tubes",
            "precautions": "Avoid smoking, stay hydrated, rest, use a humidifier"
        },
        {
            "condition_name": "Sinusitis",
            "symptoms": "facial pain, nasal congestion, headache, thick nasal discharge, reduced smell",
            "ayurvedic_remedy": "Steam inhalation with eucalyptus, neti pot, turmeric milk",
            "medicine_suggestion": "Decongestants, Nasal corticosteroids, Antibiotics (if bacterial)",
            "severity_level": "moderate",
            "description": "Inflammation of the sinuses",
            "precautions": "Stay hydrated, avoid allergens, use saline nasal sprays"
        },
        {
            "condition_name": "Tonsillitis",
            "symptoms": "sore throat, difficulty swallowing, swollen tonsils, fever, bad breath",
            "ayurvedic_remedy": "Gargle with turmeric water, licorice tea, honey with warm water",
            "medicine_suggestion": "Antibiotics (if bacterial), Paracetamol, Throat lozenges",
            "severity_level": "moderate",
            "description": "Inflammation of the tonsils due to infection",
            "precautions": "Rest, stay hydrated, avoid irritants, maintain hygiene"
        },
        {
            "condition_name": "Conjunctivitis",
            "symptoms": "red eyes, itching, watery discharge, burning sensation, crusty eyes",
            "ayurvedic_remedy": "Rose water eye wash, triphala eyewash, aloe vera gel",
            "medicine_suggestion": "Antibiotic eye drops (if bacterial), Antihistamine drops",
            "severity_level": "mild",
            "description": "Inflammation of the conjunctiva",
            "precautions": "Avoid touching eyes, wash hands frequently, avoid sharing towels"
        },
        {
            "condition_name": "Urinary Tract Infection",
            "symptoms": "burning sensation during urination, frequent urination, cloudy urine, pelvic pain",
            "ayurvedic_remedy": "Coriander seed water, cranberry juice, avoid spicy foods",
            "medicine_suggestion": "Antibiotics, Pain relievers, Urinary alkalizers",
            "severity_level": "moderate",
            "description": "Infection in the urinary system",
            "precautions": "Stay hydrated, urinate frequently, maintain hygiene"
        },
        {
            "condition_name": "Arthritis",
            "symptoms": "joint pain, stiffness, swelling, reduced mobility, fatigue",
            "ayurvedic_remedy": "Ashwagandha powder, ginger-turmeric tea, warm oil massage",
            "medicine_suggestion": "NSAIDs, Corticosteroids, Disease-modifying antirheumatic drugs",
            "severity_level": "moderate",
            "description": "Inflammation of the joints",
            "precautions": "Exercise regularly, maintain healthy weight, avoid cold exposure"
        },
        {
            "condition_name": "Asthma",
            "symptoms": "wheezing, shortness of breath, chest tightness, coughing",
            "ayurvedic_remedy": "Tulsi tea, licorice root decoction, steam inhalation",
            "medicine_suggestion": "Inhaled corticosteroids, Bronchodilators, Leukotriene modifiers",
            "severity_level": "moderate",
            "description": "A chronic respiratory condition causing airway inflammation",
            "precautions": "Avoid triggers, use inhalers, maintain clean environment"
        },
        {
            "condition_name": "Eczema",
            "symptoms": "itchy skin, redness, dry patches, inflammation, scaling",
            "ayurvedic_remedy": "Neem oil application, turmeric paste, aloe vera gel",
            "medicine_suggestion": "Topical corticosteroids, Antihistamines, Moisturizers",
            "severity_level": "mild",
            "description": "A chronic skin condition causing inflammation and irritation",
            "precautions": "Avoid irritants, keep skin moisturized, use gentle soaps"
        },
        {
            "condition_name": "Acne",
            "symptoms": "pimples, blackheads, whiteheads, oily skin, scarring",
            "ayurvedic_remedy": "Neem face mask, turmeric paste, sandalwood powder",
            "medicine_suggestion": "Benzoyl peroxide, Retinoids, Antibiotics",
            "severity_level": "mild",
            "description": "A skin condition caused by clogged pores",
            "precautions": "Cleanse skin regularly, avoid oily products, maintain hygiene"
        },
        {
            "condition_name": "Irritable Bowel Syndrome",
            "symptoms": "abdominal pain, bloating, diarrhea, constipation, gas",
            "ayurvedic_remedy": "Fennel tea, peppermint oil, avoid heavy meals",
            "medicine_suggestion": "Antispasmodics, Laxatives, Antidiarrheals",
            "severity_level": "moderate",
            "description": "A functional gastrointestinal disorder",
            "precautions": "Eat fiber-rich diet, manage stress, avoid trigger foods"
        },
        {
            "condition_name": "Anemia",
            "symptoms": "fatigue, pale skin, shortness of breath, dizziness, cold hands",
            "ayurvedic_remedy": "Pomegranate juice, beetroot juice, sesame seeds",
            "medicine_suggestion": "Iron supplements, Vitamin B12, Folic acid",
            "severity_level": "moderate",
            "description": "A condition with low red blood cell count",
            "precautions": "Eat iron-rich foods, avoid tea with meals, regular check-ups"
        },
        {
            "condition_name": "Hypertension",
            "symptoms": "headache, dizziness, blurred vision, chest pain, fatigue",
            "ayurvedic_remedy": "Arjuna bark tea, ashwagandha powder, avoid salty foods",
            "medicine_suggestion": "ACE inhibitors, Beta-blockers, Diuretics",
            "severity_level": "moderate",
            "description": "High blood pressure affecting the cardiovascular system",
            "precautions": "Reduce salt intake, exercise regularly, manage stress"
        },
        {
            "condition_name": "Diabetes Type 2",
            "symptoms": "increased thirst, frequent urination, fatigue, blurred vision, slow healing",
            "ayurvedic_remedy": "Fenugreek water, bitter gourd juice, cinnamon tea",
            "medicine_suggestion": "Metformin, Insulin, Sulfonylureas",
            "severity_level": "moderate",
            "description": "A chronic condition affecting blood sugar regulation",
            "precautions": "Monitor blood sugar, follow diet plan, exercise regularly"
        },
        {
            "condition_name": "Insomnia",
            "symptoms": "difficulty falling asleep, staying asleep, daytime fatigue, irritability",
            "ayurvedic_remedy": "Warm milk with nutmeg, ashwagandha tea, meditation",
            "medicine_suggestion": "Melatonin, Sedative-hypnotics, Antihistamines",
            "severity_level": "mild",
            "description": "A sleep disorder causing difficulty in sleeping",
            "precautions": "Maintain sleep schedule, avoid caffeine, create bedtime routine"
        },
        {
            "condition_name": "Anxiety",
            "symptoms": "restlessness, rapid heartbeat, sweating, trembling, worry",
            "ayurvedic_remedy": "Brahmi tea, ashwagandha powder, meditation",
            "medicine_suggestion": "SSRIs, Benzodiazepines, Beta-blockers",
            "severity_level": "moderate",
            "description": "A mental health condition causing excessive worry",
            "precautions": "Practice relaxation techniques, avoid caffeine, seek therapy"
        },
        {
            "condition_name": "Depression",
            "symptoms": "sadness, loss of interest, fatigue, sleep changes, appetite changes",
            "ayurvedic_remedy": "Saffron tea, ashwagandha powder, yoga",
            "medicine_suggestion": "SSRIs, SNRIs, Tricyclic antidepressants",
            "severity_level": "moderate",
            "description": "A mental health disorder causing persistent sadness",
            "precautions": "Seek therapy, maintain social connections, exercise"
        },
        {
            "condition_name": "Gastroesophageal Reflux Disease",
            "symptoms": "heartburn, regurgitation, chest pain, difficulty swallowing",
            "ayurvedic_remedy": "Aloe vera juice, fennel tea, avoid spicy foods",
            "medicine_suggestion": "Proton pump inhibitors, H2 blockers, Antacids",
            "severity_level": "moderate",
            "description": "A digestive disorder causing acid reflux",
            "precautions": "Avoid trigger foods, eat smaller meals, elevate head during sleep"
        },
        {
            "condition_name": "Psoriasis",
            "symptoms": "red patches, silvery scales, itching, dry skin, joint pain",
            "ayurvedic_remedy": "Neem oil, turmeric paste, aloe vera gel",
            "medicine_suggestion": "Topical corticosteroids, Vitamin D analogues, Retinoids",
            "severity_level": "moderate",
            "description": "A chronic autoimmune skin condition",
            "precautions": "Moisturize skin, avoid triggers, manage stress"
        },
        {
            "condition_name": "Hemorrhoids",
            "symptoms": "rectal bleeding, itching, pain, swelling, discomfort",
            "ayurvedic_remedy": "Triphala powder, warm sitz bath, aloe vera gel",
            "medicine_suggestion": "Hydrocortisone cream, Pain relievers, Stool softeners",
            "severity_level": "mild",
            "description": "Swollen veins in the lower rectum or anus",
            "precautions": "Eat high-fiber diet, stay hydrated, avoid straining"
        },
        {
            "condition_name": "Sciatica",
            "symptoms": "lower back pain, leg pain, numbness, tingling, muscle weakness",
            "ayurvedic_remedy": "Castor oil massage, turmeric milk, yoga",
            "medicine_suggestion": "NSAIDs, Muscle relaxants, Corticosteroids",
            "severity_level": "moderate",
            "description": "Pain radiating along the sciatic nerve",
            "precautions": "Maintain good posture, exercise regularly, avoid heavy lifting"
        },
        {
            "condition_name": "Gout",
            "symptoms": "sudden joint pain, swelling, redness, warmth, stiffness",
            "ayurvedic_remedy": "Cherry juice, ginger tea, avoid purine-rich foods",
            "medicine_suggestion": "NSAIDs, Colchicine, Corticosteroids",
            "severity_level": "moderate",
            "description": "A form of arthritis caused by uric acid buildup",
            "precautions": "Stay hydrated, avoid alcohol, limit purine-rich foods"
        },
        {
            "condition_name": "Kidney Stones",
            "symptoms": "severe back pain, abdominal pain, blood in urine, nausea, vomiting",
            "ayurvedic_remedy": "Coconut water, coriander seed water, lemon water",
            "medicine_suggestion": "Pain relievers, Alpha-blockers, Diuretics",
            "severity_level": "severe",
            "description": "Hard deposits formed in the kidneys",
            "precautions": "Stay hydrated, reduce salt intake, avoid oxalate-rich foods"
        },
        {
            "condition_name": "Peptic Ulcer",
            "symptoms": "burning stomach pain, bloating, heartburn, nausea, vomiting",
            "ayurvedic_remedy": "Licorice root tea, aloe vera juice, avoid spicy foods",
            "medicine_suggestion": "Proton pump inhibitors, Antibiotics, Antacids",
            "severity_level": "moderate",
            "description": "Sores in the stomach lining or duodenum",
            "precautions": "Avoid NSAIDs, reduce stress, eat smaller meals"
        },
        {
            "condition_name": "Sprained Ankle",
            "symptoms": "pain, swelling, bruising, limited mobility, tenderness",
            "ayurvedic_remedy": "Turmeric paste, castor oil wrap, rest",
            "medicine_suggestion": "NSAIDs, Pain relievers, Compression wraps",
            "severity_level": "mild",
            "description": "Injury to the ligaments of the ankle",
            "precautions": "Rest, ice, compress, elevate, avoid strenuous activity"
        },
        {
            "condition_name": "Carpal Tunnel Syndrome",
            "symptoms": "wrist pain, numbness, tingling, hand weakness, burning sensation",
            "ayurvedic_remedy": "Ashwagandha oil massage, turmeric milk, wrist exercises",
            "medicine_suggestion": "NSAIDs, Corticosteroid injections, Wrist splints",
            "severity_level": "moderate",
            "description": "Compression of the median nerve in the wrist",
            "precautions": "Avoid repetitive wrist movements, use ergonomic tools"
        },
        {
            "condition_name": "Tendinitis",
            "symptoms": "pain near joint, stiffness, swelling, tenderness",
            "ayurvedic_remedy": "Castor oil massage, turmeric paste, rest",
            "medicine_suggestion": "NSAIDs, Corticosteroids, Physical therapy",
            "severity_level": "moderate",
            "description": "Inflammation of a tendon",
            "precautions": "Rest, avoid repetitive strain, use proper techniques"
        },
        {
            "condition_name": "Chronic Fatigue Syndrome",
            "symptoms": "extreme fatigue, muscle pain, poor concentration, sleep issues",
            "ayurvedic_remedy": "Ashwagandha powder, ginseng tea, meditation",
            "medicine_suggestion": "Antidepressants, Sleep aids, Pain relievers",
            "severity_level": "moderate",
            "description": "A condition causing persistent fatigue",
            "precautions": "Pace activities, maintain sleep hygiene, manage stress"
        },
        {
            "condition_name": "Vertigo",
            "symptoms": "dizziness, spinning sensation, nausea, balance issues, sweating",
            "ayurvedic_remedy": "Ginger tea, brahmi oil, avoid sudden movements",
            "medicine_suggestion": "Antihistamines, Benzodiazepines, Antiemetics",
            "severity_level": "moderate",
            "description": "A sensation of spinning or dizziness",
            "precautions": "Avoid triggers, move slowly, stay hydrated"
        },
        {
            "condition_name": "Rosacea",
            "symptoms": "facial redness, flushing, visible blood vessels, pimples, burning",
            "ayurvedic_remedy": "Sandalwood paste, aloe vera gel, avoid spicy foods",
            "medicine_suggestion": "Metronidazole cream, Azelaic acid, Antibiotics",
            "severity_level": "mild",
            "description": "A chronic skin condition causing facial redness",
            "precautions": "Avoid triggers, use gentle skincare, protect from sun"
        },
        {
            "condition_name": "Hives",
            "symptoms": "itchy welts, redness, swelling, burning sensation",
            "ayurvedic_remedy": "Neem paste, turmeric milk, avoid allergens",
            "medicine_suggestion": "Antihistamines, Corticosteroids, Epinephrine (severe cases)",
            "severity_level": "mild",
            "description": "A skin reaction causing itchy welts",
            "precautions": "Avoid allergens, keep skin cool, avoid tight clothing"
        },
        {
            "condition_name": "Athlete’s Foot",
            "symptoms": "itchy feet, scaling, redness, cracked skin, burning",
            "ayurvedic_remedy": "Neem oil, tea tree oil, foot soak with turmeric",
            "medicine_suggestion": "Antifungal creams, Oral antifungals, Antihistamines",
            "severity_level": "mild",
            "description": "A fungal infection affecting the feet",
            "precautions": "Keep feet dry, wear breathable shoes, avoid sharing towels"
        },
        {
            "condition_name": "Dandruff",
            "symptoms": "flaky scalp, itching, dry scalp, redness",
            "ayurvedic_remedy": "Coconut oil with neem, lemon rinse, aloe vera gel",
            "medicine_suggestion": "Antifungal shampoos, Coal tar shampoos, Corticosteroids",
            "severity_level": "mild",
            "description": "A scalp condition causing flaking and itching",
            "precautions": "Wash hair regularly, avoid harsh products, manage stress"
        },
        {
            "condition_name": "Menstrual Cramps",
            "symptoms": "lower abdominal pain, bloating, fatigue, mood swings",
            "ayurvedic_remedy": "Ginger tea, sesame oil massage, fennel tea",
            "medicine_suggestion": "NSAIDs, Oral contraceptives, Pain relievers",
            "severity_level": "mild",
            "description": "Painful uterine contractions during menstruation",
            "precautions": "Use heat therapy, stay hydrated, avoid caffeine"
        },
        {
            "condition_name": "Constipation",
            "symptoms": "infrequent bowel movements, hard stools, straining, bloating",
            "ayurvedic_remedy": "Triphala powder, warm water with lemon, figs",
            "medicine_suggestion": "Laxatives, Stool softeners, Fiber supplements",
            "severity_level": "mild",
            "description": "Difficulty in passing stools",
            "precautions": "Eat high-fiber diet, stay hydrated, exercise regularly"
        },
        {
            "condition_name": "Diarrhea",
            "symptoms": "loose stools, frequent bowel movements, abdominal cramps, dehydration",
            "ayurvedic_remedy": "Pomegranate juice, buttermilk, avoid oily foods",
            "medicine_suggestion": "Loperamide, Oral rehydration salts, Antispasmodics",
            "severity_level": "moderate",
            "description": "Frequent passage of loose or watery stools",
            "precautions": "Stay hydrated, avoid trigger foods, maintain hygiene"
        },
        {
            "condition_name": "Food Poisoning",
            "symptoms": "nausea, vomiting, diarrhea, abdominal pain, fever",
            "ayurvedic_remedy": "Ginger tea, cumin water, avoid heavy meals",
            "medicine_suggestion": "Antiemetics, Antibiotics (if bacterial), Rehydration salts",
            "severity_level": "moderate",
            "description": "Illness caused by contaminated food",
            "precautions": "Cook food thoroughly, avoid raw foods, maintain hygiene"
        },
        {
            "condition_name": "Sunburn",
            "symptoms": "red skin, pain, blistering, peeling, sensitivity",
            "ayurvedic_remedy": "Aloe vera gel, coconut oil, sandalwood paste",
            "medicine_suggestion": "Hydrocortisone cream, NSAIDs, Moisturizers",
            "severity_level": "mild",
            "description": "Skin damage caused by UV exposure",
            "precautions": "Use sunscreen, wear protective clothing, avoid peak sun hours"
        },
        {
            "condition_name": "Heat Rash",
            "symptoms": "itchy red bumps, prickling sensation, small blisters",
            "ayurvedic_remedy": "Sandalwood powder, neem paste, cool compress",
            "medicine_suggestion": "Calamine lotion, Antihistamines, Hydrocortisone cream",
            "severity_level": "mild",
            "description": "Skin irritation due to blocked sweat ducts",
            "precautions": "Stay cool, wear loose clothing, avoid excessive sweating"
        },
        {
            "condition_name": "Mouth Ulcers",
            "symptoms": "painful sores in mouth, difficulty eating, burning sensation",
            "ayurvedic_remedy": "Honey application, licorice gargle, coconut oil",
            "medicine_suggestion": "Topical anesthetics, Antiseptic gels, Pain relievers",
            "severity_level": "mild",
            "description": "Sores on the mucous membrane of the mouth",
            "precautions": "Avoid spicy foods, maintain oral hygiene, stay hydrated"
        },
        {
            "condition_name": "Dry Eyes",
            "symptoms": "gritty sensation, burning, redness, blurred vision, sensitivity",
            "ayurvedic_remedy": "Rose water drops, triphala eyewash, ghee application",
            "medicine_suggestion": "Artificial tears, Cyclosporine drops, Punctal plugs",
            "severity_level": "mild",
            "description": "Insufficient tear production or poor tear quality",
            "precautions": "Use humidifiers, avoid screens, blink frequently"
        },
        {
            "condition_name": "Heartburn",
            "symptoms": "burning in chest, sour taste, regurgitation, throat irritation",
            "ayurvedic_remedy": "Fennel tea, aloe vera juice, avoid spicy foods",
            "medicine_suggestion": "Antacids, H2 blockers, Proton pump inhibitors",
            "severity_level": "mild",
            "description": "A burning sensation due to acid reflux",
            "precautions": "Avoid trigger foods, eat smaller meals, stay upright after eating"
        },
        {
            "condition_name": "Nasal Polyps",
            "symptoms": "nasal congestion, runny nose, reduced smell, facial pain",
            "ayurvedic_remedy": "Neti pot, turmeric milk, steam inhalation",
            "medicine_suggestion": "Nasal corticosteroids, Antihistamines, Surgery (if severe)",
            "severity_level": "moderate",
            "description": "Noncancerous growths in the nasal passages",
            "precautions": "Avoid irritants, manage allergies, use humidifiers"
        },
        {
            "condition_name": "Ear Infection",
            "symptoms": "ear pain, hearing loss, fluid drainage, fever, irritability",
            "ayurvedic_remedy": "Garlic oil drops, tulsi tea, warm compress",
            "medicine_suggestion": "Antibiotics, Pain relievers, Ear drops",
            "severity_level": "moderate",
            "description": "Infection in the middle or outer ear",
            "precautions": "Keep ears dry, avoid inserting objects, treat colds promptly"
        },
        {
            "condition_name": "Pink Eye",
            "symptoms": "red eyes, itching, discharge, crusty eyes, tearing",
            "ayurvedic_remedy": "Rose water wash, triphala eyewash, aloe vera gel",
            "medicine_suggestion": "Antibiotic eye drops, Antihistamines, Artificial tears",
            "severity_level": "mild",
            "description": "Inflammation or infection of the conjunctiva",
            "precautions": "Avoid touching eyes, wash hands, avoid sharing towels"
        },
        {
            "condition_name": "Strep Throat",
            "symptoms": "sore throat, fever, swollen lymph nodes, difficulty swallowing",
            "ayurvedic_remedy": "Turmeric gargle, licorice tea, honey with warm water",
            "medicine_suggestion": "Antibiotics, Pain relievers, Throat lozenges",
            "severity_level": "moderate",
            "description": "A bacterial infection in the throat",
            "precautions": "Rest, stay hydrated, avoid spreading infection"
        },
        {
            "condition_name": "Laryngitis",
            "symptoms": "hoarse voice, sore throat, dry cough, difficulty speaking",
            "ayurvedic_remedy": "Ginger-honey tea, licorice gargle, steam inhalation",
            "medicine_suggestion": "Pain relievers, Throat lozenges, Corticosteroids",
            "severity_level": "mild",
            "description": "Inflammation of the voice box",
            "precautions": "Rest voice, stay hydrated, avoid irritants"
        },
        {
            "condition_name": "Shingles",
            "symptoms": "painful rash, blisters, itching, fever, sensitivity",
            "ayurvedic_remedy": "Neem paste, turmeric milk, aloe vera gel",
            "medicine_suggestion": "Antiviral drugs, Pain relievers, Corticosteroids",
            "severity_level": "moderate",
            "description": "A viral infection causing a painful rash",
            "precautions": "Avoid contact with others, manage stress, keep rash clean"
        },
        {
            "condition_name": "Plantar Fasciitis",
            "symptoms": "heel pain, stiffness, swelling, tenderness",
            "ayurvedic_remedy": "Castor oil massage, turmeric paste, foot stretches",
            "medicine_suggestion": "NSAIDs, Orthotics, Corticosteroid injections",
            "severity_level": "moderate",
            "description": "Inflammation of the plantar fascia in the foot",
            "precautions": "Wear supportive shoes, stretch regularly, avoid overexertion"
        },
        {
            "condition_name": "Cystitis",
            "symptoms": "painful urination, frequent urination, pelvic discomfort, cloudy urine",
            "ayurvedic_remedy": "Coriander seed water, cranberry juice, avoid irritants",
            "medicine_suggestion": "Antibiotics, Pain relievers, Urinary alkalizers",
            "severity_level": "moderate",
            "description": "Inflammation of the bladder, often due to infection",
            "precautions": "Stay hydrated, urinate frequently, maintain hygiene"
        },
        {
            "condition_name": "Menopause Symptoms",
            "symptoms": "hot flashes, night sweats, mood swings, fatigue, vaginal dryness",
            "ayurvedic_remedy": "Shatavari powder, ashwagandha tea, cooling foods",
            "medicine_suggestion": "Hormone replacement therapy, Antidepressants, Gabapentin",
            "severity_level": "moderate",
            "description": "Symptoms associated with the end of menstrual cycles",
            "precautions": "Stay cool, exercise, manage stress, eat balanced diet"
        },
        {
            "condition_name": "Restless Leg Syndrome",
            "symptoms": "urge to move legs, tingling, discomfort, worse at night",
            "ayurvedic_remedy": "Ashwagandha oil massage, warm milk with nutmeg, yoga",
            "medicine_suggestion": "Dopamine agonists, Gabapentin, Iron supplements",
            "severity_level": "moderate",
            "description": "A neurological disorder causing leg discomfort",
            "precautions": "Avoid caffeine, exercise regularly, maintain sleep schedule"
        },
        {
            "condition_name": "Tinnitus",
            "symptoms": "ringing in ears, buzzing, humming, hearing loss",
            "ayurvedic_remedy": "Sesame oil ear drops, brahmi tea, avoid loud noises",
            "medicine_suggestion": "Antidepressants, Antianxiety drugs, Hearing aids",
            "severity_level": "mild",
            "description": "Perception of noise or ringing in the ears",
            "precautions": "Protect ears from loud noises, manage stress, avoid caffeine"
        },
        {
            "condition_name": "Mastitis",
            "symptoms": "breast pain, swelling, redness, fever, chills",
            "ayurvedic_remedy": "Warm compress, turmeric milk, cabbage leaf wrap",
            "medicine_suggestion": "Antibiotics, Pain relievers, Anti-inflammatory drugs",
            "severity_level": "moderate",
            "description": "Inflammation of the breast, often due to infection",
            "precautions": "Continue breastfeeding, maintain hygiene, rest"
        },
        {
            "condition_name": "Pinched Nerve",
            "symptoms": "sharp pain, numbness, tingling, muscle weakness",
            "ayurvedic_remedy": "Castor oil massage, turmeric milk, yoga",
            "medicine_suggestion": "NSAIDs, Corticosteroids, Physical therapy",
            "severity_level": "moderate",
            "description": "Compression of a nerve causing pain or numbness",
            "precautions": "Maintain good posture, avoid repetitive motions, rest"
        },
        {
            "condition_name": "Gallstones",
            "symptoms": "abdominal pain, nausea, vomiting, bloating, jaundice",
            "ayurvedic_remedy": "Lemon water, turmeric tea, avoid fatty foods",
            "medicine_suggestion": "Pain relievers, Ursodiol, Surgery (if severe)",
            "severity_level": "severe",
            "description": "Hardened deposits in the gallbladder",
            "precautions": "Maintain healthy weight, avoid fatty foods, stay hydrated"
        },
        {
            "condition_name": "Chronic Sinusitis",
            "symptoms": "nasal congestion, facial pain, headache, thick discharge",
            "ayurvedic_remedy": "Neti pot, eucalyptus steam, turmeric milk",
            "medicine_suggestion": "Nasal corticosteroids, Antibiotics, Decongestants",
            "severity_level": "moderate",
            "description": "Long-term inflammation of the sinuses",
            "precautions": "Avoid allergens, use humidifiers, stay hydrated"
        },
        {
            "condition_name": "Tension Headache",
            "symptoms": "tight band-like pain, neck stiffness, scalp tenderness",
            "ayurvedic_remedy": "Peppermint oil massage, brahmi tea, yoga",
            "medicine_suggestion": "NSAIDs, Muscle relaxants, Analgesics",
            "severity_level": "mild",
            "description": "A headache caused by muscle tension",
            "precautions": "Manage stress, maintain posture, stay hydrated"
        },
        {
            "condition_name": "Bursitis",
            "symptoms": "joint pain, swelling, stiffness, warmth, tenderness",
            "ayurvedic_remedy": "Turmeric paste, castor oil wrap, rest",
            "medicine_suggestion": "NSAIDs, Corticosteroid injections, Physical therapy",
            "severity_level": "moderate",
            "description": "Inflammation of the bursa near joints",
            "precautions": "Avoid repetitive motions, rest, use proper techniques"
        },
        {
            "condition_name": "Diverticulitis",
            "symptoms": "abdominal pain, fever, nausea, constipation, diarrhea",
            "ayurvedic_remedy": "Aloe vera juice, fennel tea, avoid heavy foods",
            "medicine_suggestion": "Antibiotics, Pain relievers, Liquid diet",
            "severity_level": "moderate",
            "description": "Inflammation of pouches in the colon",
            "precautions": "Eat high-fiber diet, stay hydrated, avoid seeds"
        },
        {
            "condition_name": "Canker Sores",
            "symptoms": "painful mouth sores, burning, difficulty eating, sensitivity",
            "ayurvedic_remedy": "Honey application, licorice gargle, coconut oil",
            "medicine_suggestion": "Topical anesthetics, Antiseptic gels, Corticosteroids",
            "severity_level": "mild",
            "description": "Small ulcers in the mouth",
            "precautions": "Avoid spicy foods, maintain oral hygiene, reduce stress"
        },
        {
            "condition_name": "Gingivitis",
            "symptoms": "gum swelling, bleeding, bad breath, tenderness",
            "ayurvedic_remedy": "Neem mouth rinse, clove oil, turmeric gargle",
            "medicine_suggestion": "Antiseptic mouthwash, Antibiotics, Dental cleaning",
            "severity_level": "mild",
            "description": "Inflammation of the gums",
            "precautions": "Brush regularly, floss, avoid smoking"
        },
        {
            "condition_name": "Hypothyroidism",
            "symptoms": "fatigue, weight gain, cold intolerance, dry skin, hair loss",
            "ayurvedic_remedy": "Ashwagandha powder, guggul, avoid cruciferous vegetables",
            "medicine_suggestion": "Levothyroxine, Thyroid hormone replacement",
            "severity_level": "moderate",
            "description": "Underactive thyroid gland",
            "precautions": "Monitor thyroid levels, eat balanced diet, avoid stress"
        },
        {
            "condition_name": "Hyperthyroidism",
            "symptoms": "weight loss, rapid heartbeat, sweating, nervousness, heat intolerance",
            "ayurvedic_remedy": "Brahmi tea, ashwagandha, cooling foods",
            "medicine_suggestion": "Antithyroid drugs, Beta-blockers, Radioactive iodine",
            "severity_level": "moderate",
            "description": "Overactive thyroid gland",
            "precautions": "Monitor thyroid levels, avoid caffeine, manage stress"
        },
        {
            "condition_name": "Chlamydia",
            "symptoms": "painful urination, abnormal discharge, pelvic pain, testicular pain",
            "ayurvedic_remedy": "Coriander seed water, neem tea, avoid irritants",
            "medicine_suggestion": "Antibiotics, Pain relievers",
            "severity_level": "moderate",
            "description": "A sexually transmitted bacterial infection",
            "precautions": "Practice safe sex, get tested, avoid sexual contact until treated"
        },
        {
            "condition_name": "Gonorrhea",
            "symptoms": "painful urination, discharge, pelvic pain, sore throat",
            "ayurvedic_remedy": "Neem tea, turmeric milk, avoid spicy foods",
            "medicine_suggestion": "Antibiotics, Pain relievers",
            "severity_level": "moderate",
            "description": "A sexually transmitted bacterial infection",
            "precautions": "Practice safe sex, get tested, avoid sexual contact until treated"
        },
        {
            "condition_name": "Herpes Simplex",
            "symptoms": "painful sores, itching, burning, fever, swollen lymph nodes",
            "ayurvedic_remedy": "Neem paste, aloe vera gel, licorice tea",
            "medicine_suggestion": "Antiviral drugs, Pain relievers, Topical creams",
            "severity_level": "moderate",
            "description": "A viral infection causing sores",
            "precautions": "Avoid contact during outbreaks, practice safe sex, manage stress"
        },
        {
            "condition_name": "Yeast Infection",
            "symptoms": "vaginal itching, discharge, burning, redness, discomfort",
            "ayurvedic_remedy": "Coconut oil, yogurt application, neem tea",
            "medicine_suggestion": "Antifungal creams, Oral antifungals, Probiotics",
            "severity_level": "mild",
            "description": "A fungal infection in the vaginal area",
            "precautions": "Keep area dry, wear breathable clothing, avoid douching"
        },
        {
            "condition_name": "Jock Itch",
            "symptoms": "itchy groin, redness, rash, burning, scaling",
            "ayurvedic_remedy": "Neem oil, turmeric paste, keep area dry",
            "medicine_suggestion": "Antifungal creams, Oral antifungals, Antihistamines",
            "severity_level": "mild",
            "description": "A fungal infection in the groin area",
            "precautions": "Keep area dry, wear loose clothing, avoid sharing towels"
        },
        {
            "condition_name": "Ringworm",
            "symptoms": "red ring-shaped rash, itching, scaling, raised edges",
            "ayurvedic_remedy": "Neem paste, turmeric paste, tea tree oil",
            "medicine_suggestion": "Antifungal creams, Oral antifungals, Antihistamines",
            "severity_level": "mild",
            "description": "A fungal infection of the skin",
            "precautions": "Keep skin clean, avoid sharing personal items, treat promptly"
        },
        {
            "condition_name": "Lice Infestation",
            "symptoms": "scalp itching, visible lice, nits on hair, irritation",
            "ayurvedic_remedy": "Neem oil, coconut oil, combing with fine-tooth comb",
            "medicine_suggestion": "Permethrin lotion, Ivermectin, Combing",
            "severity_level": "mild",
            "description": "Parasitic infestation of the scalp or body",
            "precautions": "Wash bedding, avoid sharing combs, treat all contacts"
        },
        {
            "condition_name": "Scabies",
            "symptoms": "intense itching, rash, burrows, redness, sores",
            "ayurvedic_remedy": "Neem oil, turmeric paste, sulfur ointment",
            "medicine_suggestion": "Permethrin cream, Ivermectin, Antihistamines",
            "severity_level": "moderate",
            "description": "A skin infestation caused by mites",
            "precautions": "Wash bedding, treat all contacts, avoid close contact"
        },
        {
            "condition_name": "Impetigo",
            "symptoms": "red sores, blisters, crusty patches, itching, pain",
            "ayurvedic_remedy": "Neem paste, turmeric paste, honey application",
            "medicine_suggestion": "Antibiotic ointments, Oral antibiotics, Antiseptics",
            "severity_level": "mild",
            "description": "A bacterial skin infection",
            "precautions": "Keep skin clean, avoid scratching, wash hands frequently"
        },
        {
            "condition_name": "Cellulitis",
            "symptoms": "redness, swelling, warmth, pain, fever",
            "ayurvedic_remedy": "Turmeric paste, neem oil, warm compress",
            "medicine_suggestion": "Antibiotics, Pain relievers, Elevation",
            "severity_level": "moderate",
            "description": "A bacterial infection of the skin and tissues",
            "precautions": "Keep skin clean, treat cuts promptly, monitor for worsening"
        },
        {
            "condition_name": "Boils",
            "symptoms": "painful lump, redness, pus, swelling, warmth",
            "ayurvedic_remedy": "Turmeric paste, neem oil, warm compress",
            "medicine_suggestion": "Antibiotics, Pain relievers, Incision and drainage",
            "severity_level": "moderate",
            "description": "A bacterial infection of a hair follicle",
            "precautions": "Keep area clean, avoid squeezing, maintain hygiene"
        },
        {
            "condition_name": "Folliculitis",
            "symptoms": "red bumps, pustules, itching, tenderness, rash",
            "ayurvedic_remedy": "Neem oil, turmeric paste, warm compress",
            "medicine_suggestion": "Antibiotic creams, Antifungals, Antiseptics",
            "severity_level": "mild",
            "description": "Inflammation of hair follicles",
            "precautions": "Avoid tight clothing, keep skin clean, avoid shaving irritation"
        },
        {
            "condition_name": "Cold Sores",
            "symptoms": "painful blisters, tingling, itching, crusting, fever",
            "ayurvedic_remedy": "Neem paste, licorice tea, aloe vera gel",
            "medicine_suggestion": "Antiviral creams, Oral antivirals, Pain relievers",
            "severity_level": "mild",
            "description": "A viral infection caused by herpes simplex virus",
            "precautions": "Avoid touching sores, manage stress, use sunscreen"
        },
        {
            "condition_name": "Warts",
            "symptoms": "small growths, rough texture, pain, black dots",
            "ayurvedic_remedy": "Neem oil, turmeric paste, banana peel application",
            "medicine_suggestion": "Salicylic acid, Cryotherapy, Laser treatment",
            "severity_level": "mild",
            "description": "Skin growths caused by human papillomavirus",
            "precautions": "Avoid touching warts, keep skin clean, avoid sharing towels"
        },
        {
            "condition_name": "Seborrheic Dermatitis",
            "symptoms": "scaly patches, redness, itching, greasy skin",
            "ayurvedic_remedy": "Coconut oil, neem paste, aloe vera gel",
            "medicine_suggestion": "Antifungal creams, Corticosteroids, Medicated shampoos",
            "severity_level": "mild",
            "description": "A skin condition affecting oily areas",
            "precautions": "Wash regularly, avoid harsh soaps, manage stress"
        },
        {
            "condition_name": "Contact Dermatitis",
            "symptoms": "red rash, itching, blisters, burning, swelling",
            "ayurvedic_remedy": "Aloe vera gel, neem paste, cool compress",
            "medicine_suggestion": "Corticosteroids, Antihistamines, Barrier creams",
            "severity_level": "mild",
            "description": "A skin reaction to an irritant or allergen",
            "precautions": "Avoid triggers, use protective gear, keep skin moisturized"
        },
        {
            "condition_name": "Mumps",
            "symptoms": "swollen salivary glands, fever, headache, muscle aches, fatigue",
            "ayurvedic_remedy": "Tulsi tea, ginger tea, warm compress",
            "medicine_suggestion": "Pain relievers, Antipyretics, Rest",
            "severity_level": "moderate",
            "description": "A viral infection affecting the salivary glands",
            "precautions": "Get vaccinated, avoid contact, rest, stay hydrated"
        },
        {
            "condition_name": "Chickenpox",
            "symptoms": "itchy rash, blisters, fever, fatigue, headache",
            "ayurvedic_remedy": "Neem bath, turmeric paste, oatmeal bath",
            "medicine_suggestion": "Antiviral drugs, Antihistamines, Pain relievers",
            "severity_level": "moderate",
            "description": "A viral infection causing an itchy rash",
            "precautions": "Avoid scratching, stay isolated, get vaccinated"
        },
        {
            "condition_name": "Measles",
            "symptoms": "fever, rash, cough, runny nose, red eyes",
            "ayurvedic_remedy": "Tulsi tea, saffron milk, rest",
            "medicine_suggestion": "Vitamin A, Pain relievers, Antipyretics",
            "severity_level": "severe",
            "description": "A highly contagious viral infection",
            "precautions": "Get vaccinated, avoid contact, rest, stay hydrated"
        },
        {
            "condition_name": "Whooping Cough",
            "symptoms": "severe cough, whooping sound, vomiting, fatigue",
            "ayurvedic_remedy": "Tulsi tea, licorice root, steam inhalation",
            "medicine_suggestion": "Antibiotics, Cough suppressants, Rest",
            "severity_level": "severe",
            "description": "A bacterial infection causing severe coughing",
            "precautions": "Get vaccinated, avoid contact, maintain hygiene"
        },
        {
            "condition_name": "Mononucleosis",
            "symptoms": "fatigue, sore throat, fever, swollen lymph nodes, rash",
            "ayurvedic_remedy": "Tulsi tea, ginger tea, rest",
            "medicine_suggestion": "Pain relievers, Corticosteroids, Rest",
            "severity_level": "moderate",
            "description": "A viral infection caused by Epstein-Barr virus",
            "precautions": "Rest, avoid contact sports, stay hydrated"
        },
        {
            "condition_name": "Hepatitis A",
            "symptoms": "fatigue, nausea, jaundice, abdominal pain, fever",
            "ayurvedic_remedy": "Pomegranate juice, turmeric milk, avoid fatty foods",
            "medicine_suggestion": "Supportive care, Rest, Hydration",
            "severity_level": "moderate",
            "description": "A viral infection affecting the liver",
            "precautions": "Get vaccinated, maintain hygiene, avoid contaminated food"
        },
        {
            "condition_name": "Hepatitis B",
            "symptoms": "jaundice, fatigue, abdominal pain, dark urine, fever",
            "ayurvedic_remedy": "Bhumyamalaki powder, turmeric milk, avoid alcohol",
            "medicine_suggestion": "Antiviral drugs, Supportive care, Rest",
            "severity_level": "severe",
            "description": "A viral infection affecting the liver",
            "precautions": "Get vaccinated, practice safe sex, avoid sharing needles"
        },
        {
            "condition_name": "Dengue Fever",
            "symptoms": "high fever, severe headache, joint pain, rash, fatigue",
            "ayurvedic_remedy": "Papaya leaf juice, tulsi tea, rest",
            "medicine_suggestion": "Pain relievers, Hydration, Rest",
            "severity_level": "severe",
            "description": "A mosquito-borne viral infection",
            "precautions": "Use mosquito repellent, wear protective clothing, stay hydrated"
        },
        {
            "condition_name": "Malaria",
            "symptoms": "fever, chills, headache, muscle pain, fatigue",
            "ayurvedic_remedy": "Neem tea, tulsi tea, avoid mosquito bites",
            "medicine_suggestion": "Antimalarial drugs, Pain relievers, Rest",
            "severity_level": "severe",
            "description": "A parasitic infection transmitted by mosquitoes",
            "precautions": "Use mosquito nets, take prophylaxis, avoid mosquito bites"
        },
        

    ]
    
    cursor.executemany('''
        INSERT INTO symptoms_database (condition_name, symptoms, ayurvedic_remedy, medicine_suggestion, severity_level, description, precautions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [(item['condition_name'], item['symptoms'], item['ayurvedic_remedy'], 
           item['medicine_suggestion'], item['severity_level'], item['description'], item['precautions']) 
          for item in symptoms_data])
    
    print(f"Added {len(symptoms_data)} conditions to symptoms database")
    
    # Populate medicines database with comprehensive data
    print("Populating medicines database...")
    
    medicines_data = [
        # Pain Relief4
        {
            'name': 'Lisinopril',
            'description': 'ACE inhibitor used to treat high blood pressure and heart failure',
            'dosage': '10-40mg once daily',
            'side_effects': 'Dizziness, headache, persistent cough',
            'contraindications': 'Pregnancy, angioedema, renal artery stenosis',
            'price': 14.50,
            'category': 'Cardiovascular'
        },
        {
            'name': 'Levothyroxine',
            'description': 'Synthetic thyroid hormone for hypothyroidism',
            'dosage': '25-100mcg daily',
            'side_effects': 'Palpitations, weight loss, nervousness',
            'contraindications': 'Thyrotoxicosis, uncorrected adrenal insufficiency',
            'price': 12.00,
            'category': 'Hormonal'
        },
        {
            'name': 'Clopidogrel',
            'description': 'Antiplatelet drug to prevent strokes and heart attacks',
            'dosage': '75mg once daily',
            'side_effects': 'Bleeding, rash, gastrointestinal upset',
            'contraindications': 'Active bleeding, peptic ulcer, bleeding disorders',
            'price': 18.90,
            'category': 'Cardiovascular'
        },
        {
            'name': 'Esomeprazole',
            'description': 'Proton pump inhibitor for acid reflux and ulcers',
            'dosage': '20-40mg daily before meals',
            'side_effects': 'Nausea, flatulence, abdominal pain',
            'contraindications': 'Liver disease, osteoporosis',
            'price': 16.75,
            'category': 'Digestive Health'
        },
        {
            'name': 'Metronidazole',
            'description': 'Antibiotic for bacterial and parasitic infections',
            'dosage': '500mg every 8 hours for 7-10 days',
            'side_effects': 'Metallic taste, nausea, dizziness',
            'contraindications': 'Alcohol use, liver disease, pregnancy (1st trimester)',
            'price': 11.00,
            'category': 'Antibiotic'
        },
        {
            'name': 'Azithromycin',
            'description': 'Macrolide antibiotic for respiratory and skin infections',
            'dosage': '500mg on day 1, then 250mg for 4 days',
            'side_effects': 'Diarrhea, nausea, abdominal pain',
            'contraindications': 'Liver problems, QT prolongation',
            'price': 19.25,
            'category': 'Antibiotic'
        },
        {
            'name': 'Diclofenac',
            'description': 'NSAID for pain, inflammation, and arthritis',
            'dosage': '50mg 2-3 times daily',
            'side_effects': 'Stomach pain, heartburn, nausea',
            'contraindications': 'Ulcers, heart disease, kidney problems',
            'price': 10.60,
            'category': 'Pain Relief'
        },
        {
            'name': 'Duloxetine',
            'description': 'Antidepressant for depression and nerve pain',
            'dosage': '30-60mg once daily',
            'side_effects': 'Dry mouth, fatigue, nausea',
            'contraindications': 'MAOI use, liver disease, uncontrolled glaucoma',
            'price': 23.40,
            'category': 'Mental Health'
        },
        {
            'name': 'Bisoprolol',
            'description': 'Beta-blocker for high blood pressure and heart failure',
            'dosage': '5-10mg once daily',
            'side_effects': 'Bradycardia, fatigue, cold extremities',
            'contraindications': 'Asthma, heart block, severe bradycardia',
            'price': 15.70,
            'category': 'Cardiovascular'
        },
        {
            'name': 'Montelukast',
            'description': 'Leukotriene receptor antagonist for asthma and allergies',
            'dosage': '10mg once daily in the evening',
            'side_effects': 'Headache, abdominal pain, behavioral changes',
            'contraindications': 'Liver impairment, mental health disorders',
            'price': 17.80,
            'category': 'Respiratory'
        },
        {
            'name': 'Ranitidine',
            'description': 'H2 blocker for ulcers and gastroesophageal reflux',
            'dosage': '150mg twice daily',
            'side_effects': 'Constipation, headache, dizziness',
            'contraindications': 'Porphyria, hypersensitivity',
            'price': 8.25,
            'category': 'Digestive Health'
        },
        {
            'name': 'Tamsulosin',
            'description': 'Alpha-blocker for enlarged prostate (BPH)',
            'dosage': '0.4mg once daily after the same meal',
            'side_effects': 'Dizziness, retrograde ejaculation, nasal congestion',
            'contraindications': 'Severe liver disease, orthostatic hypotension',
            'price': 19.10,
            'category': 'Urology'
        },
        {
            'name': 'Risperidone',
            'description': 'Antipsychotic for schizophrenia and bipolar disorder',
            'dosage': '1-6mg daily depending on condition',
            'side_effects': 'Weight gain, drowsiness, restlessness',
            'contraindications': 'Dementia-related psychosis, heart conditions',
            'price': 25.00,
            'category': 'Mental Health'
        },
        {
            'name': 'Fluconazole',
            'description': 'Antifungal for yeast and fungal infections',
            'dosage': '150mg single dose or 50-200mg daily',
            'side_effects': 'Nausea, abdominal pain, headache',
            'contraindications': 'Liver disease, QT prolongation',
            'price': 13.90,
            'category': 'Antifungal'
        },
        {
            'name': 'Sildenafil',
            'description': 'Used for erectile dysfunction and pulmonary hypertension',
            'dosage': '50mg one hour before activity',
            'side_effects': 'Flushing, headache, vision changes',
            'contraindications': 'Nitrate medications, severe heart conditions',
            'price': 27.50,
            'category': 'Men’s Health'
        },
        {
            'name': 'Pregabalin',
            'description': 'Used for nerve pain, epilepsy, and anxiety',
            'dosage': '75-150mg twice daily',
            'side_effects': 'Dizziness, weight gain, dry mouth',
            'contraindications': 'Renal impairment, history of substance abuse',
            'price': 22.80,
            'category': 'Neurology'
        },
        {
            'name': 'Miconazole',
            'description': 'Topical antifungal for skin infections',
            'dosage': 'Apply 2 times daily for 2-4 weeks',
            'side_effects': 'Skin irritation, burning, redness',
            'contraindications': 'Allergy to imidazoles',
            'price': 9.50,
            'category': 'Dermatology'
        },
        {
            'name': 'Ciprofloxacin',
            'description': 'Fluoroquinolone antibiotic for various infections',
            'dosage': '250-750mg every 12 hours',
            'side_effects': 'Nausea, tendon rupture, rash',
            'contraindications': 'Tendon disorders, myasthenia gravis',
            'price': 20.60,
            'category': 'Antibiotic'
        },
        {
            'name': 'Finasteride',
            'description': 'Used for BPH and hair loss',
            'dosage': '1-5mg once daily',
            'side_effects': 'Decreased libido, erectile dysfunction, breast tenderness',
            'contraindications': 'Pregnancy (Category X), liver disease',
            'price': 18.00,
            'category': 'Men’s Health'
        },
        {
            'name': 'Zolpidem',
            'description': 'Sedative-hypnotic for short-term treatment of insomnia',
            'dosage': '5-10mg at bedtime',
            'side_effects': 'Drowsiness, dizziness, memory loss',
            'contraindications': 'Severe liver impairment, sleep apnea',
            'price': 24.20,
            'category': 'Sleep Aid'
        },
        {
            'name': 'Paracetamol',
            'description': 'Over-the-counter pain reliever and fever reducer',
            'dosage': '500-1000mg every 4-6 hours, max 4000mg/day',
            'side_effects': 'Nausea, stomach upset, liver damage in high doses',
            'contraindications': 'Liver disease, alcohol dependence, pregnancy (consult doctor)',
            'price': 5.99,
            'category': 'Pain Relief'
        },
        {
            'name': 'Ibuprofen',
            'description': 'Non-steroidal anti-inflammatory drug for pain and inflammation',
            'dosage': '200-400mg every 4-6 hours, max 1200mg/day',
            'side_effects': 'Stomach upset, heartburn, increased bleeding risk',
            'contraindications': 'Stomach ulcers, heart disease, kidney problems',
            'price': 7.99,
            'category': 'Pain Relief'
        },
        {
            'name': 'Aspirin',
            'description': 'Pain reliever and blood thinner',
            'dosage': '325-650mg every 4-6 hours',
            'side_effects': 'Stomach irritation, bleeding risk, ringing in ears',
            'contraindications': 'Bleeding disorders, stomach ulcers, children under 12',
            'price': 4.99,
            'category': 'Pain Relief'
        },
        
        # Respiratory
        {
            'name': 'Salbutamol',
            'description': 'Bronchodilator for asthma and breathing difficulties',
            'dosage': '2 puffs every 4-6 hours as needed',
            'side_effects': 'Tremors, increased heart rate, nervousness',
            'contraindications': 'Severe heart disease, uncontrolled arrhythmias',
            'price': 15.99,
            'category': 'Respiratory'
        },
        {
            'name': 'Amoxicillin',
            'description': 'Antibiotic for bacterial infections',
            'dosage': '250-500mg three times daily for 7-10 days',
            'side_effects': 'Diarrhea, nausea, allergic reactions',
            'contraindications': 'Penicillin allergy, mononucleosis',
            'price': 12.99,
            'category': 'Antibiotics'
        },
        
        # Digestive
        {
            'name': 'Omeprazole',
            'description': 'Proton pump inhibitor for acid reflux and ulcers',
            'dosage': '20-40mg once daily before breakfast',
            'side_effects': 'Headache, diarrhea, vitamin B12 deficiency',
            'contraindications': 'Liver disease, pregnancy, long-term use',
            'price': 18.99,
            'category': 'Digestive'
        },
        {
            'name': 'Metformin',
            'description': 'Oral diabetes medication to control blood sugar',
            'dosage': '500-2000mg daily in divided doses',
            'side_effects': 'Nausea, diarrhea, lactic acidosis (rare)',
            'contraindications': 'Severe kidney disease, heart failure',
            'price': 25.99,
            'category': 'Diabetes'
        },
        
        # Cardiovascular
        {
            'name': 'Amlodipine',
            'description': 'Calcium channel blocker for high blood pressure',
            'dosage': '5-10mg once daily',
            'side_effects': 'Swelling in ankles, dizziness, flushing',
            'contraindications': 'Severe heart failure, aortic stenosis',
            'price': 22.99,
            'category': 'Cardiovascular'
        },
        {
            'name': 'Atorvastatin',
            'description': 'Statin medication to lower cholesterol',
            'dosage': '10-80mg once daily',
            'side_effects': 'Muscle pain, liver problems, diabetes risk',
            'contraindications': 'Liver disease, pregnancy, active liver disease',
            'price': 28.99,
            'category': 'Cardiovascular'
        },
        
        # Mental Health
        {
            'name': 'Sertraline',
            'description': 'SSRI antidepressant for depression and anxiety',
            'dosage': '50-200mg once daily',
            'side_effects': 'Nausea, insomnia, sexual dysfunction',
            'contraindications': 'MAOI use, bipolar disorder, pregnancy',
            'price': 35.99,
            'category': 'Mental Health'
        },
        {
            'name': 'Alprazolam',
            'description': 'Benzodiazepine for anxiety and panic disorders',
            'dosage': '0.25-1mg three times daily',
            'side_effects': 'Drowsiness, dependence, memory problems',
            'contraindications': 'Respiratory depression, pregnancy, alcohol use',
            'price': 32.99,
            'category': 'Mental Health'
        },
        
        # Skin
        {
            'name': 'Hydrocortisone',
            'description': 'Topical corticosteroid for skin inflammation',
            'dosage': 'Apply 1-2 times daily to affected area',
            'side_effects': 'Skin thinning, stretch marks, local irritation',
            'contraindications': 'Fungal infections, open wounds, face use',
            'price': 8.99,
            'category': 'Dermatology'
        },
        {
            'name': 'Benzoyl Peroxide',
            'description': 'Topical medication for acne treatment',
            'dosage': 'Apply 1-2 times daily to affected areas',
            'side_effects': 'Skin irritation, dryness, bleaching of clothes',
            'contraindications': 'Sensitive skin, pregnancy, breastfeeding',
            'price': 9.99,
            'category': 'Dermatology'
        },
        
        # Vitamins and Supplements
        {
            'name': 'Vitamin D3',
            'description': 'Essential vitamin for bone health and immune function',
            'dosage': '1000-4000 IU daily',
            'side_effects': 'Nausea, kidney stones (high doses)',
            'contraindications': 'Hypercalcemia, kidney disease',
            'price': 14.99,
            'category': 'Vitamins'
        },
        {
            'name': 'Omega-3 Fish Oil',
            'description': 'Essential fatty acids for heart and brain health',
            'dosage': '1000-2000mg daily',
            'side_effects': 'Fishy burps, diarrhea, bleeding risk',
            'contraindications': 'Bleeding disorders, fish allergies',
            'price': 19.99,
            'category': 'Supplements'
        },
        {
            'name': 'Probiotics',
            'description': 'Beneficial bacteria for gut health',
            'dosage': '1-2 capsules daily with meals',
            'side_effects': 'Mild bloating, gas, diarrhea initially',
            'contraindications': 'Severe immune deficiency, acute pancreatitis',
            'price': 16.99,
            'category': 'Supplements'
        },
        
        # Sleep and Relaxation
        {
            'name': 'Melatonin',
            'description': 'Natural sleep hormone for insomnia',
            'dosage': '1-5mg 30 minutes before bedtime',
            'side_effects': 'Drowsiness, vivid dreams, morning grogginess',
            'contraindications': 'Pregnancy, autoimmune disorders',
            'price': 11.99,
            'category': 'Sleep'
        },
        {
            'name': 'Valerian Root',
            'description': 'Natural herb for sleep and anxiety',
            'dosage': '300-600mg 30 minutes before bedtime',
            'side_effects': 'Drowsiness, vivid dreams, liver problems',
            'contraindications': 'Liver disease, pregnancy, driving',
            'price': 13.99,
            'category': 'Natural Remedies'
        },
        
        # Cough and Cold
        {
            'name': 'Dextromethorphan',
            'description': 'Cough suppressant for dry cough',
            'dosage': '15-30mg every 4-6 hours',
            'side_effects': 'Drowsiness, dizziness, nausea',
            'contraindications': 'MAOI use, chronic cough, asthma',
            'price': 6.99,
            'category': 'Cough & Cold'
        },
        {
            'name': 'Guaifenesin',
            'description': 'Expectorant to loosen chest congestion',
            'dosage': '200-400mg every 4 hours',
            'side_effects': 'Nausea, vomiting, dizziness',
            'contraindications': 'Severe kidney disease, pregnancy',
            'price': 7.99,
            'category': 'Cough & Cold'
        },
        
        # Allergy
        {
            'name': 'Cetirizine',
            'description': 'Antihistamine for allergy relief',
            'dosage': '10mg once daily',
            'side_effects': 'Drowsiness, dry mouth, headache',
            'contraindications': 'Kidney disease, pregnancy, driving',
            'price': 10.99,
            'category': 'Allergy'
        },
        {
            'name': 'Loratadine',
            'description': 'Non-drowsy antihistamine for allergies',
            'dosage': '10mg once daily',
            'side_effects': 'Headache, dry mouth, fatigue',
            'contraindications': 'Liver disease, pregnancy, children under 2',
            'price': 12.99,
            'category': 'Allergy'
        },
        
        # Women's Health
        {
            'name': 'Folic Acid',
            'description': 'Essential B vitamin for pregnancy and cell growth',
            'dosage': '400-800mcg daily',
            'side_effects': 'Nausea, bitter taste, allergic reactions',
            'contraindications': 'Vitamin B12 deficiency, cancer',
            'price': 8.99,
            'category': 'Women\'s Health'
        },
        {
            'name': 'Iron Supplement',
            'description': 'Mineral supplement for iron deficiency anemia',
            'dosage': '65-200mg daily with vitamin C',
            'side_effects': 'Constipation, black stools, stomach upset',
            'contraindications': 'Hemochromatosis, thalassemia',
            'price': 11.99,
            'category': 'Supplements'
        },
        
        # Men's Health
        {
            'name': 'Saw Palmetto',
            'description': 'Natural supplement for prostate health',
            'dosage': '160-320mg daily',
            'side_effects': 'Stomach upset, headache, decreased libido',
            'contraindications': 'Pregnancy, hormone-sensitive conditions',
            'price': 17.99,
            'category': 'Men\'s Health'
        },
        
        # Eye Health
        {
            'name': 'Lutein',
            'description': 'Carotenoid for eye health and macular degeneration',
            'dosage': '10-20mg daily',
            'side_effects': 'Yellow skin discoloration, stomach upset',
            'contraindications': 'Pregnancy, breastfeeding',
            'price': 15.99,
            'category': 'Eye Health'
        },
        
        # Bone Health
        {
            'name': 'Calcium Carbonate',
            'description': 'Mineral supplement for bone health',
            'dosage': '500-1000mg daily with vitamin D',
            'side_effects': 'Constipation, gas, kidney stones',
            'contraindications': 'Hypercalcemia, kidney stones',
            'price': 9.99,
            'category': 'Bone Health'
        },
        {
            'name': 'Glucosamine',
            'description': 'Natural compound for joint health and arthritis',
            'dosage': '1500mg daily',
            'side_effects': 'Stomach upset, headache, allergic reactions',
            'contraindications': 'Shellfish allergy, diabetes, pregnancy',
            'price': 21.99,
            'category': 'Joint Health'
        },
    ]
    
    cursor.executemany('''
        INSERT INTO medicines (name, description, dosage, side_effects, contraindications, price, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [(item['name'], item['description'], item['dosage'], item['side_effects'],
           item['contraindications'], item['price'], item['category']) 
          for item in medicines_data])
    
    print(f"Added {len(medicines_data)} medicines to database")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("\n🎉 Database setup completed successfully!")
    print(f"📊 Database contains:")
    print(f"   • {len(symptoms_data)} medical conditions with symptoms")
    print(f"   • {len(medicines_data)} medicines with detailed information")
    print(f"   • Comprehensive Ayurvedic remedies")
    print(f"   • Severity levels and precautions")
    print(f"   • Price information and categories")
    
    print("\n🔧 Next Steps:")
    print("1. Run 'python app.py' to start the application")
    print("2. Register a new account")
    print("3. Test the symptom diagnosis with various conditions")
    print("4. Explore the medicine database")
    print("5. Check diagnosis history functionality")

if __name__ == '__main__':
    create_database()

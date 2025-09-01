#!/usr/bin/env python3
"""
Database Enhancement Script for Medicino
Adds comprehensive medical data to existing database
"""

import sqlite3
import os

DATABASE = 'medicino.db'

def enhance_database():
    """Add comprehensive medical data to existing database."""
    
    if not os.path.exists(DATABASE):
        print("Database not found. Please run the main application first.")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    print("Enhancing database with comprehensive medical data...")
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    cursor.execute("DELETE FROM symptoms_database")
    cursor.execute("DELETE FROM medicines")
    print("Cleared existing data tables")
    
    # Add comprehensive symptoms data
    symptoms_data = [
        # Respiratory
        ('Common Cold', 'runny nose, sneezing, sore throat, cough, congestion, mild fever, fatigue', 
         'Tulsi tea, ginger tea, honey with warm water, steam inhalation with eucalyptus oil',
         'Paracetamol, Vitamin C supplements, Decongestants', 'mild',
         'A viral infection affecting the upper respiratory tract',
         'Rest, stay hydrated, avoid cold foods, maintain good hygiene'),
        
        ('Bronchitis', 'persistent cough, chest discomfort, wheezing, shortness of breath, fatigue, mild fever',
         'Vasaka leaf decoction, Sitopaladi churna, Kantakari tea',
         'Bronchodilators, Expectorants, Antibiotics if bacterial', 'moderate',
         'Inflammation of the bronchial tubes causing cough and breathing difficulties',
         'Avoid smoking, stay hydrated, use humidifier, rest'),
        
        ('Pneumonia', 'high fever, severe cough, chest pain, difficulty breathing, fatigue, loss of appetite',
         'Kanakasava, Vasavaleha, Sitopaladi churna',
         'Antibiotics, Oxygen therapy, Hospitalization if severe', 'severe',
         'Serious lung infection requiring immediate medical attention',
         'Seek immediate medical care, complete antibiotic course, rest'),
        
        # Digestive
        ('Gastritis', 'stomach pain, nausea, vomiting, loss of appetite, bloating, heartburn',
         'Amla powder, Licorice root, Ginger tea, Aloe vera juice',
         'Antacids, Proton pump inhibitors, H2 blockers', 'moderate',
         'Inflammation of the stomach lining causing digestive discomfort',
         'Avoid spicy foods, eat smaller meals, avoid alcohol and smoking'),
        
        ('Food Poisoning', 'nausea, vomiting, diarrhea, stomach cramps, fever, dehydration',
         'Ginger tea, Cumin water, Coriander seeds, ORS solution',
         'Oral rehydration solution, Anti-emetics, Anti-diarrheals', 'moderate',
         'Illness caused by consuming contaminated food or water',
         'Stay hydrated, rest, avoid solid foods initially, seek medical care if severe'),
        
        ('Irritable Bowel Syndrome', 'abdominal pain, bloating, diarrhea, constipation, gas, mucus in stool',
         'Triphala churna, Isabgol, Hing, Jeera water',
         'Fiber supplements, Anti-spasmodics, Probiotics', 'moderate',
         'Chronic digestive disorder affecting the large intestine',
         'Identify trigger foods, manage stress, regular exercise, fiber-rich diet'),
        
        # Cardiovascular
        ('Hypertension', 'headache, dizziness, chest pain, shortness of breath, vision problems, fatigue',
         'Arjuna bark powder, Sarpagandha, Jatamansi, Garlic',
         'ACE inhibitors, Beta blockers, Calcium channel blockers', 'severe',
         'High blood pressure requiring medical management',
         'Regular monitoring, low-salt diet, exercise, stress management'),
        
        ('Angina', 'chest pain, pressure in chest, pain radiating to arms, shortness of breath, fatigue',
         'Arjuna bark, Guggulu, Pushkarmool, Garlic',
         'Nitroglycerin, Beta blockers, Calcium channel blockers', 'severe',
         'Chest pain due to reduced blood flow to heart',
         'Immediate medical attention, avoid strenuous activity, quit smoking'),
        
        # Neurological
        ('Migraine', 'severe headache, nausea, vomiting, sensitivity to light, aura, dizziness',
         'Brahmi, Shankhpushpi, Jatamansi, Ginger tea',
         'Triptans, NSAIDs, Anti-emetics, Preventive medications', 'moderate',
         'Recurrent severe headaches often with visual disturbances',
         'Identify triggers, maintain regular sleep, avoid stress, stay hydrated'),
        
        ('Tension Headache', 'mild to moderate headache, pressure around head, neck pain, stress',
         'Brahmi, Shankhpushpi, Lavender oil, Peppermint oil',
         'Paracetamol, Ibuprofen, Muscle relaxants', 'mild',
         'Common headache caused by stress and muscle tension',
         'Stress management, regular breaks, good posture, relaxation techniques'),
        
        # Musculoskeletal
        ('Arthritis', 'joint pain, stiffness, swelling, reduced range of motion, fatigue',
         'Guggulu, Shallaki, Ashwagandha, Turmeric with milk',
         'NSAIDs, DMARDs, Physical therapy, Joint supplements', 'moderate',
         'Inflammation of joints causing pain and stiffness',
         'Regular exercise, weight management, joint protection, balanced diet'),
        
        ('Back Pain', 'lower back pain, stiffness, muscle spasms, radiating pain, difficulty moving',
         'Ashwagandha, Guggulu, Shallaki, Sesame oil massage',
         'NSAIDs, Muscle relaxants, Physical therapy, Heat/cold therapy', 'moderate',
         'Common condition affecting the lower back muscles and spine',
         'Good posture, regular exercise, proper lifting techniques, ergonomic setup'),
        
        # Skin
        ('Eczema', 'itchy skin, red patches, dry skin, inflammation, scaling, oozing',
         'Neem paste, Turmeric paste, Coconut oil, Aloe vera gel',
         'Topical corticosteroids, Moisturizers, Antihistamines', 'moderate',
         'Chronic skin condition causing inflammation and itching',
         'Avoid triggers, moisturize regularly, gentle skin care, stress management'),
        
        ('Acne', 'pimples, blackheads, whiteheads, inflammation, scarring, oily skin',
         'Neem paste, Turmeric paste, Aloe vera, Sandalwood paste',
         'Benzoyl peroxide, Salicylic acid, Retinoids, Antibiotics', 'mild',
         'Common skin condition affecting hair follicles and oil glands',
         'Gentle cleansing, avoid touching face, healthy diet, stress management'),
        
        # Endocrine
        ('Diabetes', 'increased thirst, frequent urination, fatigue, blurred vision, slow healing',
         'Gudmar, Jamun seeds, Bitter gourd, Fenugreek seeds',
         'Metformin, Insulin, Sulfonylureas, DPP-4 inhibitors', 'severe',
         'Chronic condition affecting blood sugar regulation',
         'Regular monitoring, balanced diet, exercise, medication compliance'),
        
        ('Thyroid Disorder', 'fatigue, weight changes, mood swings, hair loss, temperature sensitivity',
         'Ashwagandha, Kanchanara, Guggulu, Brahmi',
         'Levothyroxine, Anti-thyroid medications, Regular monitoring', 'moderate',
         'Disorder affecting thyroid hormone production',
         'Regular check-ups, medication compliance, balanced diet, stress management'),
        
        # Mental Health
        ('Anxiety', 'excessive worry, restlessness, difficulty concentrating, sleep problems, panic attacks',
         'Brahmi, Jatamansi, Shankhpushpi, Ashwagandha',
         'SSRIs, Benzodiazepines, Cognitive behavioral therapy', 'moderate',
         'Mental health condition characterized by excessive worry and fear',
         'Stress management, regular exercise, therapy, medication compliance'),
        
        ('Depression', 'persistent sadness, loss of interest, fatigue, sleep changes, appetite changes',
         'Ashwagandha, Brahmi, Jatamansi, Saffron',
         'SSRIs, SNRIs, Psychotherapy, Lifestyle changes', 'severe',
         'Serious mental health condition requiring professional treatment',
         'Seek professional help, maintain routine, social support, medication compliance'),
        
        # Eye & Ear
        ('Conjunctivitis', 'red eyes, itching, discharge, swelling, sensitivity to light, blurred vision',
         'Rose water, Honey drops, Triphala eyewash, Coriander water',
         'Antibiotic eye drops, Antihistamines, Artificial tears', 'mild',
         'Inflammation of the conjunctiva causing eye irritation',
         'Good hygiene, avoid touching eyes, separate towels, seek medical care'),
        
        ('Ear Infection', 'ear pain, hearing loss, fever, drainage, dizziness, pressure in ear',
         'Garlic oil, Onion juice, Warm compress, Tulsi drops',
         'Antibiotics, Pain relievers, Ear drops, Decongestants', 'moderate',
         'Infection of the middle ear requiring medical treatment',
         'Seek medical care, avoid water in ears, complete antibiotic course'),
        
        # Urinary
        ('Urinary Tract Infection', 'frequent urination, burning sensation, cloudy urine, pelvic pain, fever',
         'Cranberry juice, Coriander seeds, Barley water, Coconut water',
         'Antibiotics, Increased fluid intake, Pain relievers', 'moderate',
         'Infection of the urinary system requiring antibiotic treatment',
         'Stay hydrated, good hygiene, complete antibiotic course, seek medical care')
    ]
    
    cursor.executemany('''
        INSERT INTO symptoms_database (condition_name, symptoms, ayurvedic_remedy, medicine_suggestion, severity_level, description, precautions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', symptoms_data)
    
    print(f"Added {len(symptoms_data)} conditions to symptoms database")
    
    # Add comprehensive medicines data
    medicines_data = [
        # Pain Relief
        ('Paracetamol', 'Over-the-counter pain reliever and fever reducer', '500-1000mg every 4-6 hours, max 4000mg/day',
         'Nausea, stomach upset, liver damage in high doses', 'Liver disease, alcohol dependence, pregnancy (consult doctor)',
         5.99, 'Pain Relief'),
        
        ('Ibuprofen', 'Non-steroidal anti-inflammatory drug for pain and inflammation', '200-400mg every 4-6 hours, max 1200mg/day',
         'Stomach upset, heartburn, increased bleeding risk', 'Stomach ulcers, heart disease, kidney problems',
         7.99, 'Pain Relief'),
        
        ('Aspirin', 'Pain reliever and blood thinner', '325-650mg every 4-6 hours',
         'Stomach irritation, bleeding risk, ringing in ears', 'Bleeding disorders, stomach ulcers, children under 12',
         4.99, 'Pain Relief'),
        
        # Respiratory
        ('Salbutamol', 'Bronchodilator for asthma and breathing difficulties', '2 puffs every 4-6 hours as needed',
         'Tremors, increased heart rate, nervousness', 'Severe heart disease, uncontrolled arrhythmias',
         15.99, 'Respiratory'),
        
        ('Amoxicillin', 'Antibiotic for bacterial infections', '250-500mg three times daily for 7-10 days',
         'Diarrhea, nausea, allergic reactions', 'Penicillin allergy, mononucleosis',
         12.99, 'Antibiotics'),
        
        # Digestive
        ('Omeprazole', 'Proton pump inhibitor for acid reflux and ulcers', '20-40mg once daily before breakfast',
         'Headache, diarrhea, vitamin B12 deficiency', 'Liver disease, pregnancy, long-term use',
         18.99, 'Digestive'),
        
        ('Metformin', 'Oral diabetes medication to control blood sugar', '500-2000mg daily in divided doses',
         'Nausea, diarrhea, lactic acidosis (rare)', 'Severe kidney disease, heart failure',
         25.99, 'Diabetes'),
        
        # Cardiovascular
        ('Amlodipine', 'Calcium channel blocker for high blood pressure', '5-10mg once daily',
         'Swelling in ankles, dizziness, flushing', 'Severe heart failure, aortic stenosis',
         22.99, 'Cardiovascular'),
        
        ('Atorvastatin', 'Statin medication to lower cholesterol', '10-80mg once daily',
         'Muscle pain, liver problems, diabetes risk', 'Liver disease, pregnancy, active liver disease',
         28.99, 'Cardiovascular'),
        
        # Mental Health
        ('Sertraline', 'SSRI antidepressant for depression and anxiety', '50-200mg once daily',
         'Nausea, insomnia, sexual dysfunction', 'MAOI use, bipolar disorder, pregnancy',
         35.99, 'Mental Health'),
        
        ('Alprazolam', 'Benzodiazepine for anxiety and panic disorders', '0.25-1mg three times daily',
         'Drowsiness, dependence, memory problems', 'Respiratory depression, pregnancy, alcohol use',
         32.99, 'Mental Health'),
        
        # Skin
        ('Hydrocortisone', 'Topical corticosteroid for skin inflammation', 'Apply 1-2 times daily to affected area',
         'Skin thinning, stretch marks, local irritation', 'Fungal infections, open wounds, face use',
         8.99, 'Dermatology'),
        
        ('Benzoyl Peroxide', 'Topical medication for acne treatment', 'Apply 1-2 times daily to affected areas',
         'Skin irritation, dryness, bleaching of clothes', 'Sensitive skin, pregnancy, breastfeeding',
         9.99, 'Dermatology'),
        
        # Vitamins and Supplements
        ('Vitamin D3', 'Essential vitamin for bone health and immune function', '1000-4000 IU daily',
         'Nausea, kidney stones (high doses)', 'Hypercalcemia, kidney disease',
         14.99, 'Vitamins'),
        
        ('Omega-3 Fish Oil', 'Essential fatty acids for heart and brain health', '1000-2000mg daily',
         'Fishy burps, diarrhea, bleeding risk', 'Bleeding disorders, fish allergies',
         19.99, 'Supplements'),
        
        ('Probiotics', 'Beneficial bacteria for gut health', '1-2 capsules daily with meals',
         'Mild bloating, gas, diarrhea initially', 'Severe immune deficiency, acute pancreatitis',
         16.99, 'Supplements'),
        
        # Sleep and Relaxation
        ('Melatonin', 'Natural sleep hormone for insomnia', '1-5mg 30 minutes before bedtime',
         'Drowsiness, vivid dreams, morning grogginess', 'Pregnancy, autoimmune disorders',
         11.99, 'Sleep'),
        
        ('Valerian Root', 'Natural herb for sleep and anxiety', '300-600mg 30 minutes before bedtime',
         'Drowsiness, vivid dreams, liver problems', 'Liver disease, pregnancy, driving',
         13.99, 'Natural Remedies'),
        
        # Cough and Cold
        ('Dextromethorphan', 'Cough suppressant for dry cough', '15-30mg every 4-6 hours',
         'Drowsiness, dizziness, nausea', 'MAOI use, chronic cough, asthma',
         6.99, 'Cough & Cold'),
        
        ('Guaifenesin', 'Expectorant to loosen chest congestion', '200-400mg every 4 hours',
         'Nausea, vomiting, dizziness', 'Severe kidney disease, pregnancy',
         7.99, 'Cough & Cold'),
        
        # Allergy
        ('Cetirizine', 'Antihistamine for allergy relief', '10mg once daily',
         'Drowsiness, dry mouth, headache', 'Kidney disease, pregnancy, driving',
         10.99, 'Allergy'),
        
        ('Loratadine', 'Non-drowsy antihistamine for allergies', '10mg once daily',
         'Headache, dry mouth, fatigue', 'Liver disease, pregnancy, children under 2',
         12.99, 'Allergy'),
        
        # Women's Health
        ('Folic Acid', 'Essential B vitamin for pregnancy and cell growth', '400-800mcg daily',
         'Nausea, bitter taste, allergic reactions', 'Vitamin B12 deficiency, cancer',
         8.99, 'Women\'s Health'),
        
        ('Iron Supplement', 'Mineral supplement for iron deficiency anemia', '65-200mg daily with vitamin C',
         'Constipation, black stools, stomach upset', 'Hemochromatosis, thalassemia',
         11.99, 'Supplements'),
        
        # Men's Health
        ('Saw Palmetto', 'Natural supplement for prostate health', '160-320mg daily',
         'Stomach upset, headache, decreased libido', 'Pregnancy, hormone-sensitive conditions',
         17.99, 'Men\'s Health'),
        
        # Eye Health
        ('Lutein', 'Carotenoid for eye health and macular degeneration', '10-20mg daily',
         'Yellow skin discoloration, stomach upset', 'Pregnancy, breastfeeding',
         15.99, 'Eye Health'),
        
        # Bone Health
        ('Calcium Carbonate', 'Mineral supplement for bone health', '500-1000mg daily with vitamin D',
         'Constipation, gas, kidney stones', 'Hypercalcemia, kidney stones',
         9.99, 'Bone Health'),
        
        ('Glucosamine', 'Natural compound for joint health and arthritis', '1500mg daily',
         'Stomach upset, headache, allergic reactions', 'Shellfish allergy, diabetes, pregnancy',
         21.99, 'Joint Health')
    ]
    
    cursor.executemany('''
        INSERT INTO medicines (name, description, dosage, side_effects, contraindications, price, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', medicines_data)
    
    print(f"Added {len(medicines_data)} medicines to database")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("\n🎉 Database enhancement completed successfully!")
    print(f"📊 Enhanced database now contains:")
    print(f"   • {len(symptoms_data)} medical conditions with comprehensive symptoms")
    print(f"   • {len(medicines_data)} medicines with detailed information")
    print(f"   • Extensive Ayurvedic remedies for each condition")
    print(f"   • Severity levels and detailed precautions")
    print(f"   • Price information and categorized medicines")
    print(f"   • Dosage instructions and contraindications")
    
    print("\n🔧 Next Steps:")
    print("1. Run 'python app.py' to start the application")
    print("2. Test the enhanced symptom diagnosis with various conditions")
    print("3. Explore the comprehensive medicine database")
    print("4. Check the detailed Ayurvedic remedies")
    print("5. Verify the severity levels and precautions")

if __name__ == '__main__':
    enhance_database() 
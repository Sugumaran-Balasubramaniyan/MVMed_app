import streamlit as st

medications = {
    "Zinnat": {
        "Related Medications": ["Cefzil", "Ceclor", "Rocephin"],
        "Common Uses": "Antibiotic for bacterial infections, such as respiratory infections, skin infections"
    },
    "Beyfortus": {
        "Related Medications": ["Amoxicillin", "Ampicillin", "Augmentin"],
        "Common Uses": "Acute Bronchiolitis, affecting up to 30% of babies below 2year-old during the wither and raising to respiratory detress, with cases of death, Antibiotic for bacterial infections, such as respiratory infections, ear infections, urinary tract infections"
    },
    "Actilyse": {
        "Related Medications": ["Ciprofloxacin"],
        "Common Uses": "Thrombolytic agent used to dissolve blood clots in heart attack, stroke, pulmonary embolism"
    },
    "Ciprofloxacin": {
        "Related Medications": ["Levofloxacin", "Ofloxacin", "Moxifloxacin"],
        "Common Uses": "Acute Respiratory Infection, Antibiotic for bacterial infections, such as urinary tract infections, respiratory infections, skin infections"
    },
    "Zophren": {
        "Related Medications": ["Ondansetron", "Metoclopramide", "Domperidone"],
        "Common Uses": "Anti-nausea medication used for chemotherapy-induced nausea, post-operative nausea"
    },
    "Ramipril": {
        "Related Medications": ["Enalapril", "Lisinopril", "Losartan"],
        "Common Uses": "Cardiac Insufficiency, Angiotensin-converting enzyme (ACE) inhibitor used for high blood pressure, heart failure, diabetic kidney disease"
    },
    "Hydrochlorothiazid": {
        "Related Medications": ["Chlorthalidone", "Indapamide", "Hydrochlorothiazide/Lisinopril"],
        "Common Uses": "Cardiac Insufficiency, Diuretic used for high blood pressure, edema (fluid retention)"
    },
    "Bisoprolol": {
        "Related Medications": ["Metoprolol", "Atenolol", "Carvedilol"],
        "Common Uses": "Cardiac Insufficiency, Beta-blocker used for high blood pressure, heart failure, angina (chest pain)"
    },
    "Digoxine": {
        "Related Medications": ["Digitoxin", "Dobutamine", "Milrinone"],
        "Common Uses": "Cardiac Insufficiency , Cardiac glycoside used for heart failure, atrial fibrillation"
    },
    "Fluindione": {
        "Related Medications": ["Warfarin", "Dabigatran", "Rivaroxaban"],
        "Common Uses": "Cardiac Insufficiency, Anticoagulant (blood thinner) used for preventing blood clots, stroke prevention in atrial fibrillation"
    },
    "Hycamtin": {
        "Related Medications": ["Topotecan", "Etoposide", "Cisplatin"],
        "Common Uses": "Chemotherapy medication used for small cell lung cancer, ovarian cancer"
    },
    "Tofranil": {
        "Related Medications": ["Amitriptyline", "Nortriptyline", "Imipramine"],
        "Common Uses": "Tricyclic antidepressant used for depression, enuresis (bedwetting)"
    },
    "Rimactan": {
        "Related Medications": ["Isoniazid", "Pyrazinamide", "Ethambutol"],
        "Common Uses": "Antibiotic used to treat tuberculosis and other bacterial infections"
    }
}



# Function to display related medications and common uses
def display_info(medication):
    if medication in medications:
        related_medications = medications[medication]["Related Medications"]
        common_uses = medications[medication]["Common Uses"]
        st.write(f"**Related Medications**: {', '.join(related_medications)}")
        st.write(f"**Common Uses**: {common_uses}")
    else:
        return "Medication not found in database."
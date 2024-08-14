#CARECONNECT : A PROJECT THAT PROVIDES MEDICAL ASSISTANCE THROUGH A 24/7 WORKING CHATBOT AND HELPS FIND HOSPITALS, 
#PHARMACIES, GOVERNMENT HOSPITALS, MULTI-SPECIALITY HOSPITALS AND DETECT THEIR LOCATION IN MAPS.

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import requests
import logging
import mysql.connector
import pandas as pd
import re, os
import nltk
from sentence_transformers import SentenceTransformer, util
from flask_session import Session


app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6'

# OpenCage API Key
API_KEY = 'e8b7187e67314da6807f41b07b566742'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="system",
        database="testdb"
    )

def initialize_database():
    csv_file_path = r'C:\Users\Bevina R\OneDrive\Desktop\hospital\HospitalsInIndia.csv'
    
    data = pd.read_csv(csv_file_path, index_col=0)

    mydb = get_db_connection()
    cursor = mydb.cursor()

    cursor.execute("DESCRIBE hospitals") #testing
    result = cursor.fetchall()

    cursor.execute("DROP TABLE IF EXISTS hospitals")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Hospital VARCHAR(255),
    State VARCHAR(255),
    City VARCHAR(255),
    LocalAddress TEXT,
    Pincode VARCHAR(20)
)
    """)
    for index, row in data.iterrows():
        sql = """
        INSERT INTO hospitals 
        (Hospital, State, City, LocalAddress, Pincode) 
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (row['Hospital'], row['State'], row['City'], row['LocalAddress'], row['Pincode'])
        try:
            cursor.execute(sql, values)
        except mysql.connector.Error as err:
            print(f"Error inserting row {index}: {err}")
    
    mydb.commit()
    cursor.close()
    mydb.close()

@app.route('/display_data')
def display_data():
    mydb = get_db_connection()
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM hospitals")
    result = cursor.fetchall()

    cursor.close()
    mydb.close()

    return render_template('display.html', data=result)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        phone = request.form['phone']
        return redirect(url_for('appointment_details', first_name=first_name, last_name=last_name, address=address, phone=phone))
    return render_template('index.html')

@app.route('/appointment-details', methods=['GET', 'POST'])
def appointment_details():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        phone = request.form['phone']
        return render_template('listofhosp.html', first_name=first_name, last_name=last_name)
    
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    address = request.args.get('address')
    phone = request.args.get('phone')
    
    return render_template('appointment.html', first_name=first_name, last_name=last_name, address=address, phone=phone)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/listofhosp')
def listofhosp():
    return render_template('listofhosp.html')

def get_district_from_address(address, api_key):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={requests.utils.quote(address)}&key={api_key}&limit=1'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        
        if data['results']:
            components = data['results'][0]['components']
            district = components.get('district') or \
                       components.get('suburb') or \
                       components.get('neighbourhood') or \
                       components.get('city') or \
                       components.get('town') or \
                       'District not found'
            return district
        else:
            return "No results found."
    except requests.RequestException as e:
        logging.error(f"Request error: {str(e)}")
        return f"Error: {str(e)}"
    
@app.route('/find_district', methods=['POST'])
def find_district():
    address = request.form.get('address')
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    district = get_district_from_address(address, API_KEY)
    logging.debug(f"District: {district}")  
    return jsonify({'district': district})

@app.route('/save_district', methods=['POST'])
def save_district():
    address = request.form.get('address')
    district = request.form.get('district')
    if not address or not district:
        return jsonify({'error': 'Address and district are required'}), 400
    
    logging.debug(f"Received Address: {address}")
    logging.debug(f"Received District: {district}")

    return jsonify({'message': 'District saved successfully'})

@app.route('/lab_test')
def lab_test():
    return render_template('lab_test.html')

@app.route('/govn_hospitals')
def govn_hospitals():
    return render_template('govn_hospitals.html')

@app.route('/ms_hospitals')
def ms_hospitals():
    return render_template('ms_hospitals.html')

# Chatbot configurations
model = SentenceTransformer('all-MiniLM-L6-v2')
csv_file_path = os.path.join('data', 'preprocessed_ai_medical_chatbot_dataset.csv')
df_train = pd.read_csv(csv_file_path)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text) 
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text) 
    tokens = text.split()  
    stopwords_set = set(nltk.corpus.stopwords.words('english'))
    tokens = [word for word in tokens if word not in stopwords_set] 
    return ' '.join(tokens)

intents = {}
for index, row in df_train.iterrows():
    cleaned_input = row['Cleaned_Patient']
    ai_response = row['Doctor']
    intents[cleaned_input] = ai_response

intent_embeddings = {phrase: model.encode(phrase) for phrase in intents.keys()}

def get_intent(user_input):
    user_input_cleaned = preprocess_text(user_input)
    user_input_embedding = model.encode(user_input_cleaned)
    similarities = {phrase: util.pytorch_cos_sim(user_input_embedding, emb).item() for phrase, emb in intent_embeddings.items()}
    best_match = max(similarities, key=similarities.get)
    if similarities[best_match] > 0.5:
        return intents[best_match]
    return "Sorry, I couldn't understand your question. Please try again."

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'conversation_history' not in session:
        session['conversation_history'] = []

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            response = get_intent(user_input)
            session['conversation_history'].append({'type': 'user', 'text': user_input})
            session['conversation_history'].append({'type': 'bot', 'text': response})
            return jsonify({'user_input': user_input, 'response': response})

    conversation_history = session['conversation_history']
    return render_template('chat.html', messages=conversation_history)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
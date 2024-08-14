import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from tqdm import tqdm

nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    stopwords_set = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stopwords_set]
    return ' '.join(tokens)

def preprocess(input_file, output_file):
    chunk_size = 10000
    preprocessed_conversations = []

    for chunk in tqdm(pd.read_csv(input_file, chunksize=chunk_size)):
        chunk['Cleaned_Patient'] = chunk['Patient'].apply(preprocess_text)
        preprocessed_conversations.append(chunk)

    df_preprocessed = pd.concat(preprocessed_conversations, ignore_index=True)
    df_preprocessed.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")

input_file= r"C:\Users\username\OneDrive\Desktop\chatbot\test2\ai_medical_chatbot_dataset.csv" 
preprocessed_csv_path = 'preprocessed_ai_medical_chatbot_dataset.csv'

preprocess(input_file, preprocessed_csv_path)

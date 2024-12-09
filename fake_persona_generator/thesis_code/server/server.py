from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
from GeneratorCTGAN import generateWithCTGAN
from talkToChat import generateEmailsViaChatGPT
import pandas as pd

app = Flask(__name__)
CORS(app)
user_db = {}
with open("server//user.json", "r+") as user_file:
    user_db = json.loads(user_file.read())
user_file.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    username = data.get('user_name')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    for user in user_db:
        if user.get('user_name') == data.get("user_name"):
            return jsonify({"error": "username already taken"}), 400

    user_db.append({
        "user_name": username,
        "password": password
    })

    with open("server//user.json", "w+") as user_file:
        user_file.write(json.dumps(user_db))
    user_file.close()

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()

    if not credentials:
        return jsonify({"error": "Bad request"}), 400

    user_name = credentials.get('user_name')
    password = credentials.get('password')

    print(user_name)
    print(password)
    for user in user_db:
        if user.get('user_name') == user_name:
            if user.get("password") == password:
                    return jsonify({
                        "message": "Data received successfully",
                        "received_data": {
                            "session_id": uuid.uuid4(),
                        }
                    }), 200
            
            return jsonify({"error": "Invalid username or password"}), 401 
        
    return jsonify({"error": "Invalid username or password"}), 401


@app.route('/generate', methods=['POST'])
def generate():
    generationDetails = request.get_json()

    if not generationDetails:
        return jsonify({"error": "Bad request"}), 400

    print(generationDetails)
    gender_input = generationDetails.get('gender').split(' ')[-1]
    if gender_input == "Płeć" or gender_input == "Wszyscy":
        gender = None
    elif gender_input == "Mężczyźni":
        gender = "Mężczyzna"
    else:
        gender = "Kobieta"
    email_domain = generationDetails.get('emailDomain')
    sample_count = int(generationDetails.get('sampleCount'))

    print(gender, email_domain, int(sample_count))

    data = generateWithCTGAN(sample_count)

    print(len(data))

    email_addresses = []
    # tutaj jeśli jest token w pliku talkToChat.py
    talkToChat = False
    
    if talkToChat:
        if email_domain is None or email_domain == "":
            names_list = []
            for index, row in data.iterrows():
                names_list.append(row["Imię"] + " " + row["Nazwisko"])
                email_addresses = generateEmailsViaChatGPT(names_list)
        else:
            for index, row in data.iterrows():
                email_addresses.append(row["Imię"] + "." + row["Nazwisko"]+email_domain)
    else:
        data = getPreGeneratedData(gender=gender, sample_count=sample_count)
        if email_domain is None or email_domain == "":
            for index, row in data.iterrows():
                email_addresses = data['Email'].tolist()
        else:
            for index, row in data.iterrows():
                email_addresses.append(row["Imię"] + "." + row["Nazwisko"]+email_domain)
            
    dict_representation = {
        "Imie": data["Imię"].tolist(),
        "Nazwisko": data["Nazwisko"].tolist(),
        "Stanowisko": data["Stanowisko *"].tolist(),
        "Wiek": data["Wiek *"].tolist(),
        "Plec": data["Płeć"].tolist(),
        "Email": email_addresses,
    }

    
    return jsonify(dict_representation)


def getPreGeneratedData(gender, sample_count):
    df = pd.read_csv("server/PreGeneratedFinal.csv")
    df = df.sample(frac=1).reset_index(drop=True)
    print(gender)
    if gender is not None:
        df = df[df["Płeć"] == gender]
    
    return df.head(sample_count)
    
    
if __name__ == '__main__':
    app.run(debug=True)
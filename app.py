import openai
import sqlite3
import speech_recognition as sr
from flask import Flask, request, jsonify, render_template

# Initialize Flask App
app = Flask(__name__)

# Load API Key (Set your OpenAI key in environment variables before running)
openai.api_key = "your-openai-api-key"

# Create SQLite Database
def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, order_text TEXT)")
    conn.commit()
    conn.close()

create_database()

# AI-based Recommendation System
def ai_recommendation():
    prompt = "Suggest a popular dish for a customer in an Indian restaurant."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a restaurant assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Route to Get AI-Based Recommendations
@app.route("/recommend", methods=["GET"])
def recommend():
    dish = ai_recommendation()
    return jsonify({"recommended_dish": dish})

# Voice-Based Ordering System
@app.route("/voice_order", methods=["POST"])
def voice_order():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for an order...")
        audio = recognizer.listen(source)
    try:
        order_text = recognizer.recognize_google(audio)
        # Store the order in the database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (order_text) VALUES (?)", (order_text,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Order received", "order": order_text})
    except Exception as e:
        return jsonify({"error": str(e)})

# Serve Web UI
@app.route("/")
def home():
    return render_template("index.html")

# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)


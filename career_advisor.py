import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request
import re

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)

def get_career_advice(interests, skills):
    prompt = (
        f"I'm interested in: {interests}. "
        f"My current skills are: {skills}. "
        "Based on this, suggest 2-3 suitable career paths and give practical next learning steps for each. "
        "Format your response with markdown (using ** for bold, - for bullet points, etc.) "
        "as it will be displayed on a webpage with markdown rendering."
    )

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(GROQ_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        data = response.json()
        advice = data['choices'][0]['message']['content']
        # Escape backslashes and double quotes for JavaScript
        advice = advice.replace('\\', '\\\\').replace('"', '\\"')
        # Replace backticks with HTML entities to avoid conflicts with JavaScript template literals
        advice = advice.replace('`', '&#96;')
        return advice
    else:
        print("Error:", response.status_code)
        print("Details:", response.text)
        return "Sorry, something went wrong. Please try again."

@app.route('/', methods=['GET', 'POST'])
def index():
    advice = None
    interests = ""
    skills = ""
    
    if request.method == 'POST':
        interests = request.form.get('interests', '')
        skills = request.form.get('skills', '')
        
        if interests and skills:
            advice = get_career_advice(interests, skills)
    
    return render_template('index.html', 
                          interests=interests, 
                          skills=skills, 
                          advice=advice)

if __name__ == '__main__':
    app.run(debug=True)
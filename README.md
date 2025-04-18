# 🚀 PathPilot – Your AI Career Advisor

PathPilot is an AI-powered career guidance web app built with Flask. Users can input their interests and skills, and receive personalized career paths and practical learning steps using the [GROQ API](https://console.groq.com/).

---

## 🧠 Features

- Simple web UI to enter your interests and skills
- Uses the Mixtral model via GROQ API to generate intelligent career suggestions
- Clean and responsive interface (basic HTML + CSS)
- Easy to deploy locally or on cloud platforms

---

## 🖼️ Preview

![screenshot](preview.png) <!-- Add a screenshot here -->

---

## 🛠️ Tech Stack

- Backend: Python + Flask
- AI: GROQ API (`mixtral-8x7b-32768` model)
- Frontend: HTML5 + CSS3
- Environment Variables: Python-dotenv

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/sah1l-17/PathPilot.git
cd PathPilot
```
### 2. Set up the virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Set up environment variables

 - Create a .env file in the root directory:
```bash
GROQ_API_KEY=sk-your-groq-key-here
```

### 🚀 Running the App

```bash
python app.py
```

 - Visit: http://127.0.0.1:5000

🧪 Example Prompt
Input

Interests: "Technology, Creativity"

Skills: "Python, HTML, UI Design"

Output

🎯 Career Path 1: UX Engineer
📚 Learn: Frontend frameworks, HCI

🎯 Career Path 2: Technical Product Manager
📚 Learn: Agile, Roadmapping, Team Leadership

🤖 Powered By
GROQ API

📄 License
MIT License © 2025 Sahil Ansari

### ✅ Git Push Commands

> Run these from your terminal in the project folder:

#### 1. Initialize Git (if not done yet)
```bash
git init
```
### 2. Create .gitignore file

Create a .gitignore file:

``` bash
venv/
__pycache__/
.env
*.pyc
```
### 3. Add & Commit
```bash
git add .
git commit -m "Initial commit: AI Career Advisor (PathPilot)"
```

### 4. Create GitHub Repo

Go to: https://github.com/new
Repo name: PathPilot

### 5. Add Remote & Push
```bash
git remote add origin https://github.com/yourusername/PathPilot.git
git branch -M main
git push -u origin main
```

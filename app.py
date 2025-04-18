from flask import Flask, render_template, request
from career_advisor import get_career_advice

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    career_advice = None
    interests = skills = ""

    if request.method == "POST":
        interests = request.form.get("interests")
        skills = request.form.get("skills")
        if interests and skills:
            career_advice = get_career_advice(interests, skills)

    return render_template("index.html", advice=career_advice, interests=interests, skills=skills)

if __name__ == "__main__":
    app.run(debug=True)

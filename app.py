from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)
app.config["salasar_balaji"] = os.getenv("salasar_balaji")

# Load the model
pipe = joblib.load(open("pipe(1).joblib", "rb"))

teams = [
    "Mumbai Indians", "Rajasthan Royals", "Royal Challengers Bangalore",
    "Sunrisers Hyderabad", "Kings XI Punjab", "Kolkata Knight Riders",
    "Delhi Capitals", "Gujarat Titans", "Lucknow Super Giants", "Chennai Super Kings"
]

venues = [
    "Eden Gardens", "Wankhede Stadium", "Arun Jaitley Stadium, Delhi",
    "Dr DY Patil Sports Academy", "Rajiv Gandhi International Stadium, Hydrabad",
    "M Chinnaswamy Stadium , Bangalore", "MA Chidambaram Stadium, Chepauk, Chennai",
    "Feroz Shah Kotla ,Delhi", "Dubai International Cricket Stadium",
    "Sawai Mansingh Stadium , Jaipur", "Punjab Cricket Association Stadium, Mohali",
    "Sharjah Cricket Stadium", "Narendra Modi Stadium, Ahmedabad",
    "Brabourne Stadium, Mumbai", "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "Himachal Pradesh Cricket Association Stadium ,Dharamshala",
    "ACA Cricket Stadium , Guwahati", "Maharaja Yadavindra singh Cricket Stadium , New Chandigarh"
]


@app.route('/', methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        bat_team = request.form["bat_team"]
        bowl_team = request.form["bowl_team"]
        venue = request.form["venue"]
        current_score = int(request.form["current_score"])
        overs = float(request.form["over"])
        wickets = int(request.form["wicket"])
        last_five = int(request.form["last_five"])  # ✅ FIXED: used string instead of variable

        balls_left = 120 - (overs * 6)
        wicket_left = 10 - wickets
        current_run_rate = current_score / overs

        input_df = pd.DataFrame({
            "bat_team": [bat_team],
            "bowl_team": [bowl_team],
            "venue": [venue],
            "current_score": [current_score],
            "balls_left": [balls_left],
            "wicket_left": [wicket_left],
            "current_run_rate": [current_run_rate],
            "last_five": [last_five]
        })

        result = pipe.predict(input_df)
        prediction = int(result[0])

    # ✅ FIXED: removed extra space from 'index.html '
    return render_template('index.html', teams=sorted(teams), venue=sorted(venues), prediction=prediction)


# ✅ FIXED: should be "__name__ == '__main__'"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

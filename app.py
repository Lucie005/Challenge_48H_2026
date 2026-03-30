from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from chatbox import ask_ai
from icalendar import Calendar
import requests
from datetime import datetime

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message.strip():
        return jsonify({"reply": "Message vide."}), 400

    reply = ask_ai(user_message)
    return jsonify({"reply": reply})


@app.route("/load_edt", methods=["POST"])
def load_edt():
    data = request.get_json()
    ical_url = data.get("ical_url", "").strip()

    if not ical_url:
        return jsonify({"error": "Lien iCal manquant."}), 400

    try:
        response = requests.get(ical_url, timeout=10)
        response.raise_for_status()

        cal = Calendar.from_ical(response.content)
        events = []

        for component in cal.walk():
            if component.name == "VEVENT":
                summary = str(component.get("summary", "Sans titre"))
                location = str(component.get("location", ""))
                description = str(component.get("description", ""))

                dtstart = component.get("dtstart")
                dtend = component.get("dtend")

                start = dtstart.dt if dtstart else None
                end = dtend.dt if dtend else None

                events.append({
                    "summary": summary,
                    "location": location,
                    "description": description,
                    "start": str(start),
                    "end": str(end)
                })

        events.sort(key=lambda e: e["start"])
        return jsonify({"events": events})

    except requests.RequestException:
        return jsonify({"error": "Impossible de télécharger le fichier iCal."}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur lecture iCal : {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
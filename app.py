from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- RESCUE CASE ----------------
@app.route("/rescue")
def rescue():
    return render_template("rescue_case.html")


@app.route("/save_case", methods=["POST"])
def save_case():

    animal = request.form["animal"]
    location = request.form["location"]

    photo = request.files["photo"]
    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
    photo.save(photo_path)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO rescue_cases(animal,location,photo) VALUES (?,?,?)",
        (animal, location, photo.filename)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM rescue_cases")
    cases = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", cases=cases)


# ---------------- DOCTORS ----------------
@app.route("/doctors")
def doctors():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()

    conn.close()

    return render_template("doctors.html", doctors=doctors)


# ---------------- MEDICAL RECORD ----------------
@app.route("/medical")
def medical():
    return render_template("medical.html")


@app.route("/save_medical", methods=["POST"])
def save_medical():

    case_id = request.form["case_id"]
    diagnosis = request.form["diagnosis"]
    treatment = request.form["treatment"]
    doctor = request.form["doctor"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO medical_records(case_id,diagnosis,treatment,doctor) VALUES (?,?,?,?)",
        (case_id, diagnosis, treatment, doctor)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- EMERGENCY ALERT ----------------
@app.route("/emergency")
def emergency():
    return render_template("emergency.html")


@app.route("/send_alert", methods=["POST"])
def send_alert():

    location = request.form["location"]
    description = request.form["description"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO emergency_alerts(location,description,status) VALUES (?,?,?)",
        (location, description, "Pending")
    )

    conn.commit()
    conn.close()

    return "Emergency Alert Sent"


# ---------------- AMBULANCE ROUTE ----------------
@app.route("/route/<location>")
def route(location):

    map_link = "https://www.google.com/maps/search/" + location

    return render_template("route.html", link=map_link)


# ---------------- INVENTORY ----------------
@app.route("/inventory")
def inventory():
    return render_template("inventory.html")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
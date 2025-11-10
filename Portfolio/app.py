from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret"

# --- Project data (derived from your resume) ---
PROJECTS = [
    {
        "title": "Smart Content Integrity System",
        "tech": "Python, TF-IDF, Cosine Similarity, Google Search API",
        "summary": "Plagiarism detection system for text, PDF, and code formats using NLP similarity techniques.",
        "more": "Implemented multi-format parsing, pre-processing and similarity scoring. Built a small UI for uploading and viewing results."
    },
    {
        "title": "Business Sales Dashboard from E-Commerce Data",
        "tech": "Power BI, Excel, Data Cleaning, Visualization",
        "summary": "Analyzed multi-country e-commerce data (2009–2011) to surface trends in sales and quantities.",
        "more": "Designed interactive visuals to explore product-level trends and revenue metrics."
    },
    {
        "title": "Facebook Ad Campaign Dashboard",
        "tech": "Power BI, Excel, Marketing Analytics",
        "summary": "Interactive dashboard analyzing impressions, clicks, conversions, and ad spend across demographics.",
        "more": "Visualized campaign reach and conversion metrics; provided audience-level insights."
    },
    {
        "title": "Conversation Flow Visualization for Chatbots",
        "tech": "Python, Matplotlib",
        "summary": "Tracked and visualized conversation trees to help debug and improve chatbot flows.",
        "more": "Constructed graph structures for conversation sequences and plotted them for analysis."
    },
    {
        "title": "Digital Clock with Temp & Humidity Sensor",
        "tech": "Microcontroller, LCD",
        "summary": "Real-time monitoring system with threshold alerts, UI, and serial display integration.",
        "more": "Integrated sensor readings onto a display with user-configurable thresholds."
    }
]

# --- Home route ---
@app.route("/")
def index():
    gallery_folder = os.path.join(app.static_folder, "images", "gallery")
    gallery_images = []

    if os.path.exists(gallery_folder):
        for filename in os.listdir(gallery_folder):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                # only store relative path after "static/"
                gallery_images.append(f"images/gallery/{filename}")

    gallery_images.sort()
    return render_template("index.html", projects=PROJECTS, gallery_images=gallery_images)

# --- Resume route (download) ---
@app.route("/resume")
def resume():
    resume_dir = os.path.join(app.static_folder, "resume")
    return send_from_directory(resume_dir, "Resume.pdf", as_attachment=True)

# --- Serve embedded resume file (for iframe) ---
@app.route("/static/resume/<path:filename>")
def resume_static(filename):
    return send_from_directory(os.path.join(app.static_folder, "resume"), filename)

# --- Contact form route ---
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to CSV (contacts.csv in project root)
    csv_path = os.path.join(os.path.dirname(__file__), "contacts.csv")
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "name", "email", "message"])
        writer.writerow([ts, name, email, message])

    # Optionally, you could also send an email here (configure SMTP)
    flash("Thanks — your message has been sent!")
    return redirect(url_for("index", msg="Thanks for reaching out!"))

# --- run ---
if __name__ == "__main__":
    app.run(debug=True)

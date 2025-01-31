from flask import Flask, request, jsonify, render_template, send_file
from pymisp import PyMISP
import os
import json
import psycopg2
from fpdf import FPDF

app = Flask(__name__, template_folder='templates', static_folder='static')

# MISP Configuration
MISP_URL = "https://misp-instance-url.com"
MISP_API_KEY = "your_misp_api_key"
misp = PyMISP(MISP_URL, MISP_API_KEY, False)

def test_misp_connection():
    try:
        misp.get_version()
        return True
    except Exception as e:
        print(f"MISP Connection Error: {e}")
        return False

# Database Configuration
DB_HOST = "localhost"
DB_NAME = "cyber_risk"
DB_USER = "user"
DB_PASS = "password"

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cursor = conn.cursor()

# Create Table
cursor.execute('''CREATE TABLE IF NOT EXISTS risks (
                    id SERIAL PRIMARY KEY,
                    risk_name TEXT,
                    likelihood INTEGER,
                    impact INTEGER,
                    threat_data JSONB
                )''')
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test-misp', methods=['GET'])
def test_misp():
    if test_misp_connection():
        return jsonify({"message": "MISP connection successful"})
    return jsonify({"error": "MISP connection failed"})

@app.route('/fetch-threats', methods=['GET'])
def fetch_threats():
    try:
        events = misp.search(controller='events', return_format='json')
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/add-risk', methods=['POST'])
def add_risk():
    data = request.json
    cursor.execute("INSERT INTO risks (risk_name, likelihood, impact, threat_data) VALUES (%s, %s, %s, %s)",
                   (data['risk_name'], data['likelihood'], data['impact'], json.dumps(data['threat_data'])))
    conn.commit()
    return jsonify({"message": "Risk added successfully"})

@app.route('/get-risks', methods=['GET'])
def get_risks():
    cursor.execute("SELECT * FROM risks")
    risks = cursor.fetchall()
    return jsonify(risks)

@app.route('/export-report', methods=['GET'])
def export_report():
    cursor.execute("SELECT * FROM risks")
    risks = cursor.fetchall()
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Cyber Risk Assessment Report", ln=True, align='C')
    
    for risk in risks:
        pdf.cell(200, 10, f"Risk: {risk[1]} - Likelihood: {risk[2]} - Impact: {risk[3]}", ln=True)
    
    pdf_filename = "cyber_risk_report.pdf"
    pdf.output(pdf_filename)
    return send_file(pdf_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

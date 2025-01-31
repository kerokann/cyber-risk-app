# **Cybersecurity Risk Assessment System Documentation**

### **Student Name**
- **Anastasya Selena Anandita Adnan** 001202300148
- **Indrasworo Suryo Prayogo** 001202300147

## **Project Overview**

The **Cybersecurity Risk Assessment System** is designed to help organizations assess, identify, and manage cybersecurity risks. The system integrates with the **Malware Information Sharing Platform (MISP)** to fetch real-time threat intelligence, which is used to enhance risk assessment. The system leverages **OCTAVE Allegro** for conducting risk assessments and visualizes the data in an interactive dashboard.

### **Key Features**
- **Real-time Threat Intelligence Integration**: Fetches threat data from MISP to assist in risk identification.
- **Risk Assessment Dashboard**: Visualizes risk data using a bar chart for likelihood and impact.
- **Database Integration**: Stores risks and associated data in a PostgreSQL database.
- **Reporting**: Generates and exports PDF reports summarizing risk information.
- **Web Interface**: Provides an interactive web interface for users to interact with the system.

---

## **System Architecture**

The system follows a **client-server architecture** with the following components:

### 1. **Frontend (Client Side)**
- **Web UI**: Built with HTML, CSS, and JavaScript, the frontend displays the risk data in a **Chart.js** visual format (bar chart) and offers buttons to fetch threat data and view risks.
- **Static Files**: Includes the `style.css` for a soft pink theme and `script.js` to handle API calls and render visualizations.
- **User Interaction**: The user interacts with the system by fetching threat data from MISP and viewing the risk assessment results.

### 2. **Backend (Server Side)**
- **Flask Web Framework**: Handles HTTP requests and serves the frontend using templates (`index.html`).
- **MISP Integration**: The backend uses the **PyMISP** Python library to connect with MISP and fetch real-time threat intelligence.
- **Database**: The backend stores risk data in a PostgreSQL database using **psycopg2** for database interaction.
- **PDF Report Generation**: The system generates PDF reports summarizing the risk assessment using the **FPDF** library.

### 3. **Database**
- The PostgreSQL database stores risk information, including the name, likelihood, impact, and associated threat data. The database is structured to allow easy retrieval and manipulation of risk data for reporting and visualization purposes.

---

## **Database Schema**

### **Database: `cyber_risk`**
The database contains a single table named **risks** that stores the risk data.

### **Table: `risks`**

| Column Name   | Data Type   | Description                                       |
|---------------|-------------|---------------------------------------------------|
| `id`          | SERIAL      | Primary key, auto-incremented integer             |
| `risk_name`   | TEXT        | Name of the risk (e.g., "Data Breach", "Phishing")|
| `likelihood`  | INTEGER     | Likelihood score of the risk (1-5 scale)          |
| `impact`      | INTEGER     | Impact score of the risk (1-5 scale)              |
| `threat_data` | JSONB       | Threat intelligence data fetched from MISP        |

### **SQL Table Creation**

```sql
-- Create the database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS cyber_risk;

-- Connect to the database
\c cyber_risk;

-- Create the 'risks' table
CREATE TABLE IF NOT EXISTS risks (
    id SERIAL PRIMARY KEY,
    risk_name TEXT NOT NULL,
    likelihood INTEGER NOT NULL,
    impact INTEGER NOT NULL,
    threat_data JSONB
);
```

---

## **API Usage**

The backend provides the following API endpoints:

### 1. **GET /**
- **Description**: Serves the home page (`index.html`).
- **Response**: HTML page with a dashboard that allows the user to fetch threats and view risks.

### 2. **GET /test-misp**
- **Description**: Tests the connection to MISP.
- **Usage**: Used to verify that the system can connect to the MISP instance.
- **Response**: 
  - Success: `{"message": "MISP connection successful"}`
  - Failure: `{"error": "MISP connection failed"}`

### 3. **GET /fetch-threats**
- **Description**: Fetches threat data from MISP.
- **Usage**: When the user clicks the "Fetch Threats" button, this endpoint is triggered to retrieve threat information from MISP.
- **Response**: JSON containing threat data fetched from MISP (events, indicators, etc.).

### 4. **POST /add-risk**
- **Description**: Adds a new risk to the database.
- **Usage**: This endpoint allows the frontend to add risk data to the PostgreSQL database.
- **Request Payload**: 
  ```json
  {
    "risk_name": "Phishing",
    "likelihood": 4,
    "impact": 5,
    "threat_data": {
      "event_id": 123,
      "threat_type": "Phishing"
    }
  }
  ```
- **Response**: 
  ```json
  {
    "message": "Risk added successfully"
  }
  ```

### 5. **GET /get-risks**
- **Description**: Retrieves all risks from the database.
- **Usage**: This endpoint fetches all the stored risks from the PostgreSQL database to display them on the frontend.
- **Response**: JSON array of risks:
  ```json
  [
    [1, "Phishing", 4, 5, {"event_id": 123, "threat_type": "Phishing"}],
    [2, "Data Breach", 3, 4, {"event_id": 124, "threat_type": "Data Breach"}]
  ]
  ```

### 6. **GET /export-report**
- **Description**: Generates and exports a PDF report containing all risks stored in the database.
- **Usage**: When the user clicks the "Export Report" button, a PDF report is generated and sent as a downloadable file.
- **Response**: A PDF file (`cyber_risk_report.pdf`) containing a summary of the risks.

---

## **Running the Project**

1. **Clone the Repository**:
   - Clone the project repository to your local machine using `git clone`.

2. **Install Dependencies**:
   - Create a virtual environment and install the necessary dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Setup the Database**:
   - Run `database.sql` to set up the PostgreSQL database and the `risks` table.

4. **Configure MISP**:
   - Replace `MISP_URL` and `MISP_API_KEY` in `app.py` with your MISP instance URL and API key.

5. **Run the Flask Application**:
   - Start the Flask application by running:
     ```bash
     python app.py
     ```
   - The app will run on `http://localhost:5000/`.

6. **Access the Web Interface**:
   - Open a browser and navigate to `http://localhost:5000/` to access the dashboard.

---

## **Conclusion**

This Cybersecurity Risk Assessment System provides a robust way to assess and manage cybersecurity risks by leveraging real-time threat intelligence from MISP. It uses a web-based dashboard for user interaction and integrates with a PostgreSQL database for storing and querying risk data. The system also supports generating PDF reports for risk analysis.

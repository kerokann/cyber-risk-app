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

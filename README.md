Autonomous Data Cleaner & Schema Understanding Agent

An automated data-cleaning system that detects schema issues, generates cleaning rules, and produces fully cleaned datasets through a Streamlit interface.

Upload any CSV → the system analyzes it → suggests required fixes → applies automatic cleaning.

Features
1. Schema Detection

Identifies:

Column types

Missing values

Unique value patterns

Anomalies

2. Rule Generation

Automatically suggests:

Missing-value handling

Category normalization

Date-format corrections

Outlier checks

Negative-value validation

3. Automated Data Cleaning

Performs:

Date parsing

Category standardization

Missing-value fixes

Outlier adjustments

4. Streamlit UI

Upload CSV

View raw data

Run cleaning pipeline

Download cleaned data

View schema report and rule suggestions

Project Structure
autonomous-data-cleaner/
│── data/
│── src/
│    ├── app.py
│    ├── main_clean.py
│    ├── schema_report.py
│    ├── rule_suggestions.py
│    ├── auto_cleaner.py
│
│── requirements.txt
│── README.md
Use Case

This system is ideal for:

Data engineers

Data analysts

ML teams

Anyone who wants to clean large messy datasets quickly

It removes 70% of manual cleaning work, one of the most time-consuming tasks in data science.

 Tech Stack
Python

Pandas

Streamlit

Numpy

Custom Rule-Based Engine

# Overview

As a Data Analyst, my goal for this project is to build foundational Data Engineering skills. I am moving beyond querying existing data in BI tools to programmatically provisioning cloud databases, managing secure credentials, and building backend scripts that write and manipulate data at the source.

This software is a Command Line Interface (CLI) Personal Expense Tracker. It uses a Python script to securely connect to Google Cloud Firestore and perform CRUD (Create, Read, Update, Delete) operations, simulating basic data ingestion and management workflows.

My purpose for writing this software is to gain hands-on experience with Python backend scripting, NoSQL document databases, and the Firebase Admin SDK.

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

I am using **Google Cloud Firestore**, a NoSQL document database. It is highly flexible and scalable, making it ideal for handling semi-structured data streams.

The database is structured into two related collections:
1. **`categories`**: Acts as a dimension table. Document IDs are the category names (e.g., 'food'). Fields include `category_name` (string) and `monthly_limit` (number).
2. **`expenses`**: Acts as a fact table. Documents use auto-generated IDs. Fields include `category_id` (string acting as a foreign key), `cost` (number), `description` (string), and `timestamp` (server timestamp).

# Development Environment

* Visual Studio Code (VS Code)
* Git & GitHub
* Google Cloud Platform IAM & Firebase Console

The software is written in **Python 3**. It uses the official **`firebase-admin`** library to handle secure API authentication and execute database queries.

# Useful Websites

- [Firebase Admin SDK for Python](https://firebase.google.com/docs/reference/admin/python)
- [Get Started with Cloud Firestore](https://firebase.google.com/docs/firestore/quickstart)
- [Google Cloud IAM Documentation](https://cloud.google.com/iam/docs)

# Future Work

- Build an automated pipeline to extract this NoSQL data into a structured data warehouse (like BigQuery) for analytical querying.
- Implement strict data validation logic in the Python script before records are loaded into the database.
- Write a batch processing function to ingest historical CSV expense data into Firestore.
# Digital Document Verification System

A web-based certificate verification system developed using Flask and SQLite.  
The system allows users to verify certificates using a unique Certificate ID and provides an admin interface to manage certificate records.

## Features

- Certificate verification using a unique Certificate ID
- Displays certificate details when a valid ID is entered
- Shows an invalid certificate message for unregistered IDs
- Admin login system
- Admin dashboard for managing certificate records
- Add new certificates
- Delete existing certificates
- SQLite database for storing certificate information
- Responsive and user-friendly interface

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Project Structure

```text
Digital-Document-Verification-System/
│
├── app.py
├── database.py
├── certificates.db
├── requirements.txt
├── README.md
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    ├── index.html
    ├── verify.html
    ├── result.html
    ├── admin_login.html
    └── admin_dashboard.html
    
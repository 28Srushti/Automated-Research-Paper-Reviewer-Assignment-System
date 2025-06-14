# 🧠 Automated Research Paper Reviewer Assignment System

This project is a Flask-based web application that automates the reviewer assignment process for submitted research papers using TF-IDF-based keyword matching. It also supports secure login for admins and reviewers, and sends emails with attached papers to matched reviewers.

## 🔧 Features
  🗂 Upload PDF research papers
  🔍 Extracts text and keywords from PDFs
  🤝 Matches reviewers based on their expertise using cosine similarity
  📩 Sends email with the research paper attached to matched reviewers
  🔐 Secure login system for Admins and Reviewers
  🖥️ Admin dashboard to view uploaded papers and reviewer details

## 🗃 File Structure
├── app.py               # Main application for file upload & matching
├── login.py             # Handles user login and dashboard
├── module.py            # Utility functions for keyword extraction, matching, email
├── templates/
│   ├── index.html       # Homepage for uploads
│   ├── login.html       # Login interface
│   └── admin_dashboard.html # Admin panel

## ⚙️ Installation
  1. Clone the repository:
  git clone https://github.com/yourusername/reviewer-matching-system.git
  cd reviewer-matching-system
  
  2. Create a virtual environment (optional but recommended):
  python -m venv venv
  source venv/bin/activate  # On Windows use venv\Scripts\activate
  
  3. Install required packages:
  pip install -r requirements.txt

  If requirements.txt is not present, install manually:
  pip install flask sqlalchemy werkzeug scikit-learn pymupdf

  ## 🚀 Running the App
  # For login system and database
    python login.py
  
  # In another terminal or after DB setup
    python app.py

  ## 🔐 Default Credentials (For Testing)
  You may need to add admins/reviewers directly to the review_system.db using Flask shell or SQLite browser.

  

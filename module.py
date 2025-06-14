# your_module.py

from email.mime.application import MIMEApplication
import fitz  # PyMuPDF
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

vectorizer = TfidfVectorizer(stop_words='english', max_features=10)

# Define a function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Define a function to extract keywords from text using TF-IDF
def extract_keywords(text):
    X = vectorizer.fit_transform([text])
    features = vectorizer.get_feature_names_out()
    return features

def preprocess_text(text):
    return ' '.join(text.lower().strip().split())

# Define a function to match paper keywords with reviewer expertise
def match_reviewers(keywords, reviewers):
    keywords_str = ' '.join(keywords)
    
    expertise_list = list(reviewers.values())
    expertise_list.append(keywords_str)
    
    X = vectorizer.fit_transform(expertise_list)
    
    similarity_scores = cosine_similarity(X[-1], X[:-1])
    
    matched_reviewers = []
    for index, score in enumerate(similarity_scores[0]):
        if score > 0.2:
            matched_reviewers.append(list(reviewers.keys())[index])
    
    print(f"Keywords: {keywords_str}")
    print(f"Expertise List: {expertise_list}")
    print(f"Similarity Scores: {similarity_scores}")
    print(f"Matched Reviewers: {matched_reviewers}")

    return matched_reviewers

# Define a function to send email
def send_email(to_address, subject, body, attachment_path):
    from_address = "srushtichoudhari1028@gmail.com"
    password = "ppdq vgnz biuq ggmb"  # Use environment variables or secure methods for passwords

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if os.path.isfile(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
    else:
        print(f"Attachment file not found: {attachment_path}")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_address, password)
            server.sendmail(from_address, to_address, msg.as_string())
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

# Sample data
reviewers = {
    "xyz@gmail.com": "cloud computing, data science",
    "abc@gmail.com": "computer network, edge computing",
}

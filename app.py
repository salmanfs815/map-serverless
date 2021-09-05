from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
import datetime, re

app = Flask(__name__)


@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route("/submission", methods=["POST"])
def submission():
  full_name = request.form["name"]
  email_address = request.form["email"]
  submission_type = request.form["type"]
  submission_title = request.form["title"]

  timestamp = re.sub('[:.]','-',datetime.datetime.now().isoformat())
  name_no_spaces = re.sub(r'\s+', '-', full_name.lower())
  name_alphanum = re.sub(r'[^a-zA-Z0-9-]+', '', name_no_spaces)

  submission_files = []
  for file in request.files.getlist("submission"):
    filename = f"{name_alphanum}_{timestamp}_{secure_filename(file.filename)}"
    file.save(f"uploads/{filename}")
    submission_files.append(filename)
  
  print(f"New Submission:\n\t\
    Name: {full_name}\n\t\
    Email: {email_address}\n\t\
    Type: {submission_type}\n\t\
    Title: {submission_title}\n\t\
    Files: {submission_files}")
  
  return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?success")

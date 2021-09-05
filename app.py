from flask import Flask, request, redirect
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import datetime, re

app = Flask(__name__)

# config values for testing
app.config["MAIL_SERVER"]= "smtp.mailtrap.io"
app.config["MAIL_PORT"] = 2525
app.config["MAIL_USERNAME"] = "5e98fcdb61f449"
app.config["MAIL_PASSWORD"] = "494caa4a69663f"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = "contact@bc-muslim-anthology-proj.netlify.app"

mail = Mail(app)

@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route("/submission", methods=["POST"])
def submission():
  full_name = request.form["name"]
  email_address = request.form["email"]
  submission_type = request.form["type"]
  submission_title = request.form["title"]

  timestamp = re.sub("[:.]","-",datetime.datetime.now().isoformat())
  name_no_spaces = re.sub(r"\s+", "-", full_name.lower())
  name_alphanum = re.sub(r"[^a-zA-Z0-9-]+", "", name_no_spaces)

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

@app.route("/contact", methods=["POST"])
def contact():
  name = request.form["name"]
  email = request.form["email"]
  message = f'Sent by: {name}<{email}>\n\nMessage:\n{request.form["message"]}'

  msg = Message(subject="[MAP] Contact Form Submission",
                reply_to=(name, email),
                recipients=["admin@bc-muslim-anthology-proj.ca"],
                body=message)
  mail.send(msg)

  print(f"Contact Form:\n\t\
    Name: {name}\n\t\
    Email: {email}\n\t\
    message: {message}")
  
  return redirect("https://bc-muslim-anthology-proj.netlify.app/contact-us?success")

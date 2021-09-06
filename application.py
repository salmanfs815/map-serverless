from flask import Flask, request, redirect
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

application = Flask(__name__)

# config values for testing
application.config["MAIL_SERVER"]= "smtp.mailtrap.io"
application.config["MAIL_PORT"] = 2525
application.config["MAIL_USERNAME"] = "5e98fcdb61f449"
application.config["MAIL_PASSWORD"] = "494caa4a69663f"
application.config["MAIL_USE_TLS"] = True
application.config["MAIL_USE_SSL"] = False
application.config["MAIL_DEFAULT_SENDER"] = "contact@bc-muslim-anthology-proj.netlify.app"

mail = Mail(application)

@application.route("/")
def hello_world():
  return "Hello, World!"

@application.route("/submission", methods=["POST"])
def submission():
  full_name = request.form["name"]
  email_address = request.form["email"]
  submission_type = request.form["type"]
  submission_title = request.form["title"]

  msg = Message(subject="[MAP] Anthology Submission",
                reply_to=(full_name, email_address),
                recipients=["admin@bc-muslim-anthology-proj.ca"])

  submission_files = []
  for file in request.files.getlist("submission"):
    filename = secure_filename(file.filename)
    filepath = f"uploads/{filename}"
    file.save(filepath)
    with application.open_resource(filepath) as f:
      msg.attach(filename, file.mimetype, f.read())
    submission_files.append(filename)

  message = f"New Submission:\n\n\
Name: {full_name}\n\
Email: {email_address}\n\
Type: {submission_type}\n\
Title: {submission_title}\n\
Files: {submission_files}"

  msg.body = message
  mail.send(msg)
  
  print(message)
  
  return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?success")

@application.route("/contact", methods=["POST"])
def contact():
  name = request.form["name"]
  email = request.form["email"]
  message = request.form["message"]

  msg = Message(subject="[MAP] Contact Form Submission",
                reply_to=(name, email),
                recipients=["admin@bc-muslim-anthology-proj.ca"])
  
  messageBody = f"Contact Form:\n\n\
Name: {name}\n\
Email: {email}\n\
message: {message}"
  
  msg.body = messageBody
  mail.send(msg)

  print(messageBody)
  
  return redirect("https://bc-muslim-anthology-proj.netlify.app/contact-us?success")


if __name__ == "__main__":
  application.run()

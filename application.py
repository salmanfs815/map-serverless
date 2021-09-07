from flask import Flask, request, redirect
from werkzeug.utils import secure_filename

import boto3
from botocore.exceptions import ClientError
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

application = Flask(__name__)

@application.route("/")
def hello_world():
  return "Hello, World!"

@application.route("/submission", methods=["POST"])
def submission():
  full_name = request.form["name"]
  email_address = request.form["email"]
  submission_type = request.form["type"]
  submission_title = request.form["title"]

  msg = MIMEMultipart()
  msg["Subject"] = "[MAP] Anthology Submission"
  msg["From"] = "bc-muslim-anthology-proj@protonmail.com"
  msg["To"] = "salmanf.siddiqui@gmail.com"

  submission_files = []
  for file in request.files.getlist("submission"):
    filename = secure_filename(file.filename)
    
    part = MIMEApplication(file.read())
    part.add_header("Content-Disposition",
                    "attachment",
                    filename=filename)
    msg.attach(part)

    submission_files.append(filename)

  message = f"New Submission:\n\n\
Name: {full_name}\n\
Email: {email_address}\n\
Type: {submission_type}\n\
Title: {submission_title}\n\
Files: {submission_files}"

  body = MIMEText(message, "plain")
  msg.attach(body)

  try:
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.send_raw_email(
        Source="bc-muslim-anthology-proj@protonmail.com",
        Destinations=["salmanf.siddiqui@gmail.com"],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)
  except ClientError as err:
    if "InvalidParameterValue" in str(err):
      print("ERROR sending email: message length exceeds allowed maximum (10MB)")
      return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error=maxsize")
    else:
      print("ERROR sending email:")
      print(err)
      return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error")

  print(message)
  return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?success")

@application.route("/contact", methods=["POST"])
def contact():
  name = request.form["name"]
  email = request.form["email"]
  message = request.form["message"]

  msg = MIMEMultipart()
  msg["Subject"] = "[MAP] Contact Form Submission"
  msg["From"] = "bc-muslim-anthology-proj@protonmail.com"
  msg["To"] = "salmanf.siddiqui@gmail.com"

  message = f"Contact Form:\n\n\
Name: {name}\n\
Email: {email}\n\
message: {message}"

  body = MIMEText(message, "plain")
  msg.attach(body)

  try:
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.send_raw_email(
        Source="bc-muslim-anthology-proj@protonmail.com",
        Destinations=["salmanf.siddiqui@gmail.com"],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)
  except ClientError as err:
    if "InvalidParameterValue" in str(err):
      print("ERROR sending email: message length exceeds allowed maximum (10MB)")
      return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error=maxsize")
    else:
      print("ERROR sending email:")
      print(err)
      return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error")

  print(message)
  return redirect("https://bc-muslim-anthology-proj.netlify.app/contact-us?success")


if __name__ == "__main__":
  application.run()

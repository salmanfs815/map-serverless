from flask import Flask, request, redirect
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

# import boto3
# from botocore.exceptions import ClientError
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.application import MIMEApplication
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

application = Flask(__name__)

# config values for testing
application.config['MAIL_SERVER']='smtp.mailtrap.io'
application.config['MAIL_PORT'] = 2525
application.config['MAIL_USERNAME'] = '5e98fcdb61f449'
application.config['MAIL_PASSWORD'] = '494caa4a69663f'
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USE_SSL'] = False
application.config["MAIL_DEFAULT_SENDER"] = "bc-muslim-anthology-proj@protonmail.com"

# application.config["MAIL_SERVER"]= "email-smtp.us-west-2.amazonaws.com"
# application.config["MAIL_PORT"] = 2587
# application.config["MAIL_USERNAME"] = "AKIAZS7YPLMFK5JBRUEX"
# application.config["MAIL_PASSWORD"] = "BONXhKD+yFlRLGmVGbKx7SL4MwLBDoS80PznPIF8RvtN"
# application.config["MAIL_USE_TLS"] = True
# application.config["MAIL_USE_SSL"] = False
# application.config["MAIL_DEFAULT_SENDER"] = "bc-muslim-anthology-proj@protonmail.com"

mail = Mail(application)
application.extensions['mail'].debug = 0

@application.route("/")
def hello_world():
  return "Hello, World!"

@application.route("/submission", methods=["POST"])
def submission():
  full_name = request.form["name"]
  email_address = request.form["email"]
  submission_type = request.form["type"]
  submission_title = request.form["title"]

  # msg = MIMEMultipart()
  # msg["Subject"] = "[MAP] Anthology Submission"
  # msg["From"] = "bc-muslim-anthology-proj@protonmail.com"
  # msg["To"] = "salmanf.siddiqui@gmail.com"

  msg = Message(subject="[MAP] Anthology Submission",
                reply_to=(full_name, email_address),
                recipients=["bc-muslim-anthology-proj@protonmail.com"])

  submission_files = []
  for file in request.files.getlist("submission"):
    filename = secure_filename(file.filename)

    msg.attach(filename, file.mimetype, file.read())
    
    # part = MIMEApplication(file.read())
    # part.add_header("Content-Disposition",
    #                 "attachment",
    #                 filename=filename)
    # msg.attach(part)

    submission_files.append(filename)

  message = f"New Submission:\n\n\
Name: {full_name}\n\
Email: {email_address}\n\
Type: {submission_type}\n\
Title: {submission_title}\n\
Files: {submission_files}"

  # body = MIMEText(message, "plain")
  # msg.attach(body)

  msg.body = message

  try:
    print("\nSending email...\n")
    mail.send(msg)
  except:
    print("ERROR: unable to send email")
    return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error=maxsize")

  # try:
  #   ses_client = boto3.client("ses", region_name="us-west-2")
  #   response = ses_client.send_raw_email(
  #       Source="bc-muslim-anthology-proj@protonmail.com",
  #       Destinations=["salmanf.siddiqui@gmail.com"],
  #       RawMessage={"Data": msg.as_string()}
  #   )
  #   print(response)
  # except ClientError as err:
  #   if "InvalidParameterValue" in str(err):
  #     print("ERROR sending email: message length exceeds allowed maximum (10MB)")
  #     return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error=maxsize")
  #   else:
  #     print("ERROR sending email:")
  #     print(err)
  #     return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error")

  print(message)
  return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?success")

@application.route("/contact", methods=["POST"])
def contact():
  name = request.form["name"]
  email = request.form["email"]
  message = request.form["message"]

  # msg = MIMEMultipart()
  # msg["Subject"] = "[MAP] Contact Form Submission"
  # msg["From"] = "bc-muslim-anthology-proj@protonmail.com"
  # msg["To"] = "salmanf.siddiqui@gmail.com"

  msg = Message(subject="[MAP] Contact Form Submission",
                reply_to=(name, email),
                recipients=["bc-muslim-anthology-proj@protonmail.com"])
  
  message = f"Contact Form:\n\n\
Name: {name}\n\
Email: {email}\n\
message: {message}"

  # body = MIMEText(message, "plain")
  # msg.attach(body)
  
  msg.body = message

  try:
    print("\nSending email...\n")
    mail.send(msg)
  except:
    print("ERROR: unable to send email")
    return redirect("https://bc-muslim-anthology-proj.netlify.app/contact-us?error")

  # try:
  #   ses_client = boto3.client("ses", region_name="us-west-2")
  #   response = ses_client.send_raw_email(
  #       Source="bc-muslim-anthology-proj@protonmail.com",
  #       Destinations=["salmanf.siddiqui@gmail.com"],
  #       RawMessage={"Data": msg.as_string()}
  #   )
  #   print(response)
  # except ClientError as err:
  #   if "InvalidParameterValue" in str(err):
  #     print("ERROR sending email: message length exceeds allowed maximum (10MB)")
  #     return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error=maxsize")
  #   else:
  #     print("ERROR sending email:")
  #     print(err)
  #     return redirect("https://bc-muslim-anthology-proj.netlify.app/submit-entry?error")

  print(message)
  return redirect("https://bc-muslim-anthology-proj.netlify.app/contact-us?success")


if __name__ == "__main__":
  application.run()

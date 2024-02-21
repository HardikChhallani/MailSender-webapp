from flask import Flask,render_template,request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/',methods=['POST'])
def getvalue():
    sender_mail = str(request.form['Sender-Email'])
    sender_app_password = str(request.form['Sender-App-Password'])
    receiver_mail = request.form['Receiver-Email']
    receiver_mail_lst = receiver_mail.split(',') #Listing the receiver mail id obtain via input
    subject = str(request.form['Subject'])
    description = str(request.form['Description'])

    return send_mails(sender_mail,sender_app_password,receiver_mail_lst,subject,description)

def send_mails(sender_mail,sender_app_password,receiver_mail_lst,subject,description):
    email = sender_mail
    app_password = sender_app_password
    subject = subject
    description = description
    try:
        for i in receiver_mail_lst:
            message = MIMEMultipart()
            message["From"] = email
            message["To"] = i
            message["Subject"] = subject
            message.attach(MIMEText(description, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(email, app_password)
            server.send_message(message)
            server.quit()
        return render_template('dashboard.html',success=True)
    except Exception as e:
        print(e)

if (__name__ == '__main__'):
    app.run(debug=True)
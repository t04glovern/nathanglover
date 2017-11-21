import os
from flask import Flask, render_template, request, send_from_directory
from flask_mail import Mail, Message

import config

'''
Init
'''
app = Flask(__name__)

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
mail = Mail(app)

'''
Web Page Routes
'''


@app.route("/", methods=['GET'])
def landing():
    return render_template("index.html")


@app.route("/ajax/send_mail", methods=['POST'])
def send_mail():
    sender_name = request.form['name']
    sender_email = request.form['email']
    sender_phone = request.form['phone']
    sender_message = request.form['message']

    msg = Message(
        sender_name + ' has sent an email',
        sender=config.MAIL_SENDER_EMAIL,
        recipients=[config.MAIL_RECEIVER_EMAIL]
    )

    msg.body = "Name: " + sender_name + "\n\n" + \
               "Email: " + sender_email + "\n\n" + \
               "Phone: " + sender_phone + "\n\n" + \
               sender_message

    mail.send(msg)
    return "Sent"


@app.route('/keybase.txt')
def keybase():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'keybase.txt',
        mimetype='text/plain'
    )


@app.route('/.well-known/keybase.txt')
def keybase_well_known():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'keybase.txt',
        mimetype='text/plain'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')

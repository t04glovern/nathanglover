import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_mail import Mail, Message
from flask_table import Table, Col

import etherscan.accounts as accounts

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

eth_wallet_address = config.ETH_WALLET_ADDRESS
etherscan_api_key = config.ETHERSCAN_API_KEY
etherscan_api = accounts.Account(address=eth_wallet_address, api_key=etherscan_api_key)

'''
Ethereum Table
'''

'''
class EthTable(Table):
    #tx_hash = Col('TxHash')
    #tx_age = Col('Age')
    tx_from = Col('From')
    tx_to = Col('To')
    tx_value = Col('Value')
    #tx_fee = Col('TxFee')


class Transaction(object):
    def __init__(self, tx_hash, tx_age, tx_from, tx_to, tx_value, tx_fee):
        self.tx_hash = tx_hash
        self.tx_age = tx_age
        self.tx_from = tx_from
        self.tx_to = tx_to
        self.tx_value = tx_value
        self.tx_fee = tx_fee


# Get the eth transactions
eth_transactions = etherscan_api.get_transaction_page(page=1, offset=10)


# Create and populate the eth transaction table objects
table_transactions = []
for transaction in eth_transactions:
    table_transactions.append(
        dict(#tx_hash=transaction["hash"],
             #tx_age=transaction["timeStamp"],
             tx_from=transaction["from"],
             tx_to=transaction["to"],
             tx_value=transaction["value"],
             #tx_fee=transaction["gasUsed"]
            )
    )


# Populate the table with the transaction objects
eth_table = EthTable(table_transactions, table_id='eth_table', classes=['table-responsive', 'table'])
'''

'''
Ethereum Price
'''

eth_value = int(etherscan_api.get_balance()) / config.WEI_DIVIDER


'''
Web Page Routes
'''


@app.route("/", methods=['GET'])
def landing():
    return render_template("index.html", eth_value=eth_value, eth_wallet=config.ETH_WALLET_ADDRESS)


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

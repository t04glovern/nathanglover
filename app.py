from flask import Flask, render_template


'''
Init
'''
app = Flask(__name__)

'''
Web Page Routes
'''


@app.route("/", methods=['GET'])
def landing():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
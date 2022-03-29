from flask import Flask, redirect
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)


@app.route('/message', methods=['POST'])
def index():
    return redirect('http://localhost:5000')


if __name__ == '__main__':
    app.run()

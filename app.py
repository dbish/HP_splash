from flask import Flask, render_template, url_for, request
import boto3
import os
import constants
from waitress import serve

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

aws_session = boto3.Session(
    aws_access_key_id = constants.AWS_PUBLIC_KEY,
    aws_secret_access_key = constants.AWS_SERVER_SECRET_KEY
)

def storeEmail(email):
    dynamodb = aws_session.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('augmend_waitlist')
    response = table.put_item(Item = {
        'email':email
    })
    print(response)


@app.route("/", methods = ['GET', 'POST'])
def index():
    email = ''
    if request.method == 'POST':
        data = request.form
        email = data['email']
        storeEmail(email)
    return render_template('index.html', email=email)

@app.route("/join")
def join():
    return render_template('recruiting.html')

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    serve(app, host='0.0.0.0', port=80)
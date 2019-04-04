from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "11": "aa",
    "22": "aa"
}


@auth.get_password
def get_pw(username):
    print('1')
    if username in users:
        return users.get(username)
    return None


@app.route('/')
@auth.login_required
def index():
    print('2')
    # print(auth.get_password())
    return "Hello, %s!" % auth.username()


if __name__ == '__main__':
    app.run()

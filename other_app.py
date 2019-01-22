from flask import Flask, request, render_template
import requests
import jwt

CLIENT_ID = 1
CLIENT_SECRET = 'APP_1_SECRET'
app = Flask(__name__)


@app.route('/')
def hello_world():
    code = request.args['code']

    print("Getting token...")
    data = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code}
    r = requests.post('http://localhost:8080/oauth2/token', json=data)
    if r.status_code != 200:
        print(r.status_code)
        print('Cant get token')
        return "<h1>Server error<h1>"

    token = r.json()['access_token']
    print("Token:", token)

    print("Getting user rents...")
    user_id = jwt.decode(token, verify=False)['sub']

    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get('http://localhost:8080/user/{}/rent'.format(user_id),
                     headers=headers)

    if r.status_code != 200:
        print('Cant get rents')
        print(r.json())
        return "<h1>Server error<h1>"

    return "<h1>Your rents: {0}<h1>".format(r.json()['user rents'])


if __name__ == '__main__':
    app.run('localhost', port=9090, debug=True)
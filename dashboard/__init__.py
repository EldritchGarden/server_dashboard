from flask import Flask, render_template, request, redirect, flash
from requests import HTTPError

from dashboard.pterodactyl import Server, server_list

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect('/')

    return render_template('index.html', server_list=server_list())

@app.route('/start/<id>', methods=['POST'])
def send_start_signal(id: str) -> str:
    try:
        server = Server(id)
        return server.start()
    except HTTPError as e:
        return e.response.text, e.response.status_code

@app.route('/state/<id>')
def get_server_state(id: str) -> str:
    try:
        server = Server(id)
        return server.get_state()['state']
    except HTTPError as e:
        return e.response.text, e.response.status_code

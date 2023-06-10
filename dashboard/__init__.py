from flask import Flask, render_template

from dashboard.pterodactyl import Server, server_list

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', server_list=server_list())

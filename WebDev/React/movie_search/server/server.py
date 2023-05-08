# pip3 install flask-cors
# Run this program: flask --app server --debug run

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
from flask import redirect
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/") # 'root' path of the url
def home():
    # current_user = request.args.get('username')
    current_user = request.cookies.get('user')
    return render_template('home.html', username=current_user)

@app.route("/about") # 'root' path of the url
def about():
    current_user = request.args.get('username')
    return render_template('about.html', username=current_user)

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    pwd = request.form.get('password')

    http_response = make_response(redirect('/?username=' + username))
    http_response.set_cookie('user', username)
    return http_response

@app.route("/logout", methods=["GET"])
def logout():
    http_response = make_response(redirect('/'))
    return http_response

@app.route("/likes/<movie_id>", methods=['GET'])
def likes(movie_id):
    movie_data = load_data()
    number_of_likes = movie_data.get(movie_id, 0)
    
    response = jsonify({ "count": number_of_likes })
    return response

@app.route("/likes/<movie_id>", methods=["POST"])
def change_likes(movie_id):
    delta = int(request.args.get("change"))
    
    movie_data = load_data()
    number_of_likes = movie_data.get(movie_id, 0)
    number_of_likes += delta
    
    if number_of_likes < 0:
        number_of_likes = 0
    
    movie_data[movie_id] = number_of_likes
    save_data(movie_data)
    
    response = jsonify({ "count": number_of_likes })
    return response

@app.route("/likes/top10", methods=["GET"])
def top_ten():
    movie_data = load_data();
    ids = [id for id, votes in sorted(movie_data.items(), key=lambda e: e[1], reverse=True)]
    return jsonify(ids[:10])

def load_data():
    try:
        with open('movie_data.json', 'r') as f:
            movie_data = json.load(f)
    except FileNotFoundError:
        movie_data = {}

    return movie_data

def save_data(movie_data):
    json_str = json.dumps(movie_data)
    with open("movie_data.json","w") as f:
        f.write(json_str)
    

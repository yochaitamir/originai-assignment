# import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response,send_from_directory
from flask_sqlalchemy import SQLAlchemy
import requests
from dataclasses import dataclass
from flask_cors import CORS
import pandas
import os
app = Flask(__name__, static_folder="./images-rating/build")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///images-rating.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@dataclass
class Image(db.Model):
    image_id: int
    image_url: str
    likes: int
    dislikes: int

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(250), unique=False)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Image {self.image_url}>'


db.create_all()
# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/')
def serve():
    # if path != "" and os.path.exists(app.static_folder + '/' + path):
    #     return send_from_directory(app.static_folder, path)
    # else:
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    """static folder serve"""
    file_name = path.split("/")[-1]
    dir_name = os.path.join(app.static_folder, "/".join(path.split("/")[:-1]))
    return send_from_directory(dir_name, file_name)

def populateDB():
    try:
        # 563492ad6f917000010000016785fe3645224defb9b412bacc72b345
        headers_dict = {"Authorization": "563492ad6f917000010000016785fe3645224defb9b412bacc72b345"}
        response = requests.get("https://api.pexels.com/v1/curated?per_page=100", headers=headers_dict)
        for image in response.json()["photos"]:
            new_image = Image(image_url=image["src"]["original"], likes=0, dislikes=0)
            # new_image = Image(likes=4, dislikes=4)
            db.session.add(new_image)
            db.session.commit()
    except:
        print("An exception occurred")


@app.route('/like/<id>', methods=['GET'])
def like(id):
    try:
        image_id = id
        Image_to_update = Image.query.get(image_id)
        Image_to_update.likes = Image_to_update.likes + 1
        db.session.commit()
        return jsonify({"msg": "like added"})
    except:
        print("couldnt update like")


@app.route('/dislike/<id>', methods=['GET'])
def dislike(id):
    try:
        image_id = id
        Image_to_update = Image.query.get(image_id)
        Image_to_update.dislikes = Image_to_update.dislikes + 1
        db.session.commit()
        return jsonify({"msg": "dislikes added"})
    except:
        print("couldnt update dislike")


@app.route('/exportcsv')
def exportcsv():
    try:
        all_images = db.session.query(Image).all()
        new_data = pandas.DataFrame(all_images)
        new_data.to_csv("images_rating.csv")
        return jsonify({"msg": "A csv file has been created"})
    except:
        return jsonify({"msg": "Creating csv file failed!"})


@app.route('/populate')
def home():
    # db.session.query(Image).delete()
    all_images = db.session.query(Image).all()
    if not len(all_images) > 0:
        populateDB()
        all_images = db.session.query(Image).all()
    return jsonify(all_images)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

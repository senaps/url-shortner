from string import ascii_uppercase, ascii_lowercase, digits
import random

from flask import Flask, jsonify, request, abort

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/url.db'
    db.init_app(app)
    
    @app.route("/ping/")
    def ping():
        return jsonify({"result": "pong"}), 200

    return app


class Url(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), index=True, nullable=False)
    shortened = db.Column(db.String(8))

    def __repr__(self):
        return f"<Url {self.url}>"


app = create_app()


def make_shorten():
    return random.choices(ascii_lowercase + ascii_uppercase + digits, k=8)


@app.route("/", methods=['POST'])
def shorten_url():
    """receive a url and shorten it

    this route will receive a long url and shorten it out and will reuturn
    to the user the user the short url.

    """
    data = request.get_json()
    if not data:
        abort(400)
    url = data.get("url")
    if not url:
        abort(400)
    shortened = make_shorten()
    res = Url.query.filter_by(url=url).first()
    if not res:
        obj = URL(url=url, shortened=shortened)
        db.session.add(obj)
        db.session.commit()
        return jsonify({"url": url, "shortened": shortened}), 201
    return jsonify({"url": url, "shortened": res.shortened}), 200


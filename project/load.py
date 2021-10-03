#Telepathy Labs
#From Beejay's Flask Boiler Plate

from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from project.models.base import db
from project.models.vid_member import VidMember
from project.models.video import Video
from project.models.videoreel import VideoReel

import markdown
import markdown.extensions.fenced_code

app = Flask(__name__, static_url_path='')
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple-vidreel.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#Import the routes
from project.routes import routes

##Let's create the DB if it's not created yet
with app.app_context():
    if not db.engine.dialect.has_table(db.engine, "videos"):
        Video.__table__.create(db.engine)
    if not db.engine.dialect.has_table(db.engine, "video_reels"):
        VideoReel.__table__.create(db.engine)
    if not db.engine.dialect.has_table(db.engine, "association"):
        db.create_all()
   

@app.route("/readme")
def readme():
    """This will just load the README.md

    Returns:
        README -- render of the README.md
    """
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string


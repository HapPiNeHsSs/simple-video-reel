from project.models.base import db
from datetime import datetime

VidMember =  db.Table('association', db.Model.metadata,
    db.Column('video_reel', db.Integer, db.ForeignKey('video_reels.id')),
    db.Column('video', db.Integer, db.ForeignKey('videos.id'))
)


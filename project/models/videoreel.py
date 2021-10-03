from project.models.base import db
from project.models.vid_member import VidMember
from project.models.enums import standard as standard_types, definition as definition_types
from project.models.timecode import Timecode
from project.models.video import Video
from datetime import datetime

class VideoReel(db.Model):
    """
    The Video Reel

    This also provides class methods for create, retrieve, update methods
    
    """ 
    
    __tablename__ = 'video_reels'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    videos = db.relationship("Video", secondary=VidMember, back_populates="video_reel")
    standard = db.Column(db.Enum(standard_types), nullable=False)
    definition = db.Column(db.Enum(definition_types), nullable=False)
    timecode = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, name, videos, totalframes, standard, definition):
        """Creates Video Entry
        Arguments:
            name, description, timecode, standard, definition
        """        
        self.name = name
        self.videos = Video.find_many_in_id_list(videos)
        self.timecode = Timecode.fromFrames(totalframes, standard).to_json()
        self.standard = standard_types(standard)
        self.definition = definition_types(definition)
        self.recalculate_timecode()
        db.session.add(self)
        db.session.commit()
    
    def recalculate_timecode(self):
        """A quick utility function to fix erroneus timcodes
        """
        frames = 0
        for video in self.videos:
            frames+=Timecode.fromJSON(video.timecode).totalframes
        self.timecode = Timecode.fromFrames(frames, self.standard.value).to_json()
        db.session.commit()
    
    def videos_to_dict(self):
        """Return Video Objects as array of dict for easier consumption

        Returns:
            [array] -- [array of dictionaries of video object]
        """

        def to_dict(x):
            return {
                'id': x.id,
                'name': x.name,
                'description': x.description,
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
            }
        return list(map(lambda x: to_dict(x), self.videos))

    @classmethod
    def find_by_id(cls, id):
        x = cls.query.filter_by(id = id).first()
        return {
                'id': x.id,
                'name': x.name,
                'videos': x.videos,
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
            }
    
    @classmethod
    def return_all(cls):
        def to_dict(x):
            return {
                'id': x.id,
                'name': x.name,
                'videos': x.videos_to_dict(),
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
            }
        return list(map(lambda x: to_dict(x), VideoReel.query.all()))

    @classmethod
    def delete(cls,_id):
        try:
            cls.query.filter_by(id=_id).delete()
            db.session.commit()
            return {'message': 'Video Deleted'}
        except:
            return {'message': 'Something went wrong'}

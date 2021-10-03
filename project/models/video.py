from project.models.base import db
from project.models.vid_member import VidMember
from project.models.enums import standard as standard_types, definition as definition_types
from datetime import datetime
from project.models.timecode import Timecode
import enum
class Video(db.Model):
    """
    The Video

    This also provides class methods for create, retrieve, update methods
    
    """ 
    
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    video_reel = db.relationship("VideoReel", secondary=VidMember, back_populates="videos")
    description = db.Column(db.Text, nullable = False)
    timecode = db.Column(db.Text, nullable=True)
    standard = db.Column(db.Enum(standard_types), nullable=False)
    definition = db.Column(db.Enum(definition_types), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, description, timecode, standard, definition):
        """Creates Video Entry
        Arguments:
            name, description, timecode, standard, definition
        """        
        self.name = name
        self.description = description
        self.timecode = Timecode(timecode, standard).to_json()
        self.standard = standard_types(standard)
        self.definition = definition_types(definition)
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, id):
        x = cls.query.filter_by(id = id).first()
        return {
                'id': x.id,
                'name': x.name,
                'description': x.description,
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
            }
    
    @classmethod
    def find_many_in_id_list(cls, id_list):
        return cls.query.filter(Video.id.in_(id_list)).all()
    
    @classmethod
    def return_all(cls):
        def to_dict(x):
            return {
                'id': x.id,
                'name': x.name,
                'description': x.description,
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
            }
        return list(map(lambda x: to_dict(x), Video.query.all()))

    @classmethod
    def delete(cls,_id):
        try:
            cls.query.filter_by(id=_id).delete()
            db.session.commit()
            return {'message': 'Video Deleted'}
        except:
            return {'message': 'Something went wrong'}

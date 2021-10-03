import datetime, json
from project.models.enums import standard as types

class Timecode:
    """
    The Timecode of a Video Reel

    Defaults to NTSC

    This also provides class methods for create, retrieve, update methods
    Passwords are hashed using sha256
    
    """ 
    _time = ""
    time = datetime.time()
    standard = types.NTSC
    fps = 30
    frames = 0
    seconds = 0
    
    def __init__(self, timestring, standard):
        """Sets the time code 

        Currently no checks as this is POC

        Arguments:
            timestring {string} -- "HH:MM:SS:ff"
            standard {string} -- "ntsc" or ""pal
        """
        hmsf = timestring.split(':')
        self.hours = int(hmsf[0])
        self.minutes = int(hmsf[1])
        self.seconds = int(hmsf[2])
        self.frames = int(hmsf[3])
        self.standard = standard
        self.fps = 30 if types.NTSC is types(standard) else 25
        
        
        if self.frames > self.fps:
            p_frames = self.frames % self.fps
            p_sec = self.seconds + int(self.frames / self.fps)
            self.frames = p_frames
            if p_sec >= 60:
                self.seconds = p_sec % 60
                p_min = self.minutes + int(p_sec / 60)
                if p_min >= 60:
                    self.minutes = p_min % 60
                    self.hours = self.hours + int(p_min / 60)
                else: self.minutes = p_min
            else: self.seconds = p_sec
        
        #we save total frames for easier timecode addition
        timecode = self.get_time_code()

        ftr = [108000,1800,30,1] if types.NTSC is types(standard) else [90000,1500,25,1]

        self.totalframes = sum([a*b for a,b in zip(ftr, map(int,timecode.split(':')))])

        return

    def get_time_code(self):
        return(f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}:{self.frames:02d}")
    

    
    def to_dict(self):
        dict = {}
        dict['standard'] = self.standard
        dict['timecode'] = self.get_time_code()
        dict['totalframes'] = self.totalframes
        return dict
    
    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def fromJSON(cls, json_str):
        dict = json.loads(json_str)
        return cls(dict['timecode'],dict['standard'])

    @classmethod
    def fromFrames(cls, frames, standard):
        """Generate the class using frame number only.

        This is greate whem adding totalframes and converting them to timecode object
        """
        timestring="00:00:00:"+str(frames)
        return cls(timestring, standard)
        


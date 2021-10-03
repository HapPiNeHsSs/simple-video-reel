from flask_restful import Resource, reqparse
from project.models.video import Video
from project.models.videoreel import VideoReel
from project.models.timecode import Timecode
from project.load import app
from flask import render_template, request, jsonify
import sys, traceback

@app.route('/api/video_reel',  methods = ['POST'])
def create_video_reel():
    """Creates a new video Reel Entry

    METHOD: POST
    ENDPOINT: /api/create_video
    Parameters: JSON
    {"video-reel-name":"vidname","video-standard":"ntsc/pal","video-definition":"hd/sd"}

    Returns:
        json --  'id': x.id,
                'name': x.name,
                'video_list': array of Video IDs
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
    """

    try: 
        
        req = request.get_json(silent=True)
        name = req['video-reel-name']
        videos = req['video_list']
        totalframes = req['totalframes']
        standard = req['video-standard']
        definition = req['video-definition']

        #check if there are mixed Standard and definition
        for vid in Video.find_many_in_id_list(videos):
            if vid.standard.value != standard:
                return {'error':'mixed standard'}
            if vid.definition.value != definition:
                return {'error':'mixed definition'}
        
        x = VideoReel(name, videos, totalframes, standard, definition)
        return {
                'id': x.id,
                'name': x.name,
                'videos': x.videos_to_dict(),
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
            }
    except  Exception as e:
        traceback.print_exc()
        return str(type(e))+" "+str(e)

@app.route('/api/video',  methods = ['POST'])
def create_video():
    """Creates a new video Entry

    METHOD: POST
    ENDPOINT: /api/create_video
    Parameters: JSON
    {"video-name":"vidname","video-description":"vidDescription",video-duration:"HH:MM:SS","video-standard":"ntsc/pal","video-definition":"hd/sd"}

    Returns:
        json --  'id': x.id,
                'name': x.name,
                'description': x.description,
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
    """
    try:       
        req = request.get_json(silent=True)
        name = req['video-name']
        description = req['video-description']
        timecode = req['video-duration']
        standard = req['video-standard']
        definition = req['video-definition']
        x = Video(name, description, timecode, standard, definition)
        return {
                'id': x.id,
                'name': x.name,
                'description': x.description,
                'timecode': Timecode.fromJSON(x.timecode).to_dict(),
                'standard': x.standard.value,
                'definition':x.definition.value
            }
    except  Exception as e:
        traceback.print_exc()
        return str(type(e))+" "+str(e)

@app.route('/api/video',  methods = ['DELETE'])
def delete_video():
    """Deletes a video Entry

    METHOD: POST
    ENDPOINT: /api/create_video
    Parameters: JSON
    {"video-name":"vidname","video-description":"vidDescription",video-duration:"HH:MM:SS","video-standard":"ntsc/pal","video-definition":"hd/sd"}

    Returns:
        json --  { "id": id}
    """
    try:
        req = request.get_json(silent=True)
        id = req['id']
        return Video.delete(id)
    except  Exception as e:
        traceback.print_exc()
        return str(type(e))+" "+str(e)

@app.route('/api/calculate_duration',  methods = ['POST'])
def calcualte_duration():
    """Quick API to calcualate duration summation

    METHOD: POST
    ENDPOINT: /api/create_video
    Parameters: JSON
    {"total_frames":int}

    Returns:
        json --  { "total_duration": timecode}
    """
    try:
        req = request.get_json(silent=True)
        frames = req['total_frames']
        standard = req['standard']
        return {'total_duration':Timecode.fromFrames(frames, standard).to_dict()}
    except  Exception as e:
        traceback.print_exc()
        return str(type(e))+" "+str(e)

@app.route('/')
def index():
    videos = Video.return_all()
    video_reels = VideoReel.return_all()
    return render_template('index.html',videos=videos, video_reels=video_reels)

@app.route('/video_list/')
def video_list():
    videos = Video.return_all()
    return render_template('video_list.html',videos=videos)

@app.route('/create_video_reel/')
def create_reel():
    videos = Video.return_all()
    return render_template('create_video_reel.html',videos=videos)
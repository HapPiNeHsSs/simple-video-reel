import os, json, unittest, time
from project.load import app, db
 
 
class BasicTests(unittest.TestCase):
    #Some basic Setup and Tear Downs

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test/testdb.sqlite'
        self.app = app.test_client()
        with  app.app_context():
            db.drop_all()
            db.create_all()

        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.drop_all()
 
 
#Here are the tests
 
    def testCreateVid(self):
        """Let's test if create a video detail. Expecting Response 200
        """ 
        data ={'video-name':"VidTest",
            'video-description':"Test Description",
            'video-duration':"04:02:34:12",
            'video-standard':'ntsc',
            'video-definition':'hd'}
        
        print("Testing adding a Video Detail: " + json.dumps(data))
        response=self.app.post('/api/video', 
                       data=json.dumps(data),
                       content_type='application/json')

        self.assertEqual(response.status_code, 200) 

    def testNoNameCreateVid(self):
        """Let's test if creatomg without video-name should work. It Should not.
        """ 
        data ={'vide':"",
            'video-description':"Test Description",
            'video-duration':"04:02:34:12",
            'video-standard':'ntsc',
            'video-definition':'hd'}
        
       
        response=self.app.post('/api/video', 
                       data=json.dumps(data),
                       content_type='application/json')
        self.assertEqual(response.data, bytes("<class 'KeyError'> 'video-name'", encoding="UTF-8")) 
    
    def testCreateVideoReel(self):
        """Let's test if we can create a Video Reel
        """ 
        data ={'video-name':"VidTest 1",
            'video-description':"Test Description 1",
            'video-duration':"00:00:01:29",
            'video-standard':'ntsc',
            'video-definition':'hd'}
        
        print("Testing adding a Video Detail 1: " + json.dumps(data))
        response=self.app.post('/api/video', 
                       data=json.dumps(data),
                       content_type='application/json')
        
        data ={'video-name':"VidTest 2",
            'video-description':"Test Description 2",
            'video-duration':"00:00:01:29",
            'video-standard':'ntsc',
            'video-definition':'hd'}
        
        print("Testing adding a Video Detail 2: " + json.dumps(data))
        response=self.app.post('/api/video', 
                       data=json.dumps(data),
                       content_type='application/json')
        print(response.data)

        data ={'video-reel-name':"VidReel",
            'totalframes':0,
            'video_list':["1","2"],
            'video-standard':'ntsc',
            'video-definition':'hd'}
        print("Testing adding a Video Reel: " + json.dumps(data))
        response=self.app.post('/api/video_reel', 
                       data=json.dumps(data),
                       content_type='application/json')
        tc = (json.loads(response.data.decode('utf-8'))['timecode']['timecode'])

        #check if the timecode matches 00:00:01:29 + 00:00:01:29. Should be 00:00:03:28
        self.assertEqual(tc, '00:00:03:28' )   
    
    def testMixStandard(self):
        """Let's test if we can add pal to a ntsc video reel
        """ 
        data ={'video-name':"VidTest 1",
            'video-description':"Test Description 1",
            'video-duration':"00:00:01:29",
            'video-standard':'ntsc',
            'video-definition':'hd'}
        
        print("Testing adding a Video Detail 1: " + json.dumps(data))
        response=self.app.post('/api/video', 
                       data=json.dumps(data),
                       content_type='application/json')
        
        data ={'video-reel-name':"VidReel",
            'totalframes':0,
            'video_list':["1"],
            'video-standard':'pal',
            'video-definition':'hd'}
        print("Testing adding a Video Reel: " + json.dumps(data))
        response=self.app.post('/api/video_reel', 
                       data=json.dumps(data),
                       content_type='application/json')
        err = json.loads(response.data.decode('utf-8'))
        #It should return an error saying mixed standard
        self.assertEqual(err['error'], 'mixed standard' )   
        
    def testMixDefinition(self):
        """Let's test if we can add SD to a HD video reel
        """ 
        data ={'video-name':"VidTest 1",
            'video-description':"Test Description 1",
            'video-duration':"00:00:01:29",
            'video-standard':'ntsc',
            'video-definition':'sd'}
        
        print("Testing adding a Video Detail 1: " + json.dumps(data))
        response=self.app.post('/api/video', 
                       data=json.dumps(data),
                       content_type='application/json')
        
        data ={'video-reel-name':"VidReel",
            'totalframes':0,
            'video_list':["1"],
            'video-standard':'ntsc',
            'video-definition':'hd'}
        print("Testing adding a Video Reel: " + json.dumps(data))
        response=self.app.post('/api/video_reel', 
                       data=json.dumps(data),
                       content_type='application/json')
        err = json.loads(response.data.decode('utf-8'))
        #It should return an error saying mixed definition
        self.assertEqual(err['error'], 'mixed definition' ) 

if __name__ == "__main__":
    unittest.main()
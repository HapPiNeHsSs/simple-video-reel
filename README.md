# Simple Video Reel 

## Running via Python3 ##

Make sure you have these requirements
- Python 3.8
- pip3

It's also good to have separate python environments. You can read about that [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv)

At this point, you must have activated your environment as well if you have chosen to have one.

To Install requirements run `pip install -r requirements.txt`

To Run the Service run `python3 run.py`

The service will run on port **8080**

Terminate by `Ctrl+C`

## Running via Docker ##

**Building and Running**

Make sure **docker** is installed and run these commands

1. `docker image build -t python-app .`
2. `docker run --name=python-app-docker -p 8080:8080 -d python-app`

This will run the service on port **8080**

**Stopping the Service**

`docker stop python-app-docker`

**Restarting the Service**

`docker start python-app-docker`

**Removing the container (when you want to start anew)**

1. `docker stop python-app-docker` if it is running, else go to step 2
2. `docker rm python-app-docker`

## Unit Test ##
The unit tests are in `project/test`.

You can run the unit tests by: `python3 -m unittest project/test/tests.py` from the root app directory

## Key URL ##

**{host}/**
- Your index. Displays already created Video Reels
- Selecting a Video Reel will show the Reel's information and the videos that are part of this Reel
- Selecting a Video from the the "Videos in Reel" box will show details about that video

**{host}/create_video_reel/**
- You can Create new Video Reels Here
- Select a video from Available Vidoes and press Add To Reel to put that video in the Reel
- Select a vide from Videos In Reel and press Remove From Reel to put it back to the Available Videos
- Selecting a video name will show the details under Selected Video Details
- Duration changes depending on what reel you've added
- Press Create Video Reel to save. You will be brought back to the index
- What the Test ordered

**{host}/video_list/**
- You can view and add videos here
- selecting a video will show raw json info under video details

## Available APIs ##

**Create Video Reel:**

Creates a Video Reel with a set Standard and Definition from an Array of Video Indices
    
    METHOD: POST
    ENDPOINT: /api/create_video
    PARAMETER: JSON {"video-reel-name":"vidname",
                      "video_list":[arrray of videos],
                      "video-standard":"ntsc/pal",
                      "video-definition":"hd/sd"}
    
    Returns:
        JSON: {
                'id': id,
                'name': name,
                'videos': videos_to_dict(),
                'timecode': Timecode,
                'standard': standard.value,
                'definition': definition.value
            }


**Create Video Detail:**

Creates a Video detail that you can add on your video detail pool
    
    METHOD: POST
    ENDPOINT: /api/video
    PARAMETER: JSON {"video-name":"video name",
                      "video-description":description,
                      "video-duration":TIMECODE,
                      "video-standard":"ntsc/pal",
                      "video-definition":"hd/sd"}
    
    Returns:
        JSON: {
                'id': id,
                'name': name,
                'description': description,
                'timecode': Timecode,
                'standard': standard.value,
                'definition': definition.value
            }


**Delete Video Detail:**
    
Deletes a Video Detail
    
    METHOD: DELETE
    ENDPOINT: /api/video
    PARAMETER: JSON {"id":"video_id"}
    
    Returns:
        JSON: {'message': 'Video Deleted'}

**Calculate Duration(Timecode) from total frames:**
    
Returns Timecode from number of frames and standard. Useful for displaying total timecode of
videos in a reel when not yet being saved. Should be client side actually
    
    METHOD: DELETE
    ENDPOINT: /api/video
    PARAMETER: JSON {"total_frames":total Video Frames,
                      "standard": "ntsc/pal"}
    
    Returns:
        JSON: {'total_duration': Timecode}


**Timecode Format**

The Timecode class has a to_dict() and toJSON() functions to help with serialization and storage.
- The format when serialize is: {"standard":"ntsc/oal","timecode":"00:00:01:29","totalframes":59}

---

---
---
# Original Telepathy Labs Test Details
---
---

# Technical Test

# User Story 911

Creative Agency User want to create a new show reel from a collection of clips in order to present my agency commercials to the advertiser

## Background

- A show reel has name, video standard, video definition and total duration expressed as
    timecode (hh:mm:ss:ff)
- Video standard is either PAL or NTSC
- Video definition is SD or HD
- A show reel can have 1 or more video clips
- A video clip has a name, description, video standard, video definition, start timecode and end
    timecode
- A timecode is expressed as HH:MM:ss:ff
    o HH > hours
    o MM > minutes
    o ss > seconds
    o ff > frames
    o PAL video has 25 fps (25 frames per second) i.e. 1 frame is 40 milliseconds
    o NTSC video has 30 fps

## Requirements

1. Create a proof of concept user interface for the customer
2. The UI should show the complete duration of all the clips in the show reel
3. The UI should allow me to give my show reel a name.
4. The UI should allow me to add and remove clips from a list. This should update the total
duration
5. One can not mix video standards and video definitions in a video reel. i.e. NTSC clip
cannot be added to PAL video reel. HD clip could not be added to a SD video reel.

## Technical Notes

## Development time is 4 hours.

Please select language(s) / framework(s) of your choice.

## The generic functions created will be used by other applications. Please ensure that there is

enough abstraction. i.e. Timecode class can be used in another project.
We are looking at code quality and thought process, we would prefer an unfinished solution with
quality code compared to a complete application with rushed code.

## Data

- Clip
    o Name: Bud Light
    o Description: A factory is working on the new Bud Light Platinum.
    o Standard: PAL


```
o Definition: SD
o Start timecode: 00:00:00:
o End timecode: 00:00:30:
```
- Clip
    o Name: M&M's
    o Description: At a party, a brown shelled M&M is mistaken for being naked. As a result,
       the red M&M tears off its skin and dances to "Sexy and I Know It" by LMFAO.
    o Standard: NTSC
    o Definition: SD
    o Start timecode: 00:00:00:
    o End timecode: 00:00:15:
- Clip
    o Name: Audi
    o Description: A group of vampires are having a party in the woods. The vampire in charge
       of drinks (blood types) arrives in his Audi. The bright lights of the car kills all of the
       vampires, with him wondering where everyone went afterwards.
    o Standard: PAL
    o Definition: SD
    o Start timecode: 00:00:00:
    o End timecode: 00:01:30:
- Clip
    o Name: Chrysler
    o Description: Clint Eastwood recounts how the automotive industry survived the Great
       Recession.
    o Standard: PAL
    o Definition: SD
    o Start timecode: 00:00:00:
    o End timecode: 00:00:10:
- Clip
    o Name: Fiat
    o Description: A man walks through a street to discover a beautiful woman (Catrinel
       Menghia) standing on a parking space, who proceeds to approach and seduce him, when
       successfully doing so he then discovers he was about to kiss a Fiat 500 Abarth.
    o Standard NTSC
    o Definition: SD
    o Start timecode: 00:00:00:
    o End timecode: 00:00:18:
- Clip
    o Name: Pepsi
    o Description: People in the Middles Ages try to entertain their king (Elton John) for a
       Pepsi. While the first person fails, a mysterious person (Season 1 X Factor winner


```
Melanie Amaro) wins the Pepsi by singing Aretha Franklin's "Respect"." After she wins,
she overthrows the king and gives Pepsi to all the town.
o Standard: NTSC
o Definition: SD
o Start timecode: 00:00:00:
o End timecode: 00:00:20:
```
- Clip
    o Name: Best Buy
    o Description: An ad featuring the creators of the camera phone, Siri, and the first text
       message. The creators of Words with Friends also appear parodying the incident
       involving Alec Baldwin playing the game on an airplane.
    o Standard: PAL
    o Definition: HD
    o Start timecode: 00:00:00:
    o End timecode: 00:00:10:
- Clip
    o Name: Captain America The First Avenger
    o Description: Video Promo
    o Standard: PAL
    o Definition: HD
    o Start timecode: 00:00:00:
    o End timecode: 00:00:20:
- Clip
    o Name: Volkswagen "Black Beetle"
    o Description: A computer generated black beetle runs fast, as it is referencing the new
       Volkswagen model.
    o Standard: NTSC
    o Definition: HD
    o Start timecode: 00:00:00:
    o End timecode: 00:00:30:

## Acceptance Tests

**1 Given^ I navigate to the user interface and create a PAL SD^ Video Reel^**
- When I try and add NTSC SD video clip:
  - Then user interface should prevent me from doing this action

**2 Given^ I navigate to the user interface and create a PAL SD Video Reel^**
- When I try and add PAL HD video clip:
  - Then user interface should prevent me from doing this action

**3 Given^ I navigate to the user interface and create a PAL SD Video Reel^**
- When I add all the PAL SD video clips
  - Then the total duration displayed is 00:02:11:01

**4 Given^ I navigate to the user interface and create a NTSC SD Video Reel^**
- When I add all the NTSC SD video clips
  - Then the total duration displayed is 00:00:54:08



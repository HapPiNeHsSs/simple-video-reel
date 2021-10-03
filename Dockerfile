FROM python:3.8-alpine
WORKDIR /video-reel
ADD . /video-reel
RUN pip install -r requirements.txt
CMD ["python","run.py"]

FROM python:3.10.8-slim 


ENV PYTHONUNBUFFERED 1
#IT TELLS THAT THE OUTPUT OF PYTHON IS PRINTED ON THE CONSOLE WITHOUT ANY BUFFER

COPY requirements.txt requirements.txt

EXPOSE 8000

RUN pip install --upgrade pip 

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

WORKDIR /
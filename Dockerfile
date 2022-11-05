FROM ubuntu
RUN apt-get update -y --fix-missing --allow-releaseinfo-change
RUN apt-get install -y build-essential libgl1-mesa-glx libsm6 libxext6 libglib2.0-0
RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install -r requirements.txt
CMD ["python3", "wsgi.py"]
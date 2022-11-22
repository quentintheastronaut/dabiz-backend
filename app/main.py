import os
from flask import Flask, render_template, request, jsonify
from app.reverseProxy import proxyRequest
from app.classifier import classifyImage


MODE = os.getenv('FLASK_ENV')
DEV_SERVER_URL = 'http://localhost:3000/'

app = Flask(__name__)

# Ignore static folder in development mode.
if MODE == "development":
    app = Flask(__name__, static_folder=None)

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    if MODE == 'development':
        return proxyRequest(DEV_SERVER_URL, path)
    else:
        return render_template("index.html")    

@app.route('/classify', methods=['POST'])
def classify():
    if (request.json['image']): 
        image_url = request.json['image']

        print(image_url)

        result = classifyImage(image_url)
        print('Model classification:')  
        print(result)      
        return jsonify(
            {
                'meta':  {
                    'statusCode' : 200,
                    'message': 'Ok'
                },
                'data': result
            }
        )
    return jsonify(
        {
            'meta':  {
                'statusCode' : 500,
                'message': 'Something went wrong'
            },
            'data': {}
        }
    )
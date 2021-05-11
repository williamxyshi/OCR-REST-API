from flask import Flask, jsonify, make_response, request
from ocr.receipt_ocr import textAlignmentGetTotal
from cv.preprocess import get_grayscale
import cv2
import json
import numpy
import secrets
import bcrypt
import jwt
from bson.json_util import dumps
from flask_pymongo import PyMongo
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
mongodb_client = PyMongo(app, uri="secret!")
db = mongodb_client.db


SECRET_KEY = 'secret'

def token_required(something):
    def wrap():
        try:
            token_passed = request.headers['token']
            if request.headers['token'] != '' and request.headers['token'] != None:
                try:
                    user = db.ocrusers.find_one({
                            'key': token_passed
                            })

                    if(user['calls'] >= 10000):
                        return_data = {
                            "error" : "4",
                            "message" : "Too many requests",
                        }
                        return app.response_class(response=json.dumps(return_data), mimetype='application/json'),401


                    newCalls = user['calls'] + 1
                    user.update({
                        'calls' : newCalls
                    })
                    db.ocrusers.save(user)
                    return something()
                except jwt.exceptions.ExpiredSignatureError:
                    return_data = {
                        "error": "1",
                        "message": "Token has expired"
                        }
                    return app.response_class(response=json.dumps(return_data), mimetype='application/json'),401
                except:
                    return_data = {
                        "error": "1",
                        "message": "Invalid Token"
                    }
                    return app.response_class(response=json.dumps(return_data), mimetype='application/json'),401
            else:
                return_data = {
                    "error" : "2",
                    "message" : "Token required",
                }
                return app.response_class(response=json.dumps(return_data), mimetype='application/json'),401
        except Exception as e:
            return_data = {
                "error" : "3",
                "message" : "An error occured"
                }
            return app.response_class(response=json.dumps(return_data), mimetype='application/json'),500

    return wrap


# @app.before_request
# def hook():
#     if request.endpoint == 'receipt_ocr':
#         if request.headers.get('token') != '111':
#             return jsonify({
#                 'error': "UnAuthorized"
#             })

@app.route('/api/receiptocr', methods=["POST"])
@token_required
def receipt_ocr():
    image_file = request.files['receipt'].read()
    npimg = numpy.frombuffer(image_file, numpy.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    gray = get_grayscale(image)

    text = textAlignmentGetTotal(gray)
    return jsonify({'total': text})

@app.route('/api/user', methods=["GET", "POST"])
def signupgetuser():
    if request.method == 'POST':
        try:
            email = request.get_json()['email']
            password = request.get_json()['password']
            user = db.ocrusers.find_one({
                'email': email
            })
            if user:
                return jsonify({"message": "user already exists"}), 400
            api_key = secrets.token_urlsafe(35)
    
            db.ocrusers.insert_one({
                'email': email, 
                'password': password, 
                'key': api_key, 
                'calls': 0 })
        except:
            return jsonify({"message": "could not create user"}), 400

        return {}, 200
    else :
        data = jwt.decode(request.headers['token'],SECRET_KEY, algorithms=['HS256'])

        user = db.ocrusers.find_one({
            'email': data['email']
        })

        return jsonify({"user": {
            'email': user['email'],
            'key' : user['key'],
            'calls': user['calls']
        }}), 200



@app.route('/api/user/login', methods=["POST"])
def login():
    email = request.get_json()['email']
    password = request.get_json()['password']

    user = db.ocrusers.find_one({
        'email': email
    })

    if user:
        # if bcrypt.checkpw(user['password'].encode('utf-8'), password):
        if user['password'] == password:
            payload = {"email": email}
            token = jwt.encode(payload, SECRET_KEY)
            return jsonify({"token": token}), 200
        else:
            return jsonify({'message': 'incorrect password'}), 400
    else:
        return jsonify({"message": 'user not found'}), 400

    
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'content-type , token'
    
    return response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import Flask
from flask import jsonify

from rains.server.api.server_request_handler import ServerRequestHandler


app: Flask = Flask(__name__)


@app.route('/get1', methods=['GET'])
def get1():
    return jsonify({
        'code': 0,
        'data': 'get1'
    })


@app.route('/get2', methods=['GET'])
def get2():
    return jsonify({
        'code': 0,
        'data': 'get2'
    })


@app.route('/post1', methods=['POST'])
def post1():
    a = ServerRequestHandler.analysis_request_parameter(['v1', 'v2'], ['v1'])
    return jsonify({
        'code': 0,
        'data': a
    })
    
    
@app.route('/post2', methods=['POST'])
def post2():
    token = ServerRequestHandler.analysis_request_headers(['Authorization'], ['Authorization'])
    a = ServerRequestHandler.analysis_request_parameter(['v1', 'v2'], ['v1'])
    return jsonify({
        'code': 0,
        'data': a,
        'token': token['Authorization']
    })


app.run()

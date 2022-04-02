from flask import Flask, jsonify, request
from flask_cors import CORS
import configenv
import os
#cors
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

FEC_API_KEY = os.getenv("FEC_API_KEY"),

@app.route('/candidate-data', methods=['POST', 'GET'])
def main():
    candidateID = request.headers.get('candidateid') # the id of the selected candidate
    print('the given candidateID is:', candidateID)
    
    candidateData = request.json # all of the data for the candidate
    print('all json data is ', candidateData)

    # formulate a response
    response = jsonify({'jsondata': 'here'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug='true')
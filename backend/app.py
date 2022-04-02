from flask import Flask
from flask_cors import CORS
import configenv
import os
#cors
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

FEC_API_KEY = os.getenv("FEC_API_KEY"),

@app.route('/')
def main():
    return {
        'data': 'here'
    }

# run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug='true')
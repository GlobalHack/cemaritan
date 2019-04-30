import json

from flask import Flask, request, jsonify

import api

app = Flask(__name__)

@app.route('/convertsingle', methods=['POST'])
def single():
    obj = request.get_json()
    return jsonify(obj)

@app.route('/bulkupload', methods=['POST'])
def accept_file():
    print(request.files)
    t = json.loads(request.files['file'])
    print(t)
    return 'Success'

if __name__=='__main__':
    app.run(debug=True)
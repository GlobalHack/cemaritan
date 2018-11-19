import json

from flask import Flask, request, jsonify

import api

app = Flask(__name__)

@app.route('/convertsingle', methods=['POST'])
def single():
    obj = request.get_json()
    return jsonify(obj)

if __name__=='__main__':
    app.run(debug=True)
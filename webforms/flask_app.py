from flask import Flask, request

app = Flask(__name__)


@app.route("/submitdata", methods=['POST'])
def print_body():
    print(str(request.form))
    return str(request.form)


if __name__=='__main__':
    app.run(debug=True)
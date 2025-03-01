from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open("studentdata.json", "r") as json_file:
    studentdata = json.load(json_file)

@app.route("/student/<id>", methods=["GET"])
def home(id):
    return jsonify(studentdata['students'][int(id)])

if __name__ == "__main__":
    app.run(debug=True)

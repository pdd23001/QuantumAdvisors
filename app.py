from flask import Flask, render_template, request, jsonify
import qaoa_scheduler
import scheduling
import hashlib
import advisor as advis

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quantum")
def quantum():
    return render_template("quantum.html")

@app.route("/run_quantum",methods=["POST"])
def run_quantum():
    data = request.json
    exams = int(data.get('exams'))
    slots = int(data.get('slots'))
    r = qaoa_scheduler.func(exams,slots)
    return jsonify(r)

@app.route("/run_classical",methods=["POST"])
def run_classical():
    return jsonify(scheduling.find_best())

@app.route("/advisor")
def advisor():
    return render_template("advisor.html")


def str_hash(s):
    return (len(s)+sum(ord(i) for i in s))%20

map = {"tjb20007":3,"pdd12345":5,"abc12345":7}

@app.route("/advisor_resp",methods=["POST"])
def advisor_resp():
    data = request.json
    ID = data.get('studentId')
    if ID in map:
        id = map[ID]
    else:
        str_hash(data.get('studentId'))
    r = advis.chatbot2(id)
    return jsonify(r)


if __name__ == "__main__":
    app.run(debug=True)

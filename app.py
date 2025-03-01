from flask import Flask, render_template, request, jsonify
import final_scheduler
import script

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
    r = final_scheduler.func(exams,slots)
    return jsonify(r)

@app.route("/run_classical",methods=["POST"])
def run_classical():
    return jsonify(script.find_best())

@app.route("/advisor")
def advisor():
    return render_template("advisor.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quantum")
def quantum():
    return render_template("quantum.html")

@app.route("/advisor")
def advisor():
    return render_template("advisor.html")

if __name__ == "__main__":
    app.run(debug=True)

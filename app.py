from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    resume_text = request.form.get("resume_text")

    if not resume_text:
        return "Please enter your resume details."

    return f"""
    <h1>Resume Analysis Result</h1>
    <p>Resume received successfully!</p>
    <hr>
    <p>{resume_text}</p>
    """


if __name__ == "__main__":
    app.run(debug=True)
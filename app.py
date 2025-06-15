from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from utils.grader import process_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            score, feedback = process_resume(filepath)
            return render_template("result.html", score=score, feedback=feedback)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

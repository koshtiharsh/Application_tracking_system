from flask import Flask, render_template, request, redirect, url_for
import os
import ats

# from your_processing_module import process_resume  # Import your processing function

app = Flask(__name__, static_url_path="/static")
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("indexx.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    desc = request.form["jobDescription"]
    if file.filename == "":
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filename)
        # Call your processing script here with the filename as an argument
        # process_resume(filename)
        (
            score,
            match_hard,
            missing_hard,
            match_soft,
            missing_soft,
            word_count,
            sections,
            hs,
            ss,
            wc,
            sc,
        ) = ats.processing(file.filename, 1, desc)
        struct = str(sc) + "%"
        hsp = str(hs) + "%"
        ssp = str(ss) + "%"
        wcp = str(wc) + "%"

        print(match_hard)
        return render_template(
            "result.html", final=score, struct=struct, hsp=hsp, ssp=ssp, wcp=wcp
        )
    else:
        return "Invalid file format! Allowed formats: pdf, docx"


if __name__ == "__main__":
    app.run(debug=True)

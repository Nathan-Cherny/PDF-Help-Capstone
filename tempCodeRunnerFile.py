import os
from flask import Flask, render_template, request, jsonify
import pymupdf 

app = Flask(__name__)


def get_data_from_pdf(pdf_bytes):
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    all_data = []

    for page in doc:
        data = page.get_text("dict")
        parsed_data = []

        for block in data["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    parsed_data.append(
                        {
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"],
                            "bbox": span["bbox"],
                        }
                    )

        all_data.append(parsed_data)

    return all_data

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crop_pdf")
def cropapdf():
    return render_template("cropPdf.html")


@app.route("/see_pdf_text_info", methods=['GET', 'POST'])
def see_pdf_text_info():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
            
        if file:
            # Read the file bytes and pass them to your parser
            pdf_bytes = file.read()
            extracted_data = get_data_from_pdf(pdf_bytes)
            return jsonify(extracted_data)

    # For GET requests, render the page
    return render_template("see_pdf_text_info.html")

app.run(debug=True)

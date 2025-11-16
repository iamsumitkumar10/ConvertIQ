# # app.py
# import os
# import io
# import zipfile
# from flask import Flask, request, render_template_string, send_file, abort
# from werkzeug.utils import secure_filename
# from PyPDF2 import PdfReader, PdfWriter

# app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # max 200MB upload (adjust if needed)

# INDEX_HTML = """
# <!doctype html>
# <html>
#   <head>
#     <meta charset="utf-8">
#     <title>PDF Splitter</title>
#   </head>
#   <body>
#     <h2>PDF Splitter</h2>
#     <form method="post" action="/split" enctype="multipart/form-data">
#       <input type="file" name="pdf_file" accept="application/pdf" required>
#       <br><br>
#       <button type="submit">Enter</button>
#     </form>
#     <p>Ek PDF upload karo; server har page ko alag PDF bana ke ZIP return karega.</p>
#   </body>
# </html>
# """

# @app.route("/")
# def index():
#     return render_template_string(INDEX_HTML)

# @app.route("/split", methods=["POST"])
# def split_pdf():
#     if 'pdf_file' not in request.files:
#         abort(400, "No file part")
#     file = request.files['pdf_file']
#     if file.filename == "":
#         abort(400, "No selected file")
#     filename = secure_filename(file.filename)

#     try:
#         reader = PdfReader(file.stream)
#     except Exception as e:
#         abort(400, f"Invalid PDF: {e}")

#     # Create an in-memory ZIP with all split pages
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
#         for i, page in enumerate(reader.pages):
#             writer = PdfWriter()
#             writer.add_page(page)

#             page_bytes = io.BytesIO()
#             writer.write(page_bytes)
#             page_bytes.seek(0)

#             page_name = f"{os.path.splitext(filename)[0]}_page_{i+1}.pdf"
#             zf.writestr(page_name, page_bytes.read())

#     zip_buffer.seek(0)
#     return send_file(
#         zip_buffer,
#         mimetype="application/zip",
#         as_attachment=True,
#         download_name=f"{os.path.splitext(filename)[0]}_pages.zip"
#     )

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)



import os
import io
import zipfile
from flask import Flask, request, render_template, send_file, abort
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # max 200MB upload

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/split", methods=["POST"])
def split_pdf():
    if 'pdf_file' not in request.files:
        abort(400, "No file part")
    
    file = request.files['pdf_file']
    if file.filename == "":
        abort(400, "No selected file")
    
    filename = secure_filename(file.filename)

    try:
        reader = PdfReader(file.stream)
    except Exception as e:
        abort(400, f"Invalid PDF: {e}")

    # Create an in-memory ZIP with all split pages
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)

            page_bytes = io.BytesIO()
            writer.write(page_bytes)
            page_bytes.seek(0)

            page_name = f"{os.path.splitext(filename)[0]}_page_{i+1}.pdf"
            zf.writestr(page_name, page_bytes.read())

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{os.path.splitext(filename)[0]}_pages.zip"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
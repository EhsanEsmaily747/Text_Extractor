from flask import Flask, request, render_template
import pdfplumber

app = Flask(__name__)

def extract_pdf_text(file_stream):
    result = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row:
                        result.append(row)
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    matches = []
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').split(',')
        pdf_file = request.files.get('pdf_file')
        if pdf_file:
            table_data = extract_pdf_text(pdf_file)
            for row in table_data:
                if any(keyword.strip().lower() in (cell or '').lower() for keyword in keywords for cell in row):
                    matches.append(row)
    return render_template('index.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)

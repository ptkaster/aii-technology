from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_cors import CORS
import random
import htmlParsing as parse
import json

app = Flask(__name__)
CORS(app)

@app.route('/')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.filename = random.randrange(1000000, 99999999999)
        filename = "api_uploaded_files/" + str(uploaded_file.filename) + ".html"
        uploaded_file.save(filename)
        parse.parse_linkedin_to_csv(filename)
    return redirect("file:///Users/ptkaster/Desktop/aii-technology/upload.html")

@app.route('/textinput', methods=['POST'])
def upload_text():
    data = json.loads(request.data)
    html = data['html_body']
    filename = "api_uploaded_files/" + str(random.randrange(1000000, 99999999999)) + ".html"
    with open(filename, 'w') as f:
        f.write(html)
        f.close()
    return parse.ai_output(filename)

@app.route('/get_linkedin_csv', methods=['POST'])
def get_linkedin_csv():
    data = json.loads(request.data)
    html = data['html_body']
    filename = "api_uploaded_files/" + str(random.randrange(1000000, 99999999999)) + ".html"
    with open(filename, 'w') as f:
        f.write(html)
        f.close()
    csv = parse.parse_linkedin_to_csv(filename)
    return csv

if __name__ == "__main__":
    app.run(debug=True, port=8000)

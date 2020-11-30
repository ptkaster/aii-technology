from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_cors import CORS
import random
import htmlParsing as parse
import json
import os.path
import os
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    return redirect("https://annenberg.usc.edu/research/aii", code=302)


@app.route('/loaderio-198f3924fd75b1b73e6fc5855b70c71c/')
def serve_loader_static():
    return app.send_static_file('/temp_images/loaderio-198f3924fd75b1b73e6fc5855b70c71c.txt')

@app.route('/server/pullgithub')
def git_pull():
    try:
        return str(subprocess.run(["git", "pull"]))
        return str(os.system("git pull"))

        os.system("systemctl reboot -i")
        return "Executed command"
    except Exception as asc:
        return str(asc)

@app.route('/static/images/<image>')
def serve_image(image):
    return app.send_static_file('site/images/' + image)

@app.route('/static/html/<html>')
def static_file(html):
    return app.send_static_file('site/html/' + html)

@app.route('/documentation/download_linkedin')
def download_linkedin():
    with open('site/html/download_linkedin.html', 'r') as file:
        return file.read()
    # return app.send_static_file('site/html/download_linkedin.html')

# @app.route('/', methods=['POST'])
# def upload_file():
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         uploaded_file.filename = random.randrange(1000000, 99999999999)
#         filename = "api_uploaded_files/" + str(uploaded_file.filename) + ".html"
#         uploaded_file.save(filename)
#         parse.parse_linkedin_to_csv(filename)
#     return redirect("file:///Users/ptkaster/Desktop/aii-technology/upload.html")

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

# @app.route('/api/mailchimp/initialize', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'mailchimpkey' in request.args and 'accesscode' in request.args:
#         apiCallResult = mailchimp.APICall(request.args['accesscode'], request.args['mailchimpkey'])
#         print(apiCallResult)
#         responseJson = {}
#         if(apiCallResult['success']):
#             responseJson['connected'] = 'true'
#         else:
#             responseJson['connected'] = 'false'
#         responseJson['connectionError'] = apiCallResult['errorCode']
#         # I can't get this to work every time to save my life so here we are
#         try:
#             responseJson['attorneyName'] = apiCallResult['attorneyFirm']
#         except:
#             responseJson['attorneyName'] = ''
#         resp = flask.Response(str(responseJson))
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#         return resp
#     else:
#         responseJson = {}
#         responseJson['connected'] = 'false'
#         responseJson['attorneyName'] = ''
#         responseJson['connectionError'] = "Error: Mailchimp connection could not be established, please double check your key."
#         resp = flask.Response(str(responseJson))
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#         return resp
#
#     return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

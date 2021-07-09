from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# @app.route('/')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")


# @app.route('/api/back_end')
# def test():
#     return {}

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'dist'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/api/covid_graph')
# def covid_graph():
#     return api_functions.covid_graph(app)

if __name__ == "__main__":
    print("server is running on localhost!!")
    # app.run(host='0.0.0.0', port=8050, debug=True)
    app.run(debug=False)
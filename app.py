from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import requests
import mysql.connector as mariadb

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# CONNECTION TO SQL DATABASE (MARIADB)
mariadb_con = mariadb.connect(user='root', password='welcome', host='Localhost', port='3306')
cursor = mariadb_con.cursor(buffered=True)

def initDatabase():
    cursor.execute("CREATE DATABASE IF NOT EXISTS todo_app")
    cursor.execute("USE todo_app")
    cursor.execute("CREATE TABLE IF NOT EXISTS todo_list (id int NOT NULL AUTO_INCREMENT,task TEXT, time TEXT, PRIMARY KEY (id))")
    mariadb_con.commit()

initDatabase()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# @app.route('/')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

@app.route('/api/todo_list/load', methods=['GET'])
def todo_list_load():
    cursor.execute("SELECT * FROM todo_list ORDER BY id DESC")
    # # fetch all the matching rows 
    result = cursor.fetchall()
    
    send_list = []
    # loop through the rows
    for row in result:
        send_list.append({
            "id": row[0],
            "desc": row[1],
            "time": row[2]
            })
    
    send_obj = {"entry_list": send_list}
    return send_obj

@app.route('/api/todo_list/insert', methods=['GET', 'POST'])
def todo_list_insert():
    post_data = request.get_json()
    cursor.execute("INSERT INTO todo_list (task, time) VALUES ('{}', '{}')".format(post_data['desc'],post_data['time']))
    mariadb_con.commit()
    # cursor.execute("SELECT * FROM todo_list ORDER BY id DESC LIMIT 1")
    cursor.execute("SELECT * FROM todo_list ORDER BY id DESC")

    # # fetch all the matching rows 
    result = cursor.fetchall()
    
    # # loop through the rows
    # for row in result:
    #     print(row)
    #     print("\n")
    print(result[0][0])
    send_obj = {"entry_list": [{
                "id": result[0][0],
                "desc": result[0][1],
                "time": result[0][2]
                }]}
    return send_obj

@app.route('/api/todo_list/delete', methods=['GET', 'POST'])
def todo_list_delete():
    post_data = request.get_json()
    print(post_data)
    cursor.execute("DELETE FROM todo_list WHERE id = {}".format(post_data['id']))
    mariadb_con.commit()

    return 'delete done'

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
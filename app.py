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
    cursor.execute("INSERT INTO todo_list (task, time) VALUES (%(tasks)s, %(times)s)", {'tasks': post_data['desc'], 'times': post_data['time']}) # .format(post_data['desc'],post_data['time']))
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

# Delete task based on id from todo_list table
@app.route('/api/todo_list/delete', methods=['POST'])
def todo_list_delete():
    post_data = request.get_json()
    print(post_data)
    cursor.execute("DELETE FROM todo_list WHERE id = {}".format(post_data['id']))
    mariadb_con.commit()

    return 'delete done'

@app.route('/api/todo_list/update', methods=['POST'])
def todo_list_update():
    post_data = request.get_json()
    print(post_data)
    cursor.execute("UPDATE todo_list SET task='{}' WHERE id = {}".format(post_data['desc'], post_data['id']))
    mariadb_con.commit()
    return 'update done'

if __name__ == "__main__":
    print("server is running on localhost!!")
    # app.run(host='0.0.0.0', port=8050, debug=True)
    app.run(debug=False)
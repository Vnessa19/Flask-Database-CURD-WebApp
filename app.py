from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db



db_connection = db.connect_to_database()

# Configuration

app = Flask(__name__)



mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

########## Functions for Users page #################
@app.route('/users', methods=['POST','GET'])
def users():
    if request.method == "GET":
        query = "SELECT user_id as 'ID', user_email as 'Email', user_password as 'Password', user_name as 'Name', user_birthday as 'Birthday'FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        return render_template("users.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Create_User"):
            user_email = request.form["email"]
            user_password = request.form["password"]
            user_name = request.form["name"]
            user_birthday = request.form["dob"]

        query = "INSERT INTO Users (user_email, user_password, user_name, user_birthday) VALUES (%s, %s, %s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query,(user_email, user_password, user_name, user_birthday))
        mysql.connection.commit()
        return redirect("/users")

@app.route('/search_user', methods=['POST'])
def search_user():
        if request.form.get("Search_User"):
            user_email = request.form["email"]
        
        query2 = "SELECT user_id as 'ID', user_email as 'Email', user_password as 'Password', user_name as 'Name', user_birthday as 'Birthday' FROM Users WHERE user_email = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query2, (user_email,))
        data = cur.fetchall()
        if data:
            return render_template("founduser.j2", data=data)
        else:
            return render_template("founduser.j2", message = 'User not found.')

@app.route('/edit_user/<int:ID>', methods=['POST','GET'])
def edit_user(ID):
    if request.method == "GET":
        query = "SELECT * FROM Users WHERE user_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query,(ID,))
        data=cur.fetchall()
        print(data)
        return render_template("edit_user.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_User"):
            user_email = request.form["email"]
            user_password = request.form["password"]
            user_name = request.form["name"]
            user_birthday = request.form["dob"]
            user_id = request.form['userID']

        query = "UPDATE Users SET user_email = %s, user_password = %s, user_name = %s, user_birthday = %s WHERE user_id= %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,(user_email, user_password, user_name, user_birthday, user_id))
        mysql.connection.commit()
        return redirect("/users")
    
@app.route('/delete_user/<int:ID>')
def delete_user(ID):
    query = "DELETE FROM Users WHERE user_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(ID,))
    mysql.connection.commit()

    return redirect("/users")
    
#############################################################

########## Functions for User Favorite page #################
@app.route('/favorite')
def favorite():
    query = "SELECT user_id as 'User ID', user_name as Name, routine_name as `Favorite Routine Name` FROM Users JOIN Favorited_routine_logs ON Users.user_id = Favorited_routine_logs.uid JOIN Routines ON Favorited_routine_logs.rid = Routines.routine_id ORDER BY user_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("favorite.j2", favorite=results)

@app.route('/routines')
def routines():
    query = "SELECT routine_id as ID, routine_name as `Routine Name`, `description` as `Description`, duration as Duration, video_link AS `Video Link`, IFNULL(Equipment.equipment_name, 'None') as `Equipment Required`, Routine_categories.routine_category_name as Category From Routines JOIN Routine_categories ON Routines.routine_category_id = Routine_categories.routine_category_id LEFT JOIN Equipment ON Routines.equipment_id = Equipment.equipment_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("routines.j2", routines=results)

@app.route('/categories')
def categories():
    query = "SELECT routine_category_id as ID, routine_category_name as Name FROM Routine_categories;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("categories.j2", categories=results)

@app.route('/equipment')
def equipment():
    query = "SELECT equipment_id as ID, equipment_name as Name FROM Equipment;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("equipment.j2", equipment=results)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 21295)) 
    app.run(port=port, debug=True)
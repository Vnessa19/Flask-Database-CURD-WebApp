from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db
from database.db_credentials import host, user, passwd, db
from database.db_connector import connect_to_database, execute_query

# Citation Scope: Flask and database connection set up on filp and each CRUD operation
# Date: 11/07/2023
# Originality: Adapted
# Source: https://github.com/osu-cs340-ecampus/flask-starter-app


#db_connection = db.connect_to_database()

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = db
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

########## Functions for Users page, read/create/update/delete functions#################
#### Read and Create operation for users
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

#### Update operation for users
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

#### Delete operation for users
@app.route('/delete_user/<int:ID>')
def delete_user(ID):
    query = "DELETE FROM Users WHERE user_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(ID,))
    mysql.connection.commit()

    return redirect("/users")
    
#############################################################

########## Functions for User Favorite page, read/create/update/delete functions#################
#### Read and Create operation for favorite
@app.route('/favorite',  methods=['POST','GET'])
def favorite():
    if request.method == "GET":
        query = "SELECT log_id as 'ID', user_email as 'User email', user_name as 'User Name', routine_name as 'Favorite Routine Name' FROM Users JOIN Favorited_routine_logs ON Users.user_id = Favorited_routine_logs.uid JOIN Routines ON Favorited_routine_logs.rid = Routines.routine_id ORDER BY user_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        query1 = 'SELECT user_email FROM Users;'
        cur = mysql.connection.cursor()
        cur.execute(query1)
        emails = cur.fetchall()

        query2 = 'Select routine_name From Routines;'
        cur = mysql.connection.cursor()
        cur.execute(query2)
        routines = cur.fetchall()

        return render_template("favorite.j2", data=data, emails=emails, routines=routines)

    if request.method == "POST":
        if request.form.get("Create_Log"):
            user_email = request.form["email"]
            routine_name = request.form["routine_name"]

        query1 = "SELECT log_id , user_email,routine_name FROM Users JOIN Favorited_routine_logs ON Users.user_id = Favorited_routine_logs.uid JOIN Routines ON Favorited_routine_logs.rid = Routines.routine_id WHERE user_email = %s AND routine_name = %s;"
        cur = cur = mysql.connection.cursor()
        cur.execute(query1,(user_email,routine_name))
        checkdata = cur.fetchall()
        if checkdata:
            return render_template("favorite2.j2", message = 'You already have favorite this routine.')

        query = "INSERT INTO Favorited_routine_logs (uid, rid) VALUES ((SELECT user_id FROM Users WHERE user_email = %s), (SELECT routine_id FROM Routines WHERE routine_name = %s));"
        cur = mysql.connection.cursor()
        cur.execute(query,(user_email,routine_name))
        mysql.connection.commit()
        return redirect("/favorite")

#### Update operation for favorite
@app.route('/edit_log/<int:ID>', methods=['POST','GET'])
def edit_log(ID):
    if request.method == "GET":
        query = "SELECT log_id, user_email, routine_name FROM Users JOIN Favorited_routine_logs ON Users.user_id = Favorited_routine_logs.uid JOIN Routines ON Favorited_routine_logs.rid = Routines.routine_id WHERE log_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,(ID,))
        data=cur.fetchall()
        

        query2 = 'Select routine_name From Routines;'
        cur = mysql.connection.cursor()
        cur.execute(query2)
        routines = cur.fetchall()
        
        return render_template("edit_log.j2", data=data, routines=routines)
    
    if request.method == "POST":
        if request.form.get("Edit_Log"):
            routine_name = request.form["routine_name"]
            user_email = request.form["email"]

        query1 = "SELECT log_id , user_email,routine_name FROM Users JOIN Favorited_routine_logs ON Users.user_id = Favorited_routine_logs.uid JOIN Routines ON Favorited_routine_logs.rid = Routines.routine_id WHERE user_email = %s AND routine_name = %s;"
        cur =  mysql.connection.cursor()
        cur.execute(query1,(user_email,routine_name))
        checkdata = cur.fetchall()
        if checkdata:
            return render_template("favorite2.j2", message = 'You already have favorite this routine.')
            
        query = "UPDATE Favorited_routine_logs SET rid = (SELECT routine_id FROM Routines WHERE routine_name = %s) WHERE uid = (SELECT user_id FROM Users WHERE user_email = %s);"
        cur = mysql.connection.cursor()
        cur.execute(query,(routine_name, user_email))
        mysql.connection.commit()
        return redirect("/favorite")

#### Delete operation for favorite
@app.route('/delete_log/<int:ID>')
def delete_log(ID):
    query = "DELETE FROM Favorited_routine_logs WHERE log_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(ID,))
    mysql.connection.commit()

    return redirect("/favorite")

#############################################################################################

########## Functions for Routines page, read/create/update/delete functions #################
#### Read and Create operation
@app.route('/routines', methods=['POST','GET'])
def routines():
    if request.method == "GET":
        query = "SELECT routine_id as ID, routine_name as `Name`, `description` as `Description`, duration as Duration, video_link AS `Video Link`, IFNULL(Equipment.equipment_name, 'None') as `Equipment Required`, Routine_categories.routine_category_name as Category From Routines JOIN Routine_categories ON Routines.routine_category_id = Routine_categories.routine_category_id LEFT JOIN Equipment ON Routines.equipment_id = Equipment.equipment_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query1 = 'SELECT equipment_id as ID, equipment_name FROM Equipment;'
        cur = mysql.connection.cursor()
        cur.execute(query1)
        equipments = cur.fetchall()

        query2 = 'SELECT routine_category_id as ID, routine_category_name From Routine_categories;'
        cur = mysql.connection.cursor()
        cur.execute(query2)
        categories = cur.fetchall()

        return render_template("routines.j2", data=data, equipments=equipments, categories=categories)
    
    if request.method == "POST":
        if request.form.get("Create_Routine"):
            routine_name = request.form["routine"]
            description = request.form["description"]
            duration = request.form["duration"]
            video_link = request.form["video"]
            equipment = request.form["equipment"]
            category = request.form["category"]
            
        if equipment == "":
            query = "INSERT INTO Routines (routine_name, description, duration, video_link, routine_category_id) VALUES (%s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query,(routine_name, description, duration, video_link, category))
            mysql.connection.commit()
            
        else:
            query = "INSERT INTO Routines (routine_name, description, duration, video_link, equipment_id, routine_category_id) VALUES (%s, %s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query,(routine_name, description, duration, video_link, equipment, category))
            mysql.connection.commit()
        return redirect("/routines")

#### Update operation for Routines
@app.route('/edit_routine/<int:ID>', methods=['POST','GET'])
def edit_routine(ID):
    if request.method == "GET":
        query = "SELECT routine_id, routine_name, description, duration as Duration, video_link, IFNULL(Equipment.equipment_name, 'None'), Routine_categories.routine_category_name as Category From Routines JOIN Routine_categories ON Routines.routine_category_id = Routine_categories.routine_category_id LEFT JOIN Equipment ON Routines.equipment_id = Equipment.equipment_id WHERE Routine_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query,(ID,))
        data=cur.fetchall()

        query1 = 'SELECT equipment_id as ID, equipment_name FROM Equipment;'
        cur = mysql.connection.cursor()
        cur.execute(query1)
        equipments = cur.fetchall()

        query2 = 'SELECT routine_category_id as ID, routine_category_name From Routine_categories;'
        cur = mysql.connection.cursor()
        cur.execute(query2)
        categories = cur.fetchall()
        return render_template("edit_routine.j2", data=data, equipments=equipments, categories=categories)

    if request.method == "POST":
        if request.form.get("Edit_Routine"):
            routine_name = request.form["routine"]
            description = request.form["description"]
            duration = request.form["duration"]
            video_link = request.form["video"]
            equipment = request.form["equipment"]
            category = request.form["category"]
            routine_id = request.form["routineID"]
            
        if equipment == "":
            query = "UPDATE Routines SET routine_name = %s, description = %s, duration = %s, video_link= %s, routine_category_id = %s WHERE routine_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query,(routine_name, description, duration, video_link, category, routine_id))
            mysql.connection.commit()
            
        else:
            query = "UPDATE Routines SET routine_name = %s, description = %s, duration = %s, video_link= %s, equipment_id = %s, routine_category_id = %s WHERE routine_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query,(routine_name, description, duration, video_link, equipment, category, routine_id))
            mysql.connection.commit()
        return redirect("/routines")

#### Delete operation for Routines
@app.route('/delete_routine/<int:ID>')
def delete_routine(ID):
    query = "DELETE FROM Routines WHERE routine_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(ID,))
    mysql.connection.commit()

    return redirect("/routines")
#############################################################################################

########## Functions for Routine_categories page, create/read ###############################
#### Read operation
@app.route('/categories', methods=['POST','GET'])
def categories():
    if request.method == "GET":
        query = "SELECT routine_category_id as 'ID', routine_category_name as Name FROM Routine_categories;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        return render_template("categories.j2", data=data)

#### Create operation 
    if request.method == "POST":
        if request.form.get("Create_Category"):
            routine_category_name = request.form["category"]

        query = "INSERT INTO Routine_categories (routine_category_name) VALUES (%s);"
        cur = mysql.connection.cursor()
        cur.execute(query,(routine_category_name,))
        mysql.connection.commit()
        return redirect("/categories")


########## Functions for Equipment page, create/read #########################################
#### Read operation
@app.route('/equipment', methods=['POST','GET'])
def equipment():
    if request.method == "GET":
        query = "SELECT equipment_id as 'ID', equipment_name as 'Name' FROM Equipment;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        return render_template("equipment.j2", data=data)

#### Create operation 
    if request.method == "POST":
        if request.form.get("Create_Equipment"):
            equipment_name = request.form["equipment"]

        query = "INSERT INTO Equipment (equipment_name) VALUES (%s);"
        cur = mysql.connection.cursor()
        cur.execute(query,(equipment_name,))
        mysql.connection.commit()
        return redirect("/equipment")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3891)) 
    app.run(port=port, debug=True)
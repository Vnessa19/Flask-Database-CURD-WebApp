from flask import Flask, render_template, json
import os
import database.db_connector as db


db_connection = db.connect_to_database()

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/users')
def users():

    # Write the query and save it to a variable
    query = "SELECT user_email as 'Email', user_password as 'Password', user_name as 'Name', user_birthday as 'Birthday'FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("users.j2", users=results)

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
from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)

# MySQL database configuration
#db_config = {
#    'host': db_server, 
#    'user': db_user,   
#    'password': db_password,
#    'database': db_database
#}

@app.route('/')
def index():
    try:
        # Connect to the database
        conn = mysql.connector.connect(host=db_server,user=db_user,password=db_password,database=db_database)
        cursor = conn.cursor(dictionary=True)
        
        # Query to fetch all rows from the items table
        cursor.execute("SELECT * FROM items;")
        items = cursor.fetchall()  # Fetch all rows
        
        # Close connection
        cursor.close()
        conn.close()
        
        # Pass the items to the template
        return render_template('index.html.tmpl',hostname=app_hostname,version=app_version, items=items)
        
    except mysql.connector.Error as err:
        return f"Error: {err}"



app_hostname = os.getenv('HOSTNAME',None)
app_version = "version1"
app_port = os.getenv('APP_PORT','5000')
    
db_server   = os.getenv('DB_SERVER',None)
db_user     = os.getenv('DB_USER',None)
db_password = os.getenv('DB_PASSWORD',None)
db_database = os.getenv('DB_DATABASE',None)
    
app.run(debug=True,host="0.0.0.0",port=app_port)

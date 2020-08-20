# -*- coding: utf-8 -*-
"""
Author: Pandurang Pampatwar
Date: Created: 4th July 2020
Purpose:
    1. This is the main script file which brings all the files together such as database, html files and log
       files.
    2. Create connection to the database
    3. Update the database with newly created database.
    4. Fetch the details of the complaint using provided reference number.
    5. Establish connection between different html pages.

"""
from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error
import logging
from joblib import load
app = Flask(__name__)

#log file configuration
FILE_NAME = 'complaints_log.txt'
Database = 'complaints_log.db'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=FILE_NAME,
                    filemode='w')

# Function to create connection to the database.
def create_connection(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
        logging.info('Connected successfully to '+Database)
        return conn
    except Error as e:
        print(e)
    return conn

# Function to insert data of new complaint into the database.
def insert_new_record(record):
    conn = create_connection(".\complaints_log.db")
    cursor = conn.cursor()
    sql_command = """ INSERT INTO complaints(Name, OrderID, OrderDate, Product, Category, UserNarrative, Status, ReferenceNumber)
            values(?,?,?,?,?,?,?,?) """
    record.append("Pending")   #setting the status of new complaint as pending.
    reference = record[0][:3]+record[1][:4]  #Generating the reference number for new complaint for future reference.
    record.append(reference)
    
    cursor.execute(sql_command, record)
    cursor.execute("commit")   #making the changes to database.
    cursor.close()
    conn.close()
    return reference

# To receive all the details of past complaint using reference number
def get_details(referenceNumber):
    conn = create_connection(".\complaints_log.db")
    cursor = conn.cursor()
    refno = '"'+referenceNumber+'"'
    sql_command = f"""Select * from complaints where ReferenceNumber == {refno}"""
    cursor.execute(sql_command)
    details = cursor.fetchall()
    cursor.close()
    conn.close()
    return details
    
conn = create_connection(".\complaints_log.db")
cursor = conn.cursor()

# Home page providing the links for making or tracking the complaint.
@app.route('/')
def home_page():
    htmlcode = """ <!DOCTYPE html> <html> <head> <style>
    a:link, a:visited {
    background-color: #f44336;
    color: white;
    padding: 14px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    }

    a:hover, a:active {
    background-color: red;
    }
    .diff {
    color: #f44336;
    font-family:Impact;
    font-size:200%; 
    }
    </style> </head>
    <body style="background-color:orange; text-align:center">
    <h1>
    <span class="diff">Turbo </span>
    <span class="common">Logistics</span>
    </h1>
    <a href="/complaints.html" target="_blank">Lodge Complaint</a> <br> <br>
    <a href="/Track Complaints.html" target="_blank">Track Complaint</a>  </body></html> """
    return htmlcode

# Function to register a complaint.
@app.route('/complaints.html', methods=['POST', 'GET'])
def  reg_complaints():
    complaint_data=[]
    description=[]
    referenceNumber=""
    if request.method == 'POST':
        try:
            complaint_data.append(request.form['name'])
            complaint_data.append(request.form['orderid'])
            complaint_data.append(request.form['orderdate'])
            complaint_data.append(request.form['product'])
            description.append(request.form['description'])
            # Importing the saved model for predicting category.
            prediction_model = load('model.pkl')

            #saving the output of the model to send it further for database update.
            category = prediction_model.predict(description)
            complaint_data.append(category[0])
            complaint_data.append(description[0])
            referenceNumber = insert_new_record(complaint_data)
            logging.info('New complaint registered successfully')

        except:
            referenceNumber = "Error"
            logging.exception(referenceNumber)
    return render_template('complaints.html', referenceNumber=referenceNumber)

# Function to track a complaint.
@app.route('/Track Complaints.html', methods=['POST','GET'])
def track_complaints():
    details = ""
    if request.method == 'POST':
        try:
            referenceNumber = request.form['refno']
            details = get_details(referenceNumber)
            logging.info('Data retrieved successfully')
        except:
            details="Not found"
            logging.info(details)
            
    return render_template('Track Complaints.html', details=details)

app.run()
"""
Results:
    1. Established connection to the database successfully.
    2. New complaint data saved to database successfully.
    3. Data retrieved from the database successfully.
    4. Connection between different html pages was tested successfully.

"""

from flask import Flask, jsonify, request, render_template
import mysql.connector
import requests
import datetime, time
from mysql.connector import Error

app = Flask(__name__)

'''Code to convert unix to valid time'''
# import datetime
# print(
#     datetime.datetime.fromtimestamp(
#         int("1284105682")
#     ).strftime('%H:%M:%S')
# )
'''Unix time end'''

''' Fetch data from DB'''


def fetch_from_DB():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proj_contestlist',
                                             user='root',
                                             password='Rohan@1215')
        cursor = connection.cursor(dictionary=True)
        sql_fetch_query = "select * from temp_table order by startTime ASC"
        cursor.execute(sql_fetch_query)
        records = cursor.fetchall()
        # print(records)
        # print(len(records))
    except Error as e:
        print("Error reading data from MySQL table", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return records
    # pass


'''Fetch End !'''


# Home page that returns an html page !!
@app.route('/')
def home_page():
    return render_template('Home.html')

# returns emailPage
@app.route('/emailPage')
def ask_email_page():
    return render_template('emailPage.html')

# Insert data into emailTable as per users choice
@app.route('/postEmail',methods=["POST"])
def postEmail():
    pass

# api to fetch data from our DB
@app.route('/contests')
def get_contests_from_DB():
    records = fetch_from_DB()
    # print(records)
    for index, row in enumerate(records):
        curr_time = int(time.time())
        if (curr_time < row['startTime']):
            # phase = before
            row['phase'] = 'Before'
        elif (row['endTime'] > curr_time >= row['startTime']):
            # phase coding
            row['phase'] = 'Coding'
        else:
            # phase ended
            row['phase'] = 'Ended'
    return {'records': records}


# print(int(time.time()))
app.run(port=5000)

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

''' Get details about a specific contest '''
def get_contest_details(contestId):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proj_contestlist',
                                             user='root',
                                             password='Rohan@1215')
        cursor = connection.cursor(dictionary=True)
        sql_fetch_query = """select * from temp_table where id=%s"""
        cursor.execute(sql_fetch_query,(contestId,))
        records = cursor.fetchone()
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

'''Get details end'''

'''Post email and timing details '''
def insert_email(details):
    # details tuple is what we want insert
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proj_contestlist',
                                             user='root',
                                             password='Rohan@1215')
        cursor = connection.cursor()
        sql_insert_query = """INSERT INTO email_table (contestId,contestName,emailAddress,sendTime) values (%s,%s,%s,%s)"""
        cursor.execute(sql_insert_query, details)
        connection.commit()
        print("Success")
        # print(records)
        # print(len(records))
    except Error as e:
        print("Error inserting data from MySQL table", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


'''POST END'''
def Hrs_to_seconds(Hrs):
    if Hrs == "1hr":
        return 3600
    elif Hrs == "12hr":
        return 12*3600
    elif Hrs == "24hr":
        return 24*3600
    else:
        return 0

# Home page that returns an html page !!
@app.route('/')
def home_page():
    return render_template('Home.html')

# returns emailPage
@app.route('/emailPage')
def ask_email_page():
    return render_template('emailPage.html')

# Insert data into emailTable as per users choice
@app.route('/postEmail', methods=['POST'])
def postEmail():
    # The response format is
    # request={
    #                 "emailId":temp_emailId,
    #                 "contestId":temp_contestId,
    #                 "emailTimeBefore":temp_emailTime
    #          }
    response = request.get_json()

    # get details about the contest using contestID
    contest_details = get_contest_details(response['contestId'])   # this is a dictionary

    # Calculate time of send in UNIX
    CutTime = Hrs_to_seconds(response['emailTimeBefore'])
    sendTime = contest_details['startTime'] - CutTime

    # Now insert the data required for email table !
    insert_tuple = (int(response['contestId']), contest_details['contest_name'], response['emailId'], sendTime)
    insert_email(insert_tuple)

    return jsonify(response)

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
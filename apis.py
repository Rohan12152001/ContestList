from flask import Flask, jsonify, request, render_template
import mysql.connector,sys
import requests
import datetime, time
from mysql.connector import Error

app = Flask(__name__)

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
    except Error as e:
        print("Error reading data from MySQL table", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return records

'''Get details end'''

'''Insert email and timing details '''
def insert_email(details):
    # "details" tuple is what we want insert
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
    except Error as e:
        print("Error inserting data in MySQL table", e)

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

def formatDateTime(givenTime):
    return datetime.datetime.fromtimestamp(
        int(givenTime)
    ).strftime('%d-%m-%Y || %H:%M:%S')

# Home page that returns an html page !!
@app.route('/')
def home_page():
    return render_template('Home.html')

# returns emailPage
@app.route('/emailPage')
def ask_email_page():
    # conID=request.args.get('contestId')
    # print("conetestID is:", conID) #  comment hai
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
# TODO: (DONE) Add contestTime, duration and endTime as formatted IST times and pass them in the JSON
@app.route('/contests')
def get_contests_from_DB():
    records = fetch_from_DB()
    # print(records)

    # record format
    # {'id': 1457, 'contest_name': 'Codeforces Round #687 (Div. 2, based on Technocup 2021 Elimin
    # ation Round 2)', 'duration_seconds': 7200, 'startTime': 1606633500, 'endTime': 1606640700}
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
        startTimeFormatted = formatDateTime(row['startTime'])
        endTimeFormatted = formatDateTime(row['endTime'])
        durationFormatted = row['duration_seconds'] // 3600  # This is in hrs
        row['startTimeFormatted'] = startTimeFormatted
        row['endTimeFormatted'] = endTimeFormatted
        row['durationFormatted'] = durationFormatted
    return {'records': records}

# This is a function !
def get_Min_ContestTime():
    Temp_records = get_contests_from_DB()
    min_ContestTime = sys.maxsize
    for record in Temp_records['records']:
        if(record['startTime'] < min_ContestTime and record['phase']=='Before'):
            min_ContestTime = record['startTime']
    return min_ContestTime

# returns emailPage
@app.route('/emailPageSubAll')
def ask_email_page_SubAll():
    # conID=request.args.get('contestId')
    # print("conetestID is:", conID) #  comment hai
    MinContestTime = get_Min_ContestTime()
    return render_template('emailPageSubAll.html', MinContestTime=MinContestTime)

# print(int(time.time()))
app.run(port=5000)

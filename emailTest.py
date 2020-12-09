import smtplib, ssl
import mysql.connector
from mysql.connector import Error
import time
import datetime

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

'''Time formatting'''
def formatTime(contestTime):
    return datetime.datetime.fromtimestamp(
        int(contestTime)
    ).strftime('%H:%M:%S')
''' END '''

'''Format Date'''
def formatDate(contestTime):
    return datetime.datetime.fromtimestamp(
        int(contestTime)
    ).strftime('%Y-%m-%d')
'''END'''

# The essentials for connecting to G-mail
smtp_server = "smtp.gmail.com"
port = 587                                                                         # For starttls the port number is 587
sender_email = "emailtester1215@gmail.com"

# TODO: Change the way of accepting passwords by using envVariables
password = input("Enter email password: ")                                         # Not a good practice
subject = "Reminder from ContestList"


''' Note: time & duration are given as UNIX time you must convert them into required formats '''
def send_Email(receiver_email, contestTime, duration, contestName):
    contestTimeFormatted = formatTime(contestTime)
    contestDateFormatted = formatDate(contestTime)
    contestDurationFormatted = duration//3600               # In hours
    # print(contestTimeFormatted,contestDateFormatted,contestDurationFormatted)  ## comment OUT
    body = f'You have a contest scheduled at {contestTimeFormatted} hrs on {contestDateFormatted} (YYYY-MM-DD) \n ' \
           f'Contest Name : {contestName} which is expected to run for {contestDurationFormatted} hrs.'
    message = f'Subject:{subject}\n\n{body}'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        # Try to log in to server and send email
        try:
            # server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("Email Sent !")
        except Exception as e:
            # Print any error messages to stdout
            print("Error is: ", e)


# This query returns all the email_Info that has to be sent at that moment
def query_for_emailJob(givenTime):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proj_contestlist',
                                             user='root',
                                             password='Rohan@1215')
        cursor = connection.cursor(dictionary=True)
        sql_fetch_query = "select contestId,contestName,emailAddress from email_table where sendTime=%s"
        cursor.execute(sql_fetch_query, (givenTime,))
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


# This job is expected to run in the background
def email_job():
    # call this job after every 5sec
    while True:
        time_now = (int(time.time()))
        email_to_these_records = query_for_emailJob(1607542500)     # This is a dictionary
        # The records format is:
        # [{'contestId': 1501, 'contestName': 'Dummy data', 'emailAddress': 'emailtester1215@gmail.com'}]

        if len(email_to_these_records) > 0:
            for record in email_to_these_records:
                # get details about the contest
                current_contest_details = get_contest_details(record['contestId'])
                receiver_email=record['emailAddress']
                contestTime=current_contest_details['startTime']
                duration=current_contest_details['duration_seconds']
                contestName=record['contestName']
                # print(receiver_email,contestTime,duration,contestName)   # Comment
                send_Email(receiver_email,contestTime,duration,contestName)
        time.sleep(1)

# Call the JOB
email_job()

# TODO: Upgrade the Note after pushing the required changes
'''NOTE : The current script takes a lot of time to send emails need to optimise '''





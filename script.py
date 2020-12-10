from flask import Flask,jsonify,request,render_template
import mysql.connector
import requests
import time
import datetime
from mysql.connector import Error
from mysql.connector import errorcode

'''Function to insert data as fetched by  Update_DB()'''
def insertIntoTable(id, name, duration, startTime, endTime):
    # endTime= startTime + duration
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proj_contestlist',
                                             user='root',
                                             password='Rohan@1215')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO temp_table (id,contest_name,duration_seconds,startTime,endTime) 
                                        VALUES (%s, %s, %s, %s, %s) """
        recordTuple=(id,name,duration,startTime,endTime)
        cursor.execute(mySql_insert_query, recordTuple)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Main func() gets data from api and calls another to insert data !!
def Update_DB():
    while True:
        url="https://codeforces.com/api/contest.list?gym=false"    # to get all contests Codeforces !!
        response=requests.request("GET",url)
        response=response.json()
        # print(response.result[0].id)
        # print(response['result'][0]['id'])
        iterate=0
        # length_of_response=print(len(response['result']))
        while(response['result'][iterate]['phase']=='BEFORE'):
            id=response['result'][iterate]['id']
            name=response['result'][iterate]['name']
            duration=response['result'][iterate]['durationSeconds']
            startTime=response['result'][iterate]['startTimeSeconds']
            endTime=startTime+duration
            insertIntoTable(id,name,duration,startTime,endTime)
            iterate+=1
        time.sleep(3600)

    #return

Update_DB()




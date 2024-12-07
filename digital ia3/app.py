from flask import Flask, render_template, request, session, url_for, redirect
import pandas as pd
import sqlite3
import hashlib
from urllib.request import urlopen
import json
from datetime import datetime


def encrypt(text):
    # convert to byte form
    text_bytes = str.encode(text)
    # hex digest the text using sha256
    textEncrypted = hashlib.sha256(text_bytes).hexdigest()
    return textEncrypted

# database name
__DBNAME__ = "IA3.db"
# api url
url_text = "https://app.ticketmaster.com/discovery/v2/events.json?countryCode=AU&classificationName=music&dmaId=703&apikey=cCeZP8CSZLVdhoQD1ny8VXlGLyWbX3ts"


app = Flask(__name__)
app.secret_key = 'x'

# google maps api key
Key = 'AIzaSyDzuFaLQm2fRi8KgjdBh72jiEqEgXziHqc'

def reset_database(__DBNAME__, url_text, admin_id): 
    # download new data, sort through data, insert into database, update the last updated time
    # import the json and save to a file
    with urlopen(url_text) as url:
        data = json.loads(url.read().decode())
        # w clears the file
        with open("data.json", "w") as file:
            file.write(json.dumps(data))

    # connect to the database
    conn = sqlite3.connect(__DBNAME__)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    #fully clear the database
    cur.execute("""
                DELETE FROM Venues
                """)
    conn.commit()
    cur.execute("""
                DELETE FROM Images
                """)
    conn.commit()
    cur.execute("""
                DELETE FROM Attractions
                """)
    conn.commit()
    cur.execute("""
                DELETE FROM Events
                """)
    conn.commit()

    with open("data.json", "r") as d:
        data = json.load(d)
        events = data["_embedded"]["events"]
        for event in events:
            eventName = event["name"]
            eventUrl = event["url"]
            startDate = event["dates"]["start"]["localDate"]
            genre = event["classifications"][0]["genre"]["name"]
            subGenre = event["classifications"][0]["subGenre"]["name"]
        
            #insert event data into database
            cur.execute(""" INSERT INTO Events (eventName, eventUrl, startDate, genre, subGenre)
                            VALUES (?,?,?,?,?)""",
                            (eventName, eventUrl, startDate, genre, subGenre)
                            )
            conn.commit()

            #get eventID
            cur.execute(""" SELECT eventID
                            FROM Events
                            WHERE eventName=? AND eventUrl=? AND startDate=? AND genre=? AND subGenre=?""",
                            (eventName, eventUrl, startDate, genre, subGenre)
                            )
            eventID = int(cur.fetchone()['eventID'])
            print(eventID)

            venues = event["_embedded"]["venues"]
            for venue in venues:
                venueName = venue["name"]
                venueUrl = venue["url"]
                longitude = venue["location"]["longitude"]
                latitude = venue["location"]["latitude"]

                #insert venue data into database

                cur.execute(""" INSERT INTO Venues (eventID, venueName, venueUrl, longitude, latitude)
                            VALUES (?,?,?,?,?)""",
                            (eventID, venueName, venueUrl, longitude, latitude)
                            )
                conn.commit()

            attractions = event["_embedded"]["attractions"]
            for attraction in attractions:
                attractionName = attraction["name"]
                attractionUrl = attraction["url"]

                #insert attraction data into database
                cur.execute(""" INSERT INTO Attractions (eventID, attractionName, attractionUrl)
                            VALUES (?,?,?)""",
                            (eventID, attractionName, attractionUrl)
                            )
                conn.commit()

            images = event["images"]
            for image in images:
                imageUrl = image["url"]
                imageWidth = image["width"]
                imageHeight = image["height"] 

                #insert image data into database
                cur.execute(""" INSERT INTO Images (eventID, imageUrl, imageWidth, imageHeight)
                            VALUES (?,?,?,?)""",
                            (eventID, imageUrl, imageWidth, imageHeight)
                            )
                conn.commit()

    # change the last updated time
    conn.commit()
    current_time=datetime.now().strftime("%Y/%m/%d %H:%M")
    cur.execute(""" INSERT INTO Data (updateTime, administratorID)
                    VALUES (?, ?)""",
                (current_time, int(admin_id)))
    conn.commit()
    # close the database
    conn.close()

# Adapted from Mr Hurwood's PTapp

@app.route('/')
def index(): # get sql data to display all events
     # CONNECT to database
    conn = sqlite3.connect(__DBNAME__)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
            """ SELECT *
                FROM Events""")
    
    eventData = cur.fetchall()
    conn.close()


    return render_template('index.html', eventData=eventData)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # when the submit button on login.html is clicked
    if request.method == 'POST':
        # collect username and password from login form
        username = request.form['Username']
        password = request.form['Password']

        # SQL injection protection
        pUsername = username.replace("'","\\'")

        # one way encrypt password
        passwordEncrypted = encrypt(password)

        # CONNECT to database
        conn = sqlite3.connect(__DBNAME__)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

            # get Names and passwords from database
        cur.execute(
            """ SELECT administratorID, username, passwordEncrypted FROM Administrators WHERE username = ?""",
                (pUsername,),
        )
        results = cur.fetchall()
        conn.close()

        # FOR EACH record
        for result in results:
            # IF login username and password match with database id and password
            if username == result["Username"] and passwordEncrypted == result["passwordEncrypted"]:
                session["administratorID"] = result["administratorID"]
                return redirect(url_for("administratorportal")) 
            #error message:
        return render_template("login.html", msg="Invalid username or password")
    
    elif request.method == 'GET': #if button on home page is clicked
         return render_template("login.html")
    
@app.route('/logout')
def logout():
    try:
        session.pop('administratorID', None)
    except:
        pass
    return redirect(url_for('index'))


@app.route('/administratorportal', methods=['POST', 'GET']) 
def administratorportal():
    # Connect to the database
    conn = sqlite3.connect(__DBNAME__)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute(
        """SELECT *
            FROM Data d, Administrators a
            WHERE a.administratorID = d.administratorID
            ORDER BY d.updateNumber DESC
            """,)
    Data = cur.fetchall()



    conn.close()
    return render_template('administratorportal.html', Data=Data)

@app.route("/updatedata", methods=["POST", "GET"])
def updatedata():

    # reset the database
    reset_database(__DBNAME__, url_text, session['administratorID'])

    # Reload the administrator portal with updated information
    return redirect(url_for("administratorportal"))
    
@app.route('/eventsearch', methods=['GET', 'POST'])
def eventsearch():
    if request.method == "POST":
        searchTerm = request.form["searchTerm"]
        # sql injection protection
        pSearchTerm = searchTerm.replace("'","\\'")
        # this means the search term in any location for the like statement
        searchTerm_universal = "%"+pSearchTerm+"%"


        conn = sqlite3.connect(__DBNAME__)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(""" 
            SELECT DISTINCT e.eventID, e.eventName, e.startDate, e.genre, e.subGenre
            FROM Events e, Attractions a, Venues v
            WHERE (e.eventName LIKE ? OR e.genre LIKE ? OR e.subGenre LIKE ? OR e.startDate LIKE ?) OR 
            ((a.attractionName LIKE ?) AND e.eventID=a.eventID) OR ((v.venueName LIKE ?)AND e.eventID=v.eventID)""",
            (searchTerm_universal, searchTerm_universal, searchTerm_universal, searchTerm_universal, searchTerm_universal, searchTerm_universal))
        Events = cur.fetchall()
        
        conn.close()

        return render_template('eventsearch.html', Events=Events, searchTerm=searchTerm)

@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == "GET":
        eventID = int(request.args.get("id"))

        conn = sqlite3.connect(__DBNAME__)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
  
        cur.execute(
            """ SELECT *
                FROM Events
                WHERE eventID=?""", (eventID,))
        event = cur.fetchone()

        cur.execute(
            """ SELECT *
                FROM Venues
                WHERE eventID=?""", (eventID,))
        Venues = cur.fetchall()

        cur.execute(
            """ SELECT *
                FROM Attractions
                WHERE eventID=?""", (eventID,))
        Attractions = cur.fetchall()

        cur.execute(
            """ SELECT *
                FROM Images
                WHERE eventID=?""", (eventID,))
        Images = cur.fetchall()

        conn.close()

        return render_template('event.html', event=event, Venues=Venues, Attractions=Attractions, Images=Images, Key=Key)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error
from db import dbconnection
import sys
app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/journals")
def journal():
    rows = findAllJournals()
    return render_template("journals.html", journals=rows)


@app.route("/newjournal")
def JournalProgress():
    return render_template("newjournal.html")


@app.route("/result")
def Result():
    return render_template("result.html")


@app.route("/addJournal", methods=['POST'])
def addJournal():
    msg = ""
    try:
        # Insert to DB
        title = request.form['title']
        date = request.form['date']
        author = request.form['author']
        tag = request.form['tag']
        emotion = request.form['emotion']
        content = request.form['content']
        print("Everything parsed!")

        con = dbconnection()
        cur = con.cursor()
        cur.execute("INSERT INTO Journal(title, date, author, tag, emotions, content) VALUES(?,?,?,?,?,?); ",
                    (title, date, author, tag, emotion, content))

        con.commit()
        print("Data inserted!")
        msg = "Journal successfully saved"
        return redirect("/journals")
    except Error as e:
        print("Hey there is an error: " + e)
        msg = e
    finally:
        # cur.close()
        # con.close()
        return render_template("result.html", msg=msg)


@app.route("/delete/<int:id>")
def deleteJournal(id):
    try:
        con = dbconnection()
        cur = con.cursor()
        cur.execute("DELETE FROM Journal WHERE id = ?", (str(id),))
        con.commit()
        msg = "Journally succesfully deleted!"
        return render_template("result.html", msg=msg)
    except Error as e:
        print("Error " + e)
        con.rollback()
        msg = "There is an error while deleting this journal"
    finally:
        cur.close()
        con.close()


@app.route("/edit/<int:id>")
def editJournal(id):
    try:
        con = dbconnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM Journal WHERE id = ?", (str(id),))
        row = cur.fetchone()
        if row:
            return render_template("editJournal.html", aJournal=row)
        else:
            msg = "Cannot find the journal with this id"
    except Error as e:
        print("There is an error " + e)
        msg = e
    finally:
        cur.close()
        con.close()


@ app.route("/update", methods=["POST"])
def updateJournal():
    msg = ""
    try:
        _id = request.form['id']
        title = request.form['title']
        date = request.form['date']
        # author = request.form['author']
        tag = request.form['tag']
        emotion = request.form['emotion']
        content = request.form['content']

        con = dbconnection()
        cur = con.cursor()
        cur.execute("UPDATE Journal SET title = ?, date = ?, content = ?, emotions = ?, tag = ? WHERE id = ?", (
            title, date, content, emotion, tag, _id))

        con.commit()
        msg = "Journal succesfully updated"
        return redirect("/journals")
    except Error as e:
        print("Error " + e)
        con.rollback()
        msg = "There is an error, rollback the change"
    finally:
        cur.close()
        con.close()


def ViewJournal():
    return render_template("viewjournal.html")


@ app.route("/editor")
def EditJournal():
    return render_template("editjournal.html")

# This function is to test  db connection


def findAllJournals():
    con = dbconnection()
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Journal")
    rows = cur.fetchall()
    return rows


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()

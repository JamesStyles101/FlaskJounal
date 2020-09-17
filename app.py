from flask import Flask, render_template, request
import sqlite3
from db import dbconnection
app = Flask(__name__)


@app.route("/")
def welcome():
    testSelect()
    return render_template("welcome.html")


@app.route("/journals")
def journal():
    return render_template("journals.html")


@app.route("/newjournal")
def JournalProgress():
    return render_template("newjournal.html")


@app.route("/result")
def Result():
    return render_template("result.html")


@app.route("/viewer")
def ViewJournal():
    return render_template("viewjournal.html")


@app.route("/editor")
def EditJournal():
    return render_template("editjournal.html")

# This function is to test  db connection


def testSelect():
    cur = dbconnection().cursor()
    cur.execute("SELECT * FROM Journal")
    rows = cur.fetchall()
    for row in rows:
        print(row)


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()

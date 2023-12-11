import json
from flask import Flask, request, jsonify
import sqlite3
import pickle
import pandas as pd
import os

def clean_data(data):
    columns = data.columns
    if "Unnamed: 0" in columns:
        data.drop(columns='Unnamed: 0', inplace=True)

    index = data[data["newpaper"].str.contains(r".*[a-zA-Z].*")].index  
    data.loc[index,"newpaper"] = data.loc[index,"newpaper"].str.replace("s","")
    data['newpaper'] = data['newpaper'].astype(float)
    data.rename(columns={"newpaper" : "newspaper"}, inplace=True)

    return data

def connect_db():
    conn = sqlite3.connect('advertising_new.db')

    return conn

def close_db(conn):
    conn.commit()
    conn.close()

def create_db(conn):
    cursor = conn.cursor()

    create_table = \
    """
        CREATE TABLE IF NOT EXISTS advertising (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TV FLOAT(32),
            radio FLOAT(32),
            newspaper FLOAT(32),
            sales FLOAT
        )
    """
    cursor.execute(create_table)


def add_data(conn):

    data = pd.read_csv('data/Advertising.csv')
    data = clean_data(data)


    if not os.path.exists("advertising_new.db"):
        data.to_sql(name="advertising", con=conn, if_exists="append", index=False)


def ingest_new_data(conn, data):

    cursor = conn.cursor()

    tv = data["TV"]
    radio = data["radio"]
    newspaper = data["newspaper"]

    query_2 = \
    f"""
        INSERT INTO advertising (TV, radio, newspaper) VALUES ({tv},{radio},{newspaper})

    """
    cursor.execute(query_2)

    query_comp = "SELECT * FROM advertising ORDER BY id DESC LIMIT 1 "

    data = cursor.execute(query_comp)
    results = data.fetchall()

    return results


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    conn = connect_db()
    create_db(conn)
    add_data(conn)
    close_db(conn)
    return "Welcome to mi API conected to predict model"

@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    data = pd.read_csv('data/Advertising.csv')
    data = clean_data(data)
    X_test = data[["TV", "radio", "newspaper"]]

    prediction = model.predict(X_test)

    return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'


@app.route('/v2/ingest_data', methods=["POST"])
def ingest_data():
    conn = connect_db()
    adv = {}
    adv["TV"] = float(request.args.get("TV"))
    adv["radio"] = float(request.args.get("radio"))
    adv["newspaper"] = float(request.args.get("newspaper"))

    comp = ingest_new_data(conn, adv)

    close_db(conn)
    return comp

@app.route('/v2/retrain', methods=['GET'])
def retrain():
    model = pickle.load(open('data/advertising_model','rb'))
    conn = connect_db()
    cursor = conn.cursor()

    query =\
    """
        SELECT TV, radio, newspaper FROM advertising
    """
    data = cursor.execute(query)
    results = data.fetchall()

    print(results)

    columns = [descripcion[0] for descripcion in cursor.description]
    X_test = pd.DataFrame(results, columns=columns)

    prediction = model.predict(X_test)

    close_db(conn)
    return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

app.run()
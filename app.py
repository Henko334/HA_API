from flask import Flask, request, jsonify
import sqlite3
import time
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('/home/henko/Desktop/WeatherDB/database.db')  # Update with actual path
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/log_event', methods=['POST'])
def write_data():
    data = request.json
    timestamp = time.localtime()
    formatted_time = f"{timestamp[0]:04d}-{timestamp[1]:02d}-{timestamp[2]:02d} {timestamp[3]:02d}:{timestamp[4]:02d}:{timestamp[5]:02d}"
    field1 = formatted_time
    field2 = data.get('Event')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO LogEvents (DateTime, Event) VALUES (?, ?)', (field1, field2))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

@app.route('/log_readings', methods=['POST'])
def write_climate():
    data = request.json
    timestamp = time.localtime()
    formatted_time = f"{timestamp[0]:04d}-{timestamp[1]:02d}-{timestamp[2]:02d} {timestamp[3]:02d}:{timestamp[4]:02d}:{timestamp[5]:02d}"
    field1 = formatted_time
    field2 = data.get('Temperature')
    field3 = data.get('Humidity')
    field4 = data.get('Pressure')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Readings (DateTime, Temperature, Humidity, Preasure) VALUES (?, ?, ?, ?)', (field1, field2, field3, field4))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"}), 200

@app.route('/read_events', methods=['GET'])
def read_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM LogEvents')
    rows = cursor.fetchall()
    conn.close()

    result = [{"LogID": row["LogID"], "DateTime": row["DateTime"], "Event": row["Event"]} for row in rows]
    return jsonify(result), 200

@app.route('/GetWeatherInfo', methods=['GET'])
def GetWeatherInfo():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Readings')
    rows = cursor.fetchall()
    conn.close()

    result = [{"ReadingID": row["ReadingID"], "DateTime": row["DateTime"], "Temperature": row["Temperature"], "Humidity": row["Humidity"], "Preasure": row["Preasure"]} for row in rows]
    return jsonify(result), 200


@app.route('/health')
def health():
	result = [{"message":"OK"}]
	return jsonify(result),200


if __name__ == '__main__':
    app.run(host='192.168.0.3', port=5000)

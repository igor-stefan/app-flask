from flask import render_template, request
from app import app, socketio, emit
from app.controllers.backend import *


@app.route("/home", methods=['GET','POST'])
@app.route("/", methods=['GET','POST']) #decorator
def index():
    return render_template('home.html')


@socketio.on('connect')
def test_connect():
    global thread
    print('Client connected')
    if not thread.isAlive():
        thread_stop_event.clear()
        print("Starting Thread")
        thread = socketio.start_background_task(sendValues)

@socketio.on('get_back')
def getting_back():
    global thread
    print("THREAD ALIVE?", thread.isAlive())
    if not thread.isAlive():
        thread_stop_event.clear()
        thread = socketio.start_background_task(sendValues)

@socketio.on('stop')
def stop_thread(dolar):
    print(dolar)
    thread_stop_event.set()
    
@app.route("/co")
def gas_co():
    return render_template('graph.html',mygas='CO',
                            sensor='MQ7', ind=0)

@app.route("/co_2")
def gas_co2():
    return render_template('graph.html',mygas='CO2',
                            sensor='MQ135', ind=1)

@app.route("/o3")
def gas_o3():
    return render_template('graph.html',mygas='O3',
                            sensor='MQ131',ind=2)

@app.route("/no_2")
def gas_no2():
    return render_template('graph.html',mygas='NO2',
                            sensor='MICS6814', ind=3)

@app.route("/so_2")
def gas_so2():
    return render_template('graph.html',mygas='SO2',
                            sensor = '2SH12', ind=4)

@app.route("/livehc")
def live_all():
    return render_template('livehc.html')

@app.route("/livejs")
def live_js():
    return render_template('livejs.html')
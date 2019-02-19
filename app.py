# In debugging mode, flask seems to start the app twice which results in weird results.
# Debug mode has now been turned off

import json
import os.path
import random
from threading import Thread
from time import sleep

from flask import Flask, render_template
from flask_socketio import send, join_room, leave_room, SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
new_content = []
stocks = [1, 2, 3, 4, 5]
weather = [1, 2, 3, 4, 5]
temp_stocks = [1, 2, 3, 4, 5]
temp_weather = [1, 2, 3, 4, 5]
stock_names = ["Microsoft", "Google", "Facebook", "IBM", "TESLA"]
dictionary_stocks = {"Microsoft": stocks[0], "Google": stocks[1], "Facebook": stocks[2],
                     "IBM": stocks[3], "TESLA": stocks[4]}
dictionary_weather = {"Stuttgart": weather[0], "Karlsruhe": weather[1], "Hamburg": weather[2],
                      "Rostock": weather[3], "Dortmund": weather[4]}
user_id = 0
msg_id = 0

current_Val = stocks
old_Val = list(stocks)
slope = [0]*5           # list of 5 zeros
slope_old = [0]*5


def update_slope():
    global slope
    global slope_old
    global msg_id
    global stock_names

    for i in range(0, 5):
        if current_Val[i] > old_Val[i]:
            slope[i] = 1
        elif current_Val[i] == old_Val[i]:
            slope[i] = 0
        else:
            slope[i] = -1

    print("\n", msg_id, " ) Microsoft = ", current_Val[0], sep='')
    print(msg_id, ") Slope = ", slope[0])
    print(msg_id, ") Slope_old = ", slope_old[0])

    for s in range(0, 5):
        if (slope_old[s] == -1)and(slope[s] == 1):
            print(msg_id, "\n----- ***V PATTERN DETECTED*** ----- STOCK #", s, "\n")
            socketio.emit('V_detection', {stock_names[s]: 0}, room=stock_names[s])
            print("Emitted V detection for '", stock_names[s], "'")

    slope_old = list(slope)
    msg_id += 1


# Manages user IDs (decrements not working as of yet)
def gen_user_ID(new=0):
    global user_id
    if new == 0:
        user_id -= 1
    elif new == 1:
        user_id += 1
        yield user_id
    else:
        print(" Some error occurred ")


# This is for the STOCKS publisher
# Updates the main "dictionary_stocks" dictionary and sends updates to the subscribers accordingly
def dic_update_stocks():
    global current_Val
    for i in range(0, len(updates_stocks)):
        if updates_stocks[i] == 0:
            dictionary_stocks["Microsoft"] = stocks[0]
            x = {"Microsoft": dictionary_stocks["Microsoft"]}
            socketio.emit('stocks updated', x, room="Microsoft")
        if updates_stocks[i] == 1:
            dictionary_stocks["Google"] = stocks[1]
            x = {"Google": dictionary_stocks["Google"]}
            socketio.emit('stocks updated', x, room="Google")
        if updates_stocks[i] == 2:
            dictionary_stocks["Facebook"] = stocks[2]
            x = {"Facebook": dictionary_stocks["Facebook"]}
            socketio.emit('stocks updated', x, room="Facebook")
        if updates_stocks[i] == 3:
            dictionary_stocks["IBM"] = stocks[3]
            x = {"IBM": dictionary_stocks["IBM"]}
            socketio.emit('stocks updated', x, room="IBM")
        if updates_stocks[i] == 4:
            dictionary_stocks["TESLA"] = stocks[4]
            x = {"TESLA": dictionary_stocks["TESLA"]}
            socketio.emit('stocks updated', x, room="TESLA")


# This is for the WEATHER publisher
# Updates the main "dictionary_weather" dictionary and sends updates to the subscribers accordingly
def dic_update_weather():
    for i in range(0, len(updates_weather)):
        if updates_weather[i] == 0:
            dictionary_weather["Stuttgart"] = weather[0]
            x = {"Stuttgart": dictionary_weather["Stuttgart"]}
            socketio.emit('weather updated', x, room="Stuttgart")
        if updates_weather[i] == 1:
            dictionary_weather["Karlsruhe"] = weather[1]
            x = {"Karlsruhe": dictionary_weather["Karlsruhe"]}
            socketio.emit('weather updated', x, room="Karlsruhe")
        if updates_weather[i] == 2:
            dictionary_weather["Hamburg"] = weather[2]
            x = {"Hamburg": dictionary_weather["Hamburg"]}
            socketio.emit('weather updated', x, room="Hamburg")
        if updates_weather[i] == 3:
            dictionary_weather["Rostock"] = weather[3]
            x = {"Rostock": dictionary_weather["Rostock"]}
            socketio.emit('weather updated', x, room="Rostock")
        if updates_weather[i] == 4:
            dictionary_weather["Dortmund"] = weather[4]
            x = {"Dortmund": dictionary_weather["Dortmund"]}
            socketio.emit('weather updated', x, room="Dortmund")


# Checks for any changes in the data from the "Stocks" publisher and asynchronously updates the subscribers
def checker_stocks():
    while True:
        global temp_stocks
        global updates_stocks
        updates_stocks = []
        if temp_stocks != stocks:
            for i in range(0, len(stocks)):
                if stocks[i] != temp_stocks[i]:
                    updates_stocks.append(i)

            dic_update_stocks()
            temp_stocks = list(stocks)


# Checks for any changes in the data from the "Weather" publisher and asynchronously updates the subscribers
def checker_weather():
    # while True:
    global temp_weather
    global updates_weather
    updates_weather = []
    if temp_weather != weather:
        for i in range(0, len(weather)):
            if weather[i] != temp_weather[i]:
                updates_weather.append(i)

        dic_update_weather()
        temp_weather = list(weather)


# Updates the "Stocks" data with random values within a range
def genNumbers():
    global current_Val
    global stocks
    for i in range(0, 5):
        stocks[i] = round(random.uniform(30, 400), 2)
        # for name, value in dictionary_stocks.items():
        #     if value == temp_stocks[i]:
        #         print("stocks[",name,"]  = ", stocks[i], "\n")


# This is done to ensure randomness in time for the randomized values
def myTimer():
    while True:
        sleep(4)
        genNumbers()


# This function will keep fetching JSON data from a local repo or a live URL after a fixed interval
def get_weather():
    script_path = os.path.dirname(__file__)
    filename = os.path.join(script_path, 'weather_14.json')
    testFile = open(filename, 'r', encoding="utf8")
    for line in testFile:
        data = json.loads(line)
        if data['city']['name'] == 'Stuttgart':
            weather[0] = float(data['main']['temp'])
        if data['city']['name'] == 'Karlsruhe':
            weather[1] = float(data['main']['temp'])
        if data['city']['name'] == 'Hamburg':
            weather[2] = float(data['main']['temp'])
        if data['city']['name'] == 'Rostock':
            weather[3] = float(data['main']['temp'])
        if data['city']['name'] == 'Dortmund':
            weather[4] = float(data['main']['temp'])


# This function detects V-patterns and signals the UI
def pattern_detector():
    global old_Val
    global current_Val

    while True:
        if current_Val != old_Val:
            update_slope()
            old_Val = list(current_Val)


get_weather()
checker_weather()
# Thread that will wait for a random time and then call genNumbers()
t1 = Thread(target=myTimer)
t1.start()
# Thread that will monitor the stocks to see if any have changed and "marks" the changed stocks
t2 = Thread(target=checker_stocks)
t2.start()
# This thread checks if the V-pattern has been detected and signals the UI
t3 = Thread(target=pattern_detector)
t3.start()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('join')        # Assigning Rooms to subscription events
def on_join(subs):
    for element in subs:
        join_room(element)
        print(element)
        if element in dictionary_stocks:
            x = {element: dictionary_stocks[element]}
            socketio.emit('stocks updated', x, room=element)
        if element in dictionary_weather:
            y = {element: dictionary_weather[element]}
            socketio.emit('weather updated', y, room=element)
        print('someone has entered the room :', element)


# Handles unsubscription events
@socketio.on('leave')
def on_leave(unsubs):
    for element in unsubs:
        leave_room(element)
        print('someone has left the room :', element)


# Sends USER ID when user connects
@socketio.on('message')
def handleMessage (msg):
    the_generator = gen_user_ID(new=1)

    uid = next(the_generator)
    print("Message: " + msg)
    send(uid)


if __name__ == '__main__':
    socketio.run(app)

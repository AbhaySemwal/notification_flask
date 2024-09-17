import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from threading import Thread
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Background task that sends notifications every 10 seconds
def send_notifications():
    while True:
        time.sleep(10)  # Pause for 10 seconds
        notification = {"message": "This is a notification!"}
        print("Emitting notification:", notification)  # Debugging print
        try:
            socketio.emit("new_notification", notification)  # Removed 'broadcast=True'
        except Exception as e:
            print("Error emitting notification:", str(e))  # Catch any emission error

@app.route("/")
def index():
    return "Flask server with real-time notifications is running!"

def start_background_task():
    thread = Thread(target=send_notifications)
    thread.daemon = True  # Ensure the thread will exit when the main program exits
    thread.start()

if __name__ == "__main__":
    print("Starting background task")
    start_background_task()
    socketio.run(app, host="0.0.0.0", port=5000)

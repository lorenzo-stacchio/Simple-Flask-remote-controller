from flask import Flask, render_template, request
from flask_socketio import SocketIO
import pyautogui
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True

socketio = SocketIO(app, cors_allowed_origins="*")

def move_mouse(x_off, y_off, width=None,height=None):        
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x + x_off, current_y + y_off, duration=0.25)


def move_mouse_offset(x_start, x_end, y_start, y_end, width,height):
    current_x, current_y = pyautogui.position()
    w,h = pyautogui.size().width,pyautogui.size().height
    transform_w, transform_h = w/width, h/height
    # reproject to current screen size
    x_start, x_end = x_start * transform_w, x_end * transform_w
    y_start, y_end = y_start*transform_h, y_end *transform_h 
    x_off = x_end - x_start
    y_off = y_end - y_start
    pyautogui.moveTo(current_x + x_off, current_y + y_off, duration=0.25)

def left_click():
    pyautogui.click(button='left')

def right_click():
    pyautogui.click(button='right')

@socketio.on('move_mouse_offset')
def handle_move(json):
    x_start, x_end, y_start, y_end, width,height = json["x_start"],json["x_end"],json["y_start"],  json["y_end"],json["width"],json["height"]
    move_mouse_offset(x_start, x_end, y_start, y_end, width,height)


@socketio.on('move')
def handle_move(json):
    x = json['x']
    y = json['y']
    move_mouse(x, y)

@socketio.on('left_click')
def handle_left_click():
    left_click()

@socketio.on('right_click')
def handle_right_click():
    right_click()
    
@app.route('/home',methods = ['GET'])
def home():
    hostname=socket.gethostname()   
    ip=socket.gethostbyname(hostname)
    return render_template("index.html", ip=ip)

@app.route('/mousearea',methods = ['GET'])
def mousearea():
    print("TOTAL SIZE", pyautogui.size())
    return render_template("mousearea.html")


@app.route('/toucharea',methods = ['GET'])
def toucharea():
    return render_template("toucharea.html")


if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0")
    print(request.environ['REMOTE_ADDR'])
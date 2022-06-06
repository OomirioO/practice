# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 LED 작동시킴

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time
import threading

led=23  
buzzer=18 
delay=0.5
app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)                    #BOARD는 커넥터 pin번호 사용
                                   
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(buzzer, 100) 
do=262
re=294
mi=330
pa=349
sol=392
ra=440
si=493
do2=523
song=[sol, sol, ra, ra, sol, sol, mi,
    sol,sol,mi,mi,re,re,re,re,
    sol,sol,ra,ra,sol,sol,mi,mi,
    sol,mi,re,mi,do,do,do,do
] 

def music() :
    p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
    for fr in song :        
        p.ChangeFrequency(fr)
        time.sleep(delay)
            
        
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/led/on")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def turn_on():
    try:
        GPIO.output(led, GPIO.HIGH)         # 불을 켜고
        return "ok"                         # 함수가 'ok'문자열을 반환함
    except :
        return "fail"

@app.route("/led/off")
def turn_off():
    try:
        GPIO.output(led,GPIO.LOW)
        return "ok"
    except :
        return "fail"

@app.route("/play/music")
def play_music():
    try:
        t1 = threading.Thread(target=music)  # Thread t1 생성
        t1.start()                                              # Thread t1 실행
        return "ok"
    except :
        return "fail"

@app.route("/stop/music")
def stop_music():
    try:
        p.stop()
        return "ok"
    except:
        return "fail"

if __name__ == "__main__":
    app.run(host="0.0.0.0")

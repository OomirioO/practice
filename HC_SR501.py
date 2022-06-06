#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

#빨간색 LED, 센서 입력핀 번호 설정 
led_R = 20
sensor = 4
SERVO_PIN = 12
# 불필요한 warning 제거,  GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LED 핀의 IN/OUT(입력/출력) 설정 
GPIO.setup(led_R, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)

# GPIO 18번 핀을 출력으로 설정 
GPIO.setup(18, GPIO.OUT)

# 서보핀의 출력 설정 
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM 인스턴스 servo 생성, 주파수 50으로 설정 
servo = GPIO.PWM(SERVO_PIN,50)
# PWM 듀티비 0 으로 시작 
servo.start(0)
p = GPIO.PWM(18, 100)  
do=262
mi=330
sol=392
alarm=[do]

def play() :
    p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
    for fr in alarm :
        p.ChangeFrequency(fr)

print ("PIR Ready . . . . ")
time.sleep(1)  # PIR 센서 준비 시간 

try:
    while True:
        if GPIO.input(sensor) == True: 	#센서가 High(1)출력 
                GPIO.output(led_R, 1)   # 빨간색 LED 켬 
                #GPIO.output(SERVO_PIN,1)
                servo.ChangeDutyCycle(7.5) #차단
                print("Motion Detected !")
                time.sleep(0.2)
                play()

        elif GPIO.input(sensor) == False :      #센서가 Low(0)출력  
                GPIO.output(led_R, 0)   # 빨간색 LED 끔 
                #GPIO.output(SERVO_PIN,1)
                servo.ChangeDutyCycle(2.5)
                print("Motion Undetected !")
                time.sleep(0.2)
                p.stop()                    

except KeyboardInterrupt:
                print("Stopped by User")
                GPIO.cleanup()


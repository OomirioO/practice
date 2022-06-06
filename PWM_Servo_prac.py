#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

#서보모터를 PWM으로 제어할 핀 번호 설정 
SERVO_PIN = 18
button_pin = 15

# 불필요한 warning 제거
GPIO.setwarnings(False)

# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# 서보핀의 출력 설정 
GPIO.setup(SERVO_PIN, GPIO.OUT)
# 버튼 핀의 INPUT설정 , PULL DOWN 설정 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 인스턴스 servo 생성, 주파수 50으로 설정 
servo = GPIO.PWM(SERVO_PIN,50)
# PWM 듀티비 0 으로 시작 
servo.start(0)
button_press=0
def button_callback(channel):
    global button_press
    if button_press==0 :
        GPIO.output(SERVO_PIN,1)
        servo.ChangeDutyCycle(7.5)
        print("90도 회전")
        #time.sleep(1)
        button_press=1
    elif button_press==1 : #서보모터가 90도일 때
        GPIO.output(SERVO_PIN,1)
        servo.ChangeDutyCycle(2.5)
        print("0도 회전")
       #time.sleep(1)   
        button_press=0


try :
    GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300)      
    while 1:
        time.sleep(0.1)  # 0.1초 딜레이
except KeyboardInterrupt :
     servo.stop()
     GPIO.cleanup()

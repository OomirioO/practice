
#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다.
import RPi.GPIO as GPIO 
import time

# 사용할 GPIO핀의 번호를 선정합니다.
button_pin = 15
led_pin1 = 4 #green_led
led_pin2 = 17 #red_led

 # 불필요한 warning 제거
GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 
# 버튼 핀의 INPUT설정 , PULL DOWN 설정 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# LED 핀의 OUT설정
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

# boolean 변수 설정 
light_on1 = False
light_on2 = False
# button_callback 함수를 정의합니다.
def button_callback(channel):
    global light_on1, light_on2   # Global 변수선언 
    if light_on1 == False and light_on2==False:  # LED 불이 꺼져있을때 
        GPIO.output(led_pin1,1)   # LED ON 
        print("LED1 ON!")
        light_on1 =True
    elif light_on1 == True and light_on2 == False:
        GPIO.output(led_pin1,1) 
        GPIO.output(led_pin2,1)
        print("LED2 ON!")
        light_on2=True
    else:                                # LED 불이 져있을때 
        GPIO.output(led_pin1,0)  # LED OFF
        GPIO.output(led_pin2,0)
        print("LED OFF!")
        light_on1=False
        light_on2=False
''' light_on1 = not light_on1  # False <=> True
    light_on2 = not light_on2'''

# Event 알림 방식으로 GPIO 핀의 Rising 신호를 감지하면 button_callback 함수를 실행합니다. 300ms 바운스타임을 설정하여 잘못된 신호를 방지합니다.
GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300)      
        
while 1:
    time.sleep(0.1)  # 0.1초 딜레이


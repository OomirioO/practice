#-*- coding: utf-8 -*-

# 필요한 라이브러리를 불러옵니다.
import RPi.GPIO as GPIO
import spidev
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led_T= 23 #top
led_B= 24 #bottom
led_L= 13 #left
led_R= 19 #right
GPIO.setup(led_T, GPIO.OUT)
GPIO.setup(led_B, GPIO.OUT)
GPIO.setup(led_L, GPIO.OUT)
GPIO.setup(led_R, GPIO.OUT)

buzzer=18 #buzzer

GPIO.setup(18, GPIO.OUT)

# PWM 듀티비 0 으로 시작 
p = GPIO.PWM(buzzer, 100) 

do=262
re=294
mi=330
pa=349
sol=392
ra=440
si=493
do2=523
song=[sol, sol, ra, ra, sol, sol, mi,mi,
    sol,sol,mi,mi,re,re,re,re,
    sol,sol,ra,ra,sol,sol,mi,mi,
    sol,mi,re,mi,do,do,do,do]

def play() :
    p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
    for fr in song :
        p.ChangeFrequency(fr)
        time.sleep(delay)

# 딜레이 시간 (센서 측정 간격)
delay = 0.5

# MCP3008 채널설정
sw_channel = 0
vrx_channel = 1
vry_channel = 2

# SPI 인스턴스 spi 생성
spi = spidev.SpiDev()

# SPI 통신 시작하기
spi.open(0, 0)

# SPI 통신 속도 설정
spi.max_speed_hz = 100000

# 0 ~ 7 까지 8개의 채널에서 SPI 데이터를 읽어옵니다.
def readadc(adcnum):
  if adcnum > 7 or adcnum < 0:
    return -1
  r = spi.xfer2([1, 8 + adcnum << 4, 0])
  data = ((r[1] & 3) << 8) + r[2]
  return data


try:
  # 무한루프
  while True:
    # X, Y 축 포지션
    vrx_pos = readadc(vrx_channel)
    vry_pos = readadc(vry_channel)
    # 스위치 입력
    sw_val = readadc(sw_channel)
  
    time.sleep(delay)
  
    if vry_pos==1023 :
      print("top")
      GPIO.output(led_T, 1)   # top LED on
      GPIO.output(led_B, 0)
      GPIO.output(led_R, 0)
      GPIO.output(led_L, 0)
      time.sleep(1)

    elif vry_pos<10 :
      print("bottom")
      GPIO.output(led_T, 0)
      GPIO.output(led_B, 1)   # bottom LED on
      GPIO.output(led_R, 0)
      GPIO.output(led_L, 0)


    elif vrx_pos==1023 :
      print("right")
      GPIO.output(led_T, 0)
      GPIO.output(led_B, 0)
      GPIO.output(led_R, 1)   # right LED on
      GPIO.output(led_L, 0)
      time.sleep(1)

    elif vrx_pos<10 :
      print("left")
      GPIO.output(led_T, 0)
      GPIO.output(led_B, 0)
      GPIO.output(led_R, 0)
      GPIO.output(led_L, 1)   # left LED on
      time.sleep(1)

    else :
      GPIO.output(led_T, 0)
      GPIO.output(led_B, 0)
      GPIO.output(led_R, 0)
      GPIO.output(led_L, 0)
    
    if sw_val<10 :
      play()
    
    elif sw_val!=0 :
      p.stop()
    
    # 출력
    print("X:{}  Y:{}  SW:{}".format(vrx_pos, vry_pos, sw_val))


except KeyboardInterrupt:
    print("Stopped by User")
GPIO.cleanup()

import RPi.GPIO as GPIO
from time import sleep

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT, initial=GPIO.LOW)
fan = GPIO.PWM(ledpin,25)		#create PWM instance with frequency
fan.start(30)				#start PWM of required Duty Cycle

while True:
    sleep(10)
#    for duty in range(0,101,1):
#        fan.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
#        sleep(0.05)
#    sleep(2)
#    
#    for duty in range(100,-1,-1):
#        fan.ChangeDutyCycle(duty)
#        sleep(0.05)
#    sleep(2)

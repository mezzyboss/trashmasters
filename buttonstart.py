import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        input_state = GPIO.input(18)
        if input_state == False:
            subprocess.call(['python3', '/home/pi/Desktop/nanpy/smartbin.py'])

except KeyboardInterrupt:
	GPIO.cleanup()

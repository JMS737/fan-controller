import logging
import signal
import sys
import time
import RPi.GPIO as GPIO

FAN_CURVE = [[40,0], [50,20], [60,50], [70,100]]

class FanController:
    def __init__(self, pin, frequency, minSpeed=30, pollingInterval=1):
        self.pollingInterval = pollingInterval
        self.minSpeed = minSpeed

        self.logger = self._init_logger()
        self.logger.info('Fan Controller instance created')
        self.fan = self._init_gpio(pin, frequency)
        signal.signal(signal.SIGTERM, self._handle_sigterm)

    def _init_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(logging.Formatter('%(levelname)8s | %(message)s'))
        logger.addHandler(stdout_handler)
        return logger
    
    def _init_gpio(self, pin, freq):
        GPIO.setmode(GPIO.BOARD)    #set pin numbering system
        GPIO.setup(pin,GPIO.OUT, initial=GPIO.LOW)
        fan = GPIO.PWM(pin, freq)
        return fan
    
    def start(self):
        self.fan.start(30)
        self.logger.info('Fan Controller started')
        try:
            while True:
                self.process()
                time.sleep(self.pollingInterval)
        except KeyboardInterrupt:
            self.logger.warning('Keybord interrupt (SIGINT) received...')
            self.stop()

    def process(self):
        temp = self.getTemperature()
        speed = self.getSpeed(temp)
        self.fan.ChangeDutyCycle(speed)

        self.logger.debug(f'Temp: {temp}, Speed: {speed}')

    def getSpeed(self, temperature):
        speed = 0
        for point in reversed(FAN_CURVE):
            if temperature >= point[0]:
                speed = point[1]
                break
        
        if speed > 0 and speed < self.minSpeed:
            speed = self.minSpeed

        return speed

    def stop(self):
        self.logger.info('Stopping fan-controller...')
        GPIO.cleanup()
        sys.exit(0)

    def _handle_sigterm(self, sig, frame):
        self.logger.warning('SIGTERM received...')
        self.stop()

    def getTemperature(self):
        cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
        cpuTemp = float(cpuTempFile.read()) / 1000
        cpuTempFile.close()

        return cpuTemp

if __name__ == '__main__':
    service = FanController(12, 25)
    service.start()

from machine import Pin, PWM, Timer
from utime import sleep
from random import randint

# Global variables
# PWM frequency
PWM_FREQ = 1000

class Light:
    def __init__(self, pins, intentisy, speed):

        # Get the list of pins used by this object
        self.pins: list[Pin] = pins

        # Create a list of PWM objects from the pins
        self.pwm_pins = [PWM(pin, freq=PWM_FREQ) for pin in self.pins]


        # Set the intensity of the light
        self.intensity: int = intentisy

        # Set the speed of the light
        self.speed: int = speed

        # Set the position of the light
        self.position: int = 0
        self.pattern_position: int = 0

        # Set the length of the light
        self.length: int = len(self.pins)

        # Set the state of the light
        # self.state = True is on,
        # self.state = False is off
        self.state: bool = False

        # Create the timer object
        self.timer = Timer()

    def on(self):
        # Set the state to True
        self.state = True
        self.timer.init(period=self.speed, mode=Timer.PERIODIC, callback=self.tick)

    def off(self):  
        # Set the state to False
        self.state = False
        self.timer.deinit()

        # Turn off all the pins
        for pwm_pin in self.pwm_pins:
            pwm_pin.duty_u16(0)

        # Reset the position
        self.position = 0

    def toggle(self):
        # If the state is False, set it to True
        if self.state == False:
            self.on()

        else:
            # If the state is True, set it to False
            # If you're here and you shouldn't be, at least it turns off
            self.off()

    def tick(self, next):
        pass
                    
    

class Spinner(Light):

    def tick(self, next):

        # If the state is True, run the light
        if self.state:

            # Turn off the current pin
            self.pwm_pins[self.position].duty_u16(0)

            # Set the next pin to 1/3 of the intensity
            next_position = self.position + 1
            if next_position >= self.length:
                next_position = 0
            self.pwm_pins[next_position].duty_u16(int(self.intensity / 3))

            # Set the next next pin to full of the intensity
            next_next_position = next_position + 1
            if next_next_position >= self.length:
                next_next_position = 0
            self.pwm_pins[next_next_position].duty_u16(int(self.intensity))

            # Increment the position
            self.position += 1
            if self.position >= self.length:
                self.position = 0

class Blinker(Light):

    def tick(self, next):

        # Not sure where to put this yet, but for now it's here.
        # This is the blink pattern
        # Each tick is a light modifier
        self.pattern = [
            100, # start on
            0, # off
            100, # on
            0, # off
            0, # off, extra pause
            ]

        # If the state is True, run the light
        if self.state:

            # Execute pattern position
            self.pwm_pins[self.position].duty_u16(int(self.intensity * self.pattern[self.pattern_position] / 100))

            # Increment the pattern position
            self.pattern_position += 1
            if self.pattern_position >= len(self.pattern):
                self.pattern_position = 0

                # If we're at the end of the pattern, increment the position
                self.position += 1
                if self.position >= self.length:
                    self.position = 0

                                                  
        

# Create light objects
lSpinnerSpeed = randint(60, 80)
lSpinner = Spinner([Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(2, Pin.OUT), Pin(3, Pin.OUT)], 65500, lSpinnerSpeed)

rSpinnerSpeed = randint(60, 80)
rSpinner = Spinner([Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT)], 65500, rSpinnerSpeed)

# Turn on the light
lSpinner.on()
rSpinner.on()

# Create light obljects
lBlinkerSpeed = randint(60, 80)
lBlinker = Blinker([Pin(8, Pin.OUT), Pin(9, Pin.OUT)], 65500, lBlinkerSpeed)

rBlinkerSpeed = randint(60, 80)
rBlinker = Blinker([Pin(10, Pin.OUT), Pin(11, Pin.OUT)], 65500, rBlinkerSpeed)

# Turn on the light
lBlinker.on()
rBlinker.on()

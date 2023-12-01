from machine import ADC, Pin, I2C, Timer
import ssd1306
import utime

class Sensor:
    def __init__(self, pin):
        # Initialize Sensor object with min and max moisture values and the specified pin
        self.min_moisture = 65535
        self.max_moisture = 21000
        self.pin = pin

    def read(self):
        # Read moisture level from the sensor and calculate the percentage
        sensor = ADC(Pin(self.pin))
        moisture = 100 - ((self.max_moisture-sensor.read_u16())
                          * 100/(self.max_moisture-self.min_moisture))
        return moisture
    

class CustomMachine:
    def __init__(self, machine_id, I2C_channel, I2C_data, I2C_clock, sensor_pin1, sensor_pin2, led_pin1, led_pin2, button_pin):
        # Initialize CustomMachine object with specified parameters
        self.machine_id = machine_id
        self.i2c = I2C(I2C_channel, sda=Pin(I2C_data), scl=Pin(I2C_clock))
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.soil_sensor1 = Sensor(sensor_pin1)
        self.soil_sensor2 = Sensor(sensor_pin2)
        self.sensors = [self.soil_sensor1, self.soil_sensor2]
        self.led1 = Pin(led_pin1, Pin.OUT)
        self.led2 = Pin(led_pin2, Pin.OUT)
        self.leds = [self.led1, self.led2]
        self.readDelay = 10
        self.button = Pin(button_pin, Pin.IN)
        self.button_state = 2
        self.last_button_state = 1
        self.press_threshold = 500  # Adjust as needed
        self.debounce_delay = 50 # Adjust as needed

        # Initialize OLED to display blank screen
        self.oled.fill(0)
        self.oled.show()


    def check_button_state(self):
        # Check the state of the button and handle button press
        current_button_state = self.button.value()

        if current_button_state == 0 and self.last_button_state == 1:

            # Button has just been pressed
            if self.button.value() == 0:
                self.handle_button_press()
                utime.sleep_ms(self.debounce_delay)

        self.last_button_state = current_button_state


    def handle_button_press(self):
        # Handle the button press and update OLED display based on button state
        if self.button_state == 0:
            # Display data from sensor 1
            self.oled.fill(0)  # Clear the display
            self.oled.text(f"Plant 1", 0, 1)
            self.oled.write_text('Moisture', 0, 16, 2)
            sensor_reading = int(self.soil_sensor1.read())
            # Display sensor reading, with correction if sensor reads outside of set range
            if sensor_reading < 0:
                self.oled.write_text('0%', 30, 40, 3)
            elif sensor_reading < 100:
                self.oled.write_text(f"{sensor_reading}%", 30, 40, 3)
            else:
                self.oled.write_text("100%", 10, 40, 3)
            self.oled.show()
        elif self.button_state == 1:
            # Display data from sensor 2
            self.oled.fill(0)  # Clear the display
            self.oled.text(f"Plant 2", 0, 1)
            self.oled.write_text('Moisture', 0, 16, 2)
            sensor_reading = int(self.soil_sensor2.read())
            # Display sensor reading, with correction if sensor reads outside of set range
            if sensor_reading < 0:
                self.oled.write_text('0%', 30, 40, 3)
            elif sensor_reading < 100:
                self.oled.write_text(f"{sensor_reading}%", 30, 40, 3)
            else:
                self.oled.write_text(f"100%", 10, 40, 3)
            self.oled.show()
        elif self.button_state == 2:
            # Display blank screen
            self.oled.fill(0)
            self.oled.show()

        # Move to the next state
        self.button_state = (self.button_state + 1) % 3  # Cycle between 0, 1, 2

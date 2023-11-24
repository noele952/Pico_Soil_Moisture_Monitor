from machine import ADC, Pin, I2C, Timer
import utime
import ssd1306
import network
import BlynkLib

# Configuration
min_moisture = 65535
max_moisture = 21000
readDelay = 10
SSID = 'ssid_name'
SSID_PASSWORD = 'secret'
BLYNK_AUTH = "blynk_auth_token"

# Blynk initialization
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# I2C display setup
i2c = I2C(0, sda=Pin(8), scl=Pin(9))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# LED pins
led_pins = [Pin(15, Pin.OUT), Pin(16, Pin.OUT)]

# Network connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, SSID_PASSWORD)

# Wait for connection
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    utime.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip = wlan.ifconfig()[0]
    print('IP: ', ip)


class Sensor:
    """Represents a soil moisture sensor."""
    def __init__(self, pin):
        self.min_moisture = 65535
        self.max_moisture = 21000
        self.pin = pin

    def read(self):
        sensor = ADC(Pin(self.pin))
        moisture = 100 - ((max_moisture - sensor.read_u16()) * 100 / (max_moisture - min_moisture))
        return moisture


class ButtonDisplayStateMachine:
    """Handles the button press and updates the OLED display based on the button state."""
    def __init__(self, button_pin, oled, sensor1, sensor2):
        self.button = Pin(button_pin, Pin.IN)
        self.oled = oled
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.state = 2
        self.last_button_state = 1
        self.press_threshold = 500  # Adjust this threshold based on your requirements
        self.debounce_delay = 50
        

        self.hourly_timer = Timer(
            period=60000, mode=Timer.PERIODIC, callback=self.send_data_to_blynk)

        # Initialize OLED to display blank screen
        self.oled.fill(0)
        self.oled.show()

    def send_data_to_blynk(self, timer):
        # Function to send moisture data to Blynk
        print("send data to blynk")
        moisture1 = int(self.sensor1.read())  
        blynk.virtual_write(7, moisture1)

        print(f'moisture1: {moisture1}')

        moisture2 = int(self.sensor2.read())  

        print('in  moisture2')
        blynk.virtual_write(8, moisture2)
        print('deeper in moisture2')
        blynk.run()
        utime.sleep(1)
        print(f'moisture2: {moisture2}')

    def check_button_state(self):
        # Check the state of the button and handle the press accordingly
        current_button_state = self.button.value()

        if current_button_state == 0 and self.last_button_state == 1:

            if self.button.value() == 0:
                self.handle_button_press()
                utime.sleep_ms(self.debounce_delay)

        self.last_button_state = current_button_state

    def handle_button_press(self):
        # Update display data based on the current state
        if self.state == 0:
            # Display data from sensor 1
            oled.fill(0)  y
            oled.text(f"Plant 1", 0, 1)
            oled.write_text('Moisture', 0, 16, 2)
            sensor_reading = int(self.sensor1.read())
            if sensor_reading < 10:
                oled.write_text('', 30, 40, 3)
            if sensor_reading < 100:
                oled.write_text(f"{sensor_reading}%", 30, 40, 3)
            else:
                oled.write_text("100%", 10, 40, 3)
            oled.show()
        elif self.state == 1:
            # Display data from sensor 2
            oled.fill(0) y
            oled.text(f"Plant 2", 0, 1)
            oled.write_text('Moisture', 0, 16, 2)
            sensor_reading = int(self.sensor2.read())
            if sensor_reading < 10:
                oled.write_text('', 30, 40, 3)
            if sensor_reading < 100:
                oled.write_text(f"{sensor_reading}%", 30, 40, 3)
            else:
                oled.write_text(f"{sensor_reading}%", 10, 40, 3)
            oled.show()
        elif self.state == 2:
            # Display blank screen
            self.oled.fill(0)
            self.oled.show()

        self.state = (self.state + 1) % 3  # Cycle between 0, 1, 2


def main():
    # Main function to control the flow of the program
    led_states = [False, False]  # Initially, both LEDs are off

    while True:
        button_display_fsm.check_button_state()
        utime.sleep_ms(50)
        sensor_data = [sensor1.read(), sensor2.read()]
        for index, data in enumerate(sensor_data):
            if data < 50:
                led_pins[index].on()
                led_states[index] = True
            elif led_states[index]:
                led_pins[index].off()
                led_states[index] = False

        utime.sleep_ms(readDelay)


if __name__ == "__main__":
    main()
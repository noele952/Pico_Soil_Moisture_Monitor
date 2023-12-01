from machine import Timer
from my_machine import CustomMachine
from mqtt import MQTT
import utime
import network


# Define MQTT parameters
MQTT_ENDPOINT = 'a1j74h8kgrsvow-ats.iot.us-east-1.amazonaws.com'
MQTT_CLIENT_ID = 'soil_moisture_machine'

# Set up Wi-Fi credentials
SSID = "Howard"
SSID_Password = "Scally12"


# Connect to the network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, SSID_Password)
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    utime.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip = wlan.ifconfig()[0]
    print('IP: ', ip)

# Instantiate a CustomMachine object
soil_machine = CustomMachine(machine_id = 123456789,
                             I2C_channel=0, 
                             I2C_data=8, 
                             I2C_clock=9, 
                             sensor_pin1=27, 
                             sensor_pin2=28, 
                             led_pin1=15, 
                             led_pin2=16, 
                             button_pin=0)

# Create MQTT connection
mqtt = MQTT(soil_machine.machine_id, 
            endpoint=MQTT_ENDPOINT, 
            client_id=MQTT_CLIENT_ID, 
            topic_pub=b'SoilMoistureMachine')


# Post data via MQTT
def send_data_mqtt(label, data):
    try:
        mqtt.post(label, data)
    except Exception as error:
        print("An mqtt post error occured:", error)


def main():
    led_states = [False, False]  # Initially, both LEDs are off

    # Set up periodic timer to send sensor data via MQTT, and print to terminal
    Timer(period=3600000, mode=Timer.PERIODIC, callback=send_data_mqtt(label='Soil_Sensor_1', data=soil_machine.soil_sensor1.read()))
    print(f'Soil_Sensor1: {soil_machine.soil_sensor1.read()}')
    Timer(period=3600000, mode=Timer.PERIODIC, callback=send_data_mqtt(label='Soil_Sensor_2', data=soil_machine.soil_sensor2.read()))
    print(f'Soil_Sensor2: {soil_machine.soil_sensor2.read()}')
    
    while True:
        soil_machine.check_button_state()
        utime.sleep_ms(50)
        
        # Read sensor data
        sensor_data = [soil_machine.soil_sensor1.read(), soil_machine.soil_sensor2.read()]
        
        # Check sensor data and set LEDs
        for index, data in enumerate(sensor_data):
            if data < 50:
                soil_machine.leds[index].on()
                led_states[index] = True
            elif led_states[index]:
                soil_machine.leds[index].off()
                led_states[index] = False

        utime.sleep_ms(soil_machine.readDelay)


if __name__ == "__main__":
    main()
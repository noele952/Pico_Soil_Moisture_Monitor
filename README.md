# Pico Soil Moisture Monitor

This project is a plant monitoring system that measures soil moisture levels using sensors and displays the information on an OLED screen. The system is designed to work with Blynk for remote monitoring.

## Table of Contents

- [Software Dependencies](#software-dependencies)
- [Hardware Setup](#hardware-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Software Dependencies

Install the following Micropythonlibraries on the pico w microcontroller

- [SSD1306 Driver GitHub](https://github.com/noele952/micropython-ssd1306-custom-text/blob/main/ssd1306.py)

- [Blynk Library Python](https://github.com/vshymanskyy/blynk-library-python/blob/master/BlynkLib.py)

- [umqtt.simple GitHub](https://github.com/fizista/micropython-umqtt.simple2)

## Hardware Setup

### Wiring Diagram

<p align="center">
<img src="https://hydropi.s3.us-east-2.amazonaws.com/github/soil_moisture_monitor/soil_moisture_monitor.png" alt="pico soil moisture monitor - wiring diagram" width="600" />
</p>

<p align="center">
<img src="https://hydropi.s3.us-east-2.amazonaws.com/github/soil_moisture_monitor/pico_soil_moisture_monitor_front1.jpg" alt="pico soil moisture monitor" width="600" />
</p>

<p align="center">
<img src="https://hydropi.s3.us-east-2.amazonaws.com/github/soil_moisture_monitor/pico_soil_moisture_monitor_front2.jpg" alt="pico soil moisture monitor" width="600" />
</p>

<p align="center">
<img src="https://hydropi.s3.us-east-2.amazonaws.com/github/soil_moisture_monitor/pico_soil_moisture_monitor_rear1.jpg" alt="pico soil moisture monitor" width="600" />
</p>

<p align="center">
<img src="https://hydropi.s3.us-east-2.amazonaws.com/github/soil_moisture_monitor/pico_soil_moisture_monitor_rear2.jpg" alt="pico soil moisture monitor" width="600" />
</p>

#### Demo -> Click For Video

[![Alt text](https://img.youtube.com/vi/FW9FmY1-QZE/0.jpg)](https://www.youtube.com/watch?v=FW9FmY1-QZE)

## Usage

To use this plant monitoring system, follow these steps:

1. Clone the repository to the pico microcontroller.
2. Set up the hardware as per the instructions in the [Hardware Setup](#hardware-setup) section.
3. Ensure that the required libraries are available on your Microcontroller's filesystem. You can place them in a `lib` directory in your project folder.
4. Configure the necessary parameters in the code, such as Wi-Fi credentials and Blynk authentication token.
5. Run the main script on your microcontroller.

The soil moisture monitor can be powered by USB, or a 3V battery

## Contributing

Contributions are welcome! If you have improvements or bug fixes, feel free to submit a pull request. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the [MIT License](LICENSE).
